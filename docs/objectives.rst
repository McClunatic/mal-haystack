.. _objectives:

Objectives
----------

MAL Haystack is designed and implemented with the high-level goal of
extracting various data from the Kaggle MAL Reviews dataset. There are
two high-level objectives:

1. Support for basic metadata extraction from non-review columns in the reviews
   dataset.
2. Support question answer (QA) extraction from reviews given targeted
   questions.

Further desired features include:

1. Ability to extract data directly from the single Kaggle dataset file, a
   ZIP file containing 3 datasets, one for details, one for recommendations,
   and one for reviews. That is: do not require the user to unzip the Kaggle ZIP
   file.
2. Options to let the user select which compressed CSV file to target for
   data extraction.
3. For basic metadata extraction, let the user to specify the metadata
   fields (CSV columns) to extract per record.
4. For QA extraction, let the user specify both the field (CSV column)
   to treat as the "document" to search, and the questions to answer.