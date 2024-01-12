import os
import sys

import sphinx

# Set the root path of the project
sys.path.insert(0, os.path.abspath('../'))

# Specify the path to the master document
master_doc = 'index'

# Set the project information
project = 'DSPy'
author = 'DSPy Team'
version = '3.2.1'

# Add the extensions that Sphinx should use
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.autodoc.typehints',
    'sphinx_rtd_theme',
    'sphinx.ext.mathjax',
    'm2r2',
    'myst_nb',
    'sphinxcontrib.autodoc_pydantic',
    'sphinx_reredirects',
    'sphinx_automodapi.automodapi',
]
source_suffix = ['.rst', '.md']

# automodapi requires this to avoid duplicates apparently
numpydoc_show_class_members = False

myst_heading_anchors = 5
# TODO: Fix the non-consecutive header level in our docs, until then
# disable the sphinx/myst warnings
suppress_warnings = ["myst.header"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_title = project + " " + version
html_static_path = ['_static']

html_css_files = [
    'css/custom.css',

]
# html_js_files = [
#     'js/mendablesearch.js',
#     (
#         'https://cdn.jsdelivr.net/npm/@docsearch/js@3.3.3/dist/umd/index.js',
#         {'defer': 'defer'},
#     ),
#     ('js/algolia.js', {'defer': 'defer'}),
# ]

nb_execution_mode = 'off'
autodoc_pydantic_model_show_json_error_strategy = 'coerce'
nitpicky = True

# If DSPy requires redirects, they should be defined here
# redirects = {}

