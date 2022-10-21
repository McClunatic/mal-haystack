"""Defines the MAL Haystack main entry point."""

import argparse
import sys
from typing import List

from haystack.pipelines import Pipeline

from mal_haystack.nodes import SeriesConverter, ZipDataFramer, ZipLister


def get_parser() -> argparse.ArgumentParser:
    """Gets the main MAL Haystack CLI argument parser.

    Returns:
        The main argument parser.
    """

    parser = argparse.ArgumentParser(
        description='Extracts and preprocesses documents from Zip file(s)',
    )
    parser.add_argument(
        'zip_files',
        nargs='+',
        help='zip file(s) to extract preprocessed documents from',
    )
    return parser


def main(argv: List[str] = sys.argv[1:]) -> int:
    """Extracts and preprocesses documents from Zip file(s).

    Arguments:
        argv: The list of command line or main arguments.
    """

    args = get_parser().parse_args(argv)

    lister = ZipLister()
    framer = ZipDataFramer()
    converter = SeriesConverter()
    p = Pipeline()
    p.add_node(component=lister, name='ZipLister', inputs=['File'])
    p.add_node(component=framer, name='ZipFramer', inputs=['ZipLister'])
    p.add_node(
        component=converter, name='SeriesConverter', inputs=['ZipFramer'])

    result = p.run(
        file_paths=args.zip_files,
        params={
            'ZipLister': {'valid_names': ['MAL Anime Reviews 85k.csv']},
            'SeriesConverter': {'series': 'Review'},
        },
    )
    print(
        f'Read {len(result["documents"])} documents from {args.zip_files}')


if __name__ == '__main__':
    sys.exit(main())
