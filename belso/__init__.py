import os
from belso.utils.logging import configure_logger, get_logger

# Initialize logger with default settings
configure_logger()

# Read version from VERSION file
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')) as f:
    __version__ = f.read().strip()

# Get the main logger for the package
logger = get_logger()
logger.info(f"Belso v{__version__} initialized.")

# Import and expose main components
from belso.translator import SchemaTranslator

__all__ = [
    "SchemaTranslator",
    "__version__",
]
