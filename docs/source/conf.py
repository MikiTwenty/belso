import os
import sys

# Set path to the root of the project
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(os.path.abspath('./_ext'))

# Project information

project = 'belso'
copyright = '2025, Michele Ventimiglia'
author = 'Michele Ventimiglia'

# ✅ Import version from the package
try:
    from belso.version import __version__ as release
except ImportError:
    release = "unknown"

# General configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'custom_docstring',
    'myst_parser'
]

# Add this setting to prevent duplicate warnings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'imported-members': False,  # Don't document imported members
}

typehints_use_signature = False
typehints_use_rtype = False

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown"
}
