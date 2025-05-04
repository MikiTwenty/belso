# belso.utils.logging

import os
import sys
import logging
from typing import Optional, Dict, Any

# Create a dedicated logger for the belso package
logger = logging.getLogger("belso")

# Store original logger level to restore it if needed
_original_level = logger.level

def get_logger(name:Optional[str]=None) -> logging.Logger:
    """
    Get a logger instance for a specific module within belso.\n
    ---
    ### Args
    - `name` (`str`): the name of the module (will be prefixed with 'belso.').\n
    ---
    ### Returns
    - `logging.Logger`: the logger instance.
    """
    if name:
        # Check if name already starts with "belso." to avoid duplication
        if name.startswith("belso."):
            return logging.getLogger(name)
        else:
            return logging.getLogger(f"belso.{name}")
    return logger

def configure_logger(
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        log_format: Optional[str] = None,
        propagate: bool = True,
        handler_config: Optional[Dict[str, Any]] = None
    ) -> None:
    """
    Configure the belso logger without affecting parent loggers.\n
    ---
    ### Args
    - `level` (`int`): the logging level. Defaults to `logging.INFO`.
    - `log_file` (`Optional[str]`): the path to the log file. Defaults to `None`.
    - `log_format` (`Optional[str]`): the log format. Defaults to `None`.
    - `propagate` (`bool`): whether to propagate logs to parent loggers. Defaults to `true`.
    - `handler_config` (`Optional[Dict[str, Any]]`): additional configuration for handlers. Defaults to `None`.
    """
    # Set propagation (whether logs should be passed to parent loggers)
    logger.propagate = propagate

    # Set level if provided
    if level is not None:
        logger.setLevel(level)

    # Default format if not specified
    if log_format is None:
        log_format = "[%(levelname)s][%(name)s] %(message)s"

    # Configure handlers based on what's requested
    if log_file or not logger.handlers:
        # Clear existing handlers if we're explicitly configuring
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Add console handler if no handlers exist or explicit config is requested
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level or logging.INFO)
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Add file handler if requested
        if log_file:
            try:
                os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(level or logging.INFO)
                file_formatter = logging.Formatter(log_format)
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            except (OSError, IOError) as e:
                # Don't fail if log file can't be created, just log a warning
                console_handler.setLevel(logging.WARNING)
                logger.warning(f"Could not create log file at {log_file}: {e}")

    # Apply any additional handler configuration
    if handler_config:
        for handler in logger.handlers:
            for key, value in handler_config.items():
                if hasattr(handler, key):
                    setattr(handler, key, value)

def disable_logging() -> None:
    """
    Temporarily disable belso logging.
    """
    global _original_level
    _original_level = logger.level
    logger.setLevel(logging.CRITICAL + 1)

def restore_logging() -> None:
    """
    Restore belso logging to its previous state.
    """
    logger.setLevel(_original_level)

def log_exception(
        e: Exception,
        message: str = "An error occurred"
    ) -> None:
    """
    Log an exception with consistent formatting.\n
    ---
    ### Args
    - `e` (`Exception`): the exception to log.
    - `message` (`str`): a message to accompany the exception.
    """
    logger.error(f"{message}: {str(e)}")
    logger.debug("Exception details", exc_info=True)
