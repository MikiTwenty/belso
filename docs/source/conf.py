# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(os.path.abspath('./_ext'))  # Add the _ext directory to the path

project = 'belso'
copyright = '2025, Michele Ventimiglia'
author = 'Michele Ventimiglia'

# Read version directly from VERSION file
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'VERSION')) as f:
    release = f.read().strip()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'custom_docstring',  # Your custom extension
]

# Configure napoleon extension to handle your custom format
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
