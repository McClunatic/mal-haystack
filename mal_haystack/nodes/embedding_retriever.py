"""Modifies the :class:`~haystack.nodes.retriever.EmbeddingRetriever` to
accept batch filters.

"""

from typing import Dict, List, Optional, Union

from haystack.nodes.retriever import EmbeddingRetriever as EmbeddingBase


class EmbeddingRetriever(EmbeddingBase):
    """Modified EmbeddingRetriever to accept `filters` in ``run`` and
    ``run_batch``.

    """

    def run(
        self,
        query: str,
        filters: Optional[Dict[str, Union[str, int, float, bool]]] = None,
        top_k: Optional[int] = None,
    ):
        """Runs the MALReader step in a pipeline.

        Arguments:
            query: The query to run.
            filters: Optional filters to narrow down the search space to
                documents whose metadata fulfill certain conditions.
            top_k: How many documents to return.
        """

        answers = self.retrieve(query=query, filters=filters, top_k=top_k)
        results = {"documents": answers}
        return results, "output_1"

    def run_batch(
        self,
        queries: List[str],
        filters: Optional[Dict[str, Union[str, int, float, bool]]] = None,
        top_k: Optional[int] = None,
    ):
        """Runs the MALReader step in a batch pipeline.

        Arguments:
            queries: The queries to run.
            filters: Optional filters to narrow down the search space to
                documents whose metadata fulfill certain conditions.
            top_k: How many documents to return per query.
        """
        answers = self.retrieve_batch(
            queries=queries,
            filters=filters,
            top_k=top_k,
        )
        results = {"documents": answers}
        return results, "output_1"
