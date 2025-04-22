import os
import sys

# Set path to the root of the project
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(os.path.abspath('./_ext'))

# -- Project information -----------------------------------------------------

project = 'belso'
copyright = '2025, Michele Ventimiglia'
author = 'Michele Ventimiglia'

# ✅ Import version from the package
try:
    from belso.version import __version__ as release
except ImportError:
    release = "unknown"

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'custom_docstring'
]

# Napoleon configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
