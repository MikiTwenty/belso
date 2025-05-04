# belso.__init__

from belso.version import __version__
from belso.utils import configure_logger, get_logger

# Initialize logger with default settings
configure_logger()

# Get the main logger for the package
_logger = get_logger()
_logger.info(f"belso v{__version__} initialized.")

# Import and expose main components
from belso.core import SchemaProcessor, Schema, Field

__all__ = [
    "__version__",
    "SchemaProcessor",
    "Field",
    "Schema"
]
