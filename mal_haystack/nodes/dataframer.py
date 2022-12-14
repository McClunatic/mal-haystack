import pathlib
from typing import List, Optional

import pandas as pd
from haystack.nodes import BaseComponent


class DataFramer(BaseComponent):
    """Component for generating a set of dataframes from CSV files.

    Parameters:
        id_hash_keys: Generate the document id from a custom list of strings
            that refer to the document's attributes. If you want to ensure you
            don't have duplicate documents in your DocumentStore but texts are
            not unique, you can modify the metadata and pass e.g. `"meta"` to
            this field (e.g. [`"content"`, `"meta"`]). In this case the id will
            be generated by using the content and the defined metadata.
    """

    outgoing_edges: int = 1

    def __init__(
        self,
        id_hash_keys: Optional[List[str]] = None,
    ):
        """Constructor."""

        self.id_hash_keys = id_hash_keys

    def convert(
        self,
        file_paths: str | pathlib.Path,
        id_hash_keys: Optional[List[str]] = None,
    ):
        """Extract `file_paths` data as :class:`pandas.DataFrame` objects.

        .. note::

           The ``meta` dictionary must contain the `zip_path` key whose value
           indicates the location of the zip file containing `file_paths`!

        Arguments:
            file_paths: Path of the zipped CSV file.
            meta: Dictionary containing ``zip_paths`` key to zip file paths to
                extract CSV `file_paths` from.
            id_hash_keys: Generate the document id from a custom list of
                strings that refer to the document's attributes. If you want to
                ensure you don't have duplicate documents in your DocumentStore
                but texts are not unique, you can modify the metadata and pass
                e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]). In
                this case the id will be generated by using the content and the
                defined metadata.
        """

        if id_hash_keys is None:
            id_hash_keys = self.id_hash_keys

        dfs = []
        for file_path in file_paths:
            with open(file_path) as myfile:
                dfs.append(pd.read_csv(myfile))

        return dfs

    def run(
        self,
        file_paths: str | pathlib.Path,
        id_hash_keys: Optional[List[str]] = None,
    ):
        """Read CSV filenames into :class:`pandas.DataFrame` objects.

        Arguments:
            file_paths: Paths of the CSV files.
            id_hash_keys: Generate the document id from a custom list of
                strings that refer to the document's attributes. If you want to
                ensure you don't have duplicate documents in your DocumentStore
                but texts are not unique, you can modify the metadata and pass
                e.g. `"meta"` to this field (e.g. [`"content"`, `"meta"`]). In
                this case the id will be generated by using the content and the
                defined metadata.
        """

        # Convert paths into dataframes
        dfs = self.convert(
            file_paths,
            id_hash_keys=id_hash_keys,
        )

        result = {'dataframes': dfs}
        return result, 'output_1'

    run_batch = run
