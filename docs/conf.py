project = 'DSPy'
author = 'Stanford University'
version = '0.1.0'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']

source_suffix = '.md'

master_doc = 'index'

pygments_style = 'sphinx'

html_theme = 'alabaster'
