# Documentation Guide

## A guide for docs contributors

The `docs` directory contains the sphinx source text for DSPy docs, visit
https://dspy.readthedocs.io/ to read the full documentation.

This guide is made for anyone who's interested in running DSPy documentation locally,
making changes to it and make contributions. DSPy is made by the thriving community
behind it, and you're always welcome to make contributions to the project and the
documentation.

## Module Documentation

- [Evaluate Module](evaluate.md): Documentation for the `evaluate` module in the `dspy` folder.

## Build Docs

If you haven't already, clone the DSPy Github repo to a local directory:

```bash
git clone https://github.com/[DSPY_REPO_PATH].git && cd DSPy
```

Install all dependencies required for building docs (mainly `sphinx` and its extension):

- [Install poetry](https://python-poetry.org/docs/#installation) - this will help you manage package dependencies
- `poetry shell` - this command creates a virtual environment, which keeps installed packages contained to this project
- `poetry install --with docs` - this will install all dependencies needed for building docs


#### Watch Docs

Just run the following command from DSPy project's root directory:
```bash
make watch-docs
```

This will start a live-reloading server, which rebuilds the documentation and refreshes any open pages automatically when
changes are saved. Open your browser to http://0.0.0.0:8000/ to view the generated docs.

#### Build Docs Manually

```bash
cd docs
make html
```

The docs HTML files are now generated under `docs/_build/html` directory, you can preview
it locally with the following command:

```bash
python -m http.server 8000 -d _build/html
```

And open your browser at http://0.0.0.0:8000/ to view the generated docs.

