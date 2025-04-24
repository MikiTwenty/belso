# belso.__init__

from belso.version import __version__
from belso.utils.logging import configure_logger, get_logger

# Initialize logger with default settings
configure_logger()

# Get the main logger for the package
logger = get_logger()
logger.info(f"belso v{__version__} initialized.")

# Import and expose main components
from belso.schemas import Schema, Field
from belso.validator import SchemaValidator
from belso.translator import SchemaTranslator

__all__ = [
    "__version__",
    "Field",
    "Schema",
    "SchemaValidator",
    "SchemaTranslator"
]
