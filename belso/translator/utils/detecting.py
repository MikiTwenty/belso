# belso.translator.utils.detecting

from typing import Any
import xml.etree.ElementTree as ET

from pydantic import BaseModel
from google.ai.generativelanguage_v1beta.types import content

from belso.schemas import Schema
from belso.utils.logging import get_logger

# Get a module-specific logger
logger = get_logger(__name__)

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
    logger.debug("Detecting schema format...")

    try:
        # Check if it's our custom Schema format
        if isinstance(schema, type) and issubclass(schema, Schema):
            logger.debug("Detected belso schema format.")
            return "belso"

        # Check if it's a Google Gemini schema
        if isinstance(schema, content.Schema):
            logger.debug("Detected Google Gemini schema format.")
            return "google"

        # Check if it's a Pydantic model (OpenAI)
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            logger.debug("Detected OpenAI (Pydantic) schema format.")
            return "openai"

        # Check if it's an XML Element
        if isinstance(schema, ET.Element):
            logger.debug("Detected XML Element schema format.")
            return "xml"

        # Check if it's a string (could be XML or a file path)
        if isinstance(schema, str):
            # Check if it looks like XML
            if schema.strip().startswith("<") and schema.strip().endswith(">"):
                logger.debug("Detected XML string schema format.")
                return "xml"
            logger.debug("String input detected, but not recognized as XML. Might be a file path.")

        # Check if it's a JSON Schema-based format (Anthropic, Ollama, Mistral, etc.)
        if isinstance(schema, dict):
            # Check for JSON Schema identifier
            if "$schema" in schema and "http://json-schema.org" in schema["$schema"]:
                # Differentiate between providers that use JSON Schema
                if "title" in schema and isinstance(schema["title"], str):
                    logger.debug("Detected LangChain schema format.")
                    return "langchain"
                else:
                    # Both Anthropic and Mistral use JSON Schema, try to differentiate
                    # This is a simplistic approach - in practice you might need more specific checks
                    logger.debug("Detected JSON Schema format (Anthropic/Mistral).")
                    return "anthropic"  # Default to Anthropic if can't differentiate
            elif "type" in schema and schema["type"] == "object" and "properties" in schema:
                # Basic check for Ollama/Hugging Face schema
                if "title" in schema:
                    logger.debug("Detected LangChain schema format.")
                    return "langchain"
                elif "format" in schema and schema["format"] == "huggingface":
                    logger.debug("Detected Hugging Face schema format.")
                    return "huggingface"
                else:
                    logger.debug("Detected Ollama schema format.")
                    return "ollama"
            elif "name" in schema and "fields" in schema and isinstance(schema["fields"], list):
                # Check for our JSON format
                logger.debug("Detected belso JSON schema format.")
                return "json"
            logger.debug("Dictionary input detected, but not recognized as a known schema format.")

        logger.warning("Unable to detect schema format. Returning 'unknown'.")
        return "unknown"

    except Exception as e:
        logger.error(f"Error during schema format detection: {e}")
        logger.debug("Detection error details", exc_info=True)
        return "unknown"
