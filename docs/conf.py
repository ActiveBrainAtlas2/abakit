# See http://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "abakit"
author = "abakit developers"
copyright = f"2020, {author}"
version = "0.0.1"
release = "0.0.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib.apidoc",
    "m2r2",
]
source_suffix = [".md", ".rst"]
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"

# -- Options for extensions --------------------------------------------------

# sphinx.ext.autodoc
autodoc_member_order = "bysource"

# sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# sphinxcontrib.apidoc
apidoc_module_dir = "../src/abakit"
apidoc_output_dir = "api"
apidoc_excluded_paths = []
apidoc_separate_modules = True
apidoc_toc_file = False
apidoc_module_first = True
apidoc_extra_args = []
