import dobby

project = "Dobby"
copyright = "2018, Simon Berger"
version = release = dobby.__version__

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon"
]

default_role = "any"

master_doc = "index"

intersphinx_mapping = {"python": ("https://docs.python.org/3.7", None)}
