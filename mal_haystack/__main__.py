"""Defines the MAL Haystack main entry point."""

import argparse
import csv
import logging
import sys
from typing import List

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes.reader import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from tqdm.auto import tqdm

from mal_haystack.nodes import EmbeddingRetriever, ZipLister
from mal_haystack.pipelines import ReviewIndexer, ZippedReviewIndexer


def get_parser() -> argparse.ArgumentParser:
    """Gets the main MAL Haystack CLI argument parser.

    Returns:
        The main argument parser.
    """

    parser = argparse.ArgumentParser(
        description='Extracts metadata and query answers from CSV documents',
    )

    parser.add_argument(
        'document_column',
        help='name of column to regard as documents for query purposes',
    )
    parser.add_argument(
        'files',
        nargs='+',
        help='file(s) to extract preprocessed documents from',
    )
    parser.add_argument(
        '-z', '--zip-path',
        help='path to zip containing CSV files, if compressed',
    )
    parser.add_argument(
        '-m', '--metadata-column',
        action='append',
        help='name of metadata column to extract (usable multiple times)',
    )
    parser.add_argument(
        '-q', '--query',
        action='append',
        help='query to extract answers for per document',
    )
    parser.add_argument(
        '--no-gpu',
        action='store_true',
        help='do not use the GPU to accelerate extractive QA pipeline',
    )
    parser.add_argument(
        '--output',
        default='output.csv',
        help='name of output CSV file to write',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='enable haystack pipeline debugging output',
    )
    return parser


def main(argv: List[str] = sys.argv[1:]) -> int:
    """Extracts and preprocesses documents from Zip file(s).

    Arguments:
        argv: The list of command line or main arguments.
    """

    args = get_parser().parse_args(argv)

    if args.debug:
        logging.getLogger('haystack.pipelines.base').setLevel(logging.DEBUG)

    # Confirm at least 1 metadata column or query
    if not args.metadata_column and not args.query:
        raise ValueError('No metadata columns or queries specified!')

    # Create and run index pipeline
    document_store = InMemoryDocumentStore(
        embedding_dim=384,  # This is to match the model used
        similarity='cosine',
    )
    if args.zip_path:
        lister = ZipLister()
        pipeline = ZippedReviewIndexer(lister, document_store)
        pipeline.run(file_paths=[args.zip_path], params={
            'ZipLister': {'valid_names': args.files},
            'DataFrameConverter': {
                'document_column': args.document_column,
                'meta_columns': args.metadata_column,
            },
        })
    else:
        pipeline = ReviewIndexer(document_store)
        pipeline.run(file_paths=args.files)

    # Create query pipeline
    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model='sentence-transformers/all-MiniLM-L6-v2',
        use_gpu=not args.no_gpu,
    )

    # Important:
    # Now that we initialized the Retriever, we need to call update_embeddings
    # to iterate over all previously indexed documents and update their
    # embedding representation.
    # While this can be a time consuming operation (depending on the corpus
    # size), it only needs to be done once. At query time, we only need to
    # embed the query and compare it to the existing document embeddings, which
    # is very fast.
    document_store.update_embeddings(retriever)

    reader = FARMReader(
        'deepset/roberta-base-squad2',
        num_processes=1,  # Eliminate multiprocessing hangups
        use_gpu=not args.no_gpu,
    )
    query_pipeline = ExtractiveQAPipeline(reader, retriever)

    document_generator = document_store.get_all_documents_generator()
    metadata_records = []
    document_count = document_store.get_document_count()
    desc = 'Extracting document metadata'
    for document in tqdm(document_generator, desc=desc, total=document_count):

        # Get column metadata
        metadata = document.meta.copy()

        # Get QA metadata
        filters = {'index': {'$eq': metadata['index']}}
        if args.query:
            result = query_pipeline.run_batch(args.query, params={
                'Retriever': {'filters': filters},
            })
            for idx, (query, answers) in enumerate(
                zip(result['queries'], result['answers'])
            ):
                metadata[f'Q{idx + 1}'] = query
                metadata[f'Q{idx + 1} answer'] = answers[0].answer
                metadata[f'Q{idx + 1} score'] = answers[0].score
                metadata[f'Q{idx + 1} context'] = answers[0].context

        metadata_records.append(metadata)

    # Write metadata records to output CSV
    chunk_index = 0
    chunk_size = 256  # TODO: Considerin making this an option
    desc = f'Writing metadata records to {args.output}'
    with (
        tqdm(desc=desc, total=len(metadata_records)) as pbar,
        open(args.output, 'w', newline='') as outfile,
    ):
        writer = csv.DictWriter(outfile, metadata_records[0].keys())
        while chunk_index < len(metadata_records):
            writer.writerows(
                metadata_records[chunk_index:chunk_index + chunk_size])
            chunk_index += chunk_size
            pbar.update(min(chunk_index, len(metadata_records)))


if __name__ == '__main__':
    sys.exit(main())
