# MAL-Haystack

This repo demonstrates the use of
[haystack](https://github.com/deepset-ai/haystack) against a
[MyAnimeList Kaggle dataset](https://www.kaggle.com/datasets/stoicstatic/mal-top-10k-anime-details).

## Environment setup

This guide assumes you have `conda` installed. First, create and activate
the `mal` environment:

```shell
conda create -n mal python=3.10
conda activate mal
```

Then, install `poetry`:

```shell
pip install poetry
```

Finally, install package dependencies using `poetry`:

```shell
poetry install
```

> NOTE: Because PyTorch is being installed from a secondary source, and
> because Poetry downloads and caches all packages from a source, expect
> to wait a long time to resolve the environment for the first time!
> See these [Instructions for installing PyTorch](https://github.com/python-poetry/poetry/issues/6409)
> to learn more.

## Dataset download

These instructions assume you have a Kaggle account. If not, please create one!
First, visit the Kaggle website and navigate to your account page. Under the
API section, click **Create API token**. It will download a `kaggle.json` file.
Save that token in a `.kaggle` directory in your home area.

Linux: `~/.kaggle/kaggle.json`
Windows: C:\Users\%USERNAME%\.kaggle\kaggle.json

Then, use the Kaggle CLI (made available once you've run `poetry install`)
to download the dataset:

```shell
cd data
kaggle datasets download stoicstatic/mal-top-10k-anime-details
```

## Example usage

Try running

```powershell
python -m mal_haystack Review "MAL Anime Reviews 85k.csv" \
    -z .\data\mal-top-10k-anime-details.zip \
    -m "Anime Title" -m "Anime URL" -m "Overall Rating" \
    -q "Who are the main characters?"
```
