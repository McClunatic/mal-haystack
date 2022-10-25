.. _implementation:

Implementation
--------------

MAL Haystack implementation builds on Pandas and Haystack (see
:ref:`technologies`) in two ways:

1. Custom Haystack nodes (including those powered by Pandas)
2. Custom Haystack pipelines

Custom Haystack nodes
+++++++++++++++++++++

MAL Haystack includes custom nodes to meet some of the desires features
discussed in :ref:`objectives`. The custom nodes and their role in
meeting project objectives are discussed in the following subsections.

:class:`~mal_haystack.nodes.ZipLister`
**************************************

To allow users to accessed zipped CSV files, the
:class:`~mal_haystack.nodes.ZipLister` node performs the function
of extracting the *paths* to all files contained within a specified
ZIP file. For example, given a zip file :file:`spam.zip` containing
:file:`foo.csv` and :file:`bar.csv`, this node behaves as
illustrated below:

.. code-block:: python

   >>> from haystack import Pipeline
   >>> from mal_haystack import ZipLister
   >>> lister = ZipLister()
   >>> p = Pipeline()
   >>> p.add_node(component=lister, name='ZipLister', inputs=['File'])
   >>> p.run()
   ['foo.csv', 'bar.csv']

Custom Haystack pipelines
+++++++++++++++++++++++++

MAL Haystack's custom pipelines save users the trouble of manually
assembling indexing pipelines from MAL Haystack nodes for its most common
use cases. Those custom pipelines are discussed in the following subsections.

:class:`~mal_haystack.pipelines.ZippedReviewIndexer`
****************************************************

The :class:`~mal_haystack.pipelines.ZippedReviewIndexer` pipeline is
used to build a document store where the original source of document
data is one or more zipped CSV files.

The pipeline's nodes and flow are illustrated below.

.. mermaid::
   :caption: ZippedReviewIndexer pipeline flow diagram.

   graph TD;
   ZipLister-->ZipDataFramer;
   ZipDataFramer-->DataFrameConverter;
   DataFrameConverter-->DocumentStore;
