# belso.utils.detecting

from typing import Any
import xml.etree.ElementTree as ET

from pydantic import BaseModel
from google.ai.generativelanguage_v1beta.types import content

from belso.utils import get_logger

# Get a module-specific _logger
_logger = get_logger(__name__)

def detect_schema_format(schema: Any) -> str:
    """
    Detect the format of the input schema.\n
    ---
    ### Args
    - `schema` (`Any`): the schema to detect.\n
    ---
    ### Returns
    - `str`: the detected format.
    """
    _logger.debug("Detecting schema format...")

    try:
        # Import Schema locally to avoid circular imports
        from belso.core import Schema

        # Check if it's our custom Schema format
        if isinstance(schema, type) and issubclass(schema, Schema):
            _logger.debug("Detected belso schema format.")
            return "belso"

        # Check if it's a Google Gemini schema
        if isinstance(schema, content.Schema):
            _logger.debug("Detected Google Gemini schema format.")
            return "google"

        # Check if it's a Pydantic model (OpenAI)
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            _logger.debug("Detected OpenAI (Pydantic) schema format.")
            return "openai"

        # Check if it's an XML Element
        if isinstance(schema, ET.Element):
            _logger.debug("Detected XML Element schema format.")
            return "xml"

        # Check if it's a string (could be XML or a file path)
        if isinstance(schema, str):
            # Check if it looks like XML
            if schema.strip().startswith("<") and schema.strip().endswith(">"):
                _logger.debug("Detected XML string schema format.")
                return "xml"
            _logger.debug("String input detected, but not recognized as XML. Might be a file path.")

        # Check if it's a JSON Schema-based format (Anthropic, Ollama, Mistral, etc.)
        if isinstance(schema, dict):
            # Check for Anthropic-style $schema
            if "$schema" in schema and "json-schema.org" in schema["$schema"]:
                _logger.debug("Detected JSON Schema format (Anthropic/Mistral).")
                return "anthropic"

            # Check for Ollama-like structure
            if "type" in schema and schema["type"] == "object" and "properties" in schema:
                if "title" in schema:
                    _logger.debug("Detected LangChain schema format.")
                    return "langchain"
                elif "format" in schema and schema["format"] == "huggingface":
                    _logger.debug("Detected Hugging Face schema format.")
                    return "huggingface"
                else:
                    _logger.debug("Detected Ollama schema format.")
                    return "ollama"

                _logger.warning("Unable to detect schema format. Returning 'unknown'.")
                return "unknown"

    except Exception as e:
        _logger.error(f"Error during schema format detection: {e}")
        _logger.debug("Detection error details", exc_info=True)
        return "unknown"
