"""Defines MAL Haystack custom pipelines."""

from typing import Optional

from haystack import Pipeline
from haystack.document_stores import BaseDocumentStore
from haystack.pipelines.standard_pipelines import BaseStandardPipeline
from .nodes import (
    DataFramer,
    DataFrameConverter,
    ZipDataFramer,
    ZipLister,
)


class ReviewIndexer(BaseStandardPipeline):
    """Pipeline for indexing and tagging zipped MAL reviews.

    Pipeline nodes are:
      - DataFramer (CSVs -> DataFrames)
      - DataFrameConverter (DataFrames -> Documents)
      - DocumentStore (Documents -> DocumentStore)

    Parameters:
        document_store: The document_store instance to use.
    """

    def __init__(self, document_store: BaseDocumentStore):
        """Constructor."""

        framer = DataFramer()
        converter = DataFrameConverter()

        self.pipeline = Pipeline()
        self.pipeline.add_node(
            component=framer,
            name='DataFramer',
            inputs=['File'],
        )
        self.pipeline.add_node(
            component=converter,
            name='DataFrameConverter',
            inputs=['DataFramer'],
        )
        self.pipeline.add_node(
            component=document_store,
            name='DocumentStore',
            inputs=['DataFrameConverter'],
        )

    def run(
        self,
        file_paths: str,
        params: Optional[dict] = None,
        debug: Optional[bool] = None,
    ):
        """Runs the pipeline.

        Parameters:
            file_paths: The CSV file paths to convert and index.
            params: Params for the pipeline nodes.
            debug: Whether the pipeline should instruct nodes to collect debug
                information about their execution. By default these include the
                input parameters they received and the output they generated.
                All debug information can then be found in the dict returned
                by this method under the key "_debug".
        """

        return self.pipeline.run(
            file_paths=file_paths,
            params=params,
            debug=debug,
        )


class ZippedReviewIndexer(BaseStandardPipeline):
    """Pipeline for indexing and tagging zipped MAL reviews.

    Pipeline nodes are:
      - ZipLister (ZIPs -> zipped CSVs)
      - ZipDataFramer (zipped CSVs -> DataFrames)
      - DataFrameConverter (DataFrames -> Documents)
      - DocumentStore (Documents -> DocumentStore)

    Parameters:
        lister: The Zip file lister to use.
        document_store: The document_store instance to use.
    """

    def __init__(self, lister: ZipLister, document_store: BaseDocumentStore):
        """Constructor."""

        framer = ZipDataFramer()
        converter = DataFrameConverter()

        self.pipeline = Pipeline()
        self.pipeline.add_node(
            component=lister,
            name='ZipLister',
            inputs=['File'],
        )
        self.pipeline.add_node(
            component=framer,
            name='ZipDataFramer',
            inputs=['ZipLister'],
        )
        self.pipeline.add_node(
            component=converter,
            name='DataFrameConverter',
            inputs=['ZipDataFramer'],
        )
        self.pipeline.add_node(
            component=document_store,
            name='DocumentStore',
            inputs=['DataFrameConverter'],
        )

    def run(
        self,
        file_paths: str,
        params: Optional[dict] = None,
        debug: Optional[bool] = None,
    ):
        """Runs the pipeline.

        Parameters:
            file_paths: The CSV file paths to convert and index.
            params: Params for the pipeline nodes.
            debug: Whether the pipeline should instruct nodes to collect debug
                information about their execution. By default these include the
                input parameters they received and the output they generated.
                All debug information can then be found in the dict returned
                by this method under the key "_debug".
        """

        return self.pipeline.run(
            file_paths=file_paths,
            params=params,
            debug=debug,
        )
