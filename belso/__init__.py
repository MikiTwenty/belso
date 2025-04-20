from belso.utils.logging import configure_logger

# Initialize logger with default settings
# This won't override parent application loggers due to our implementation
configure_logger(propagate=True)

# Import and expose main components
from belso.translator import SchemaTranslator

__all__ = [
    "SchemaTranslator",
]
