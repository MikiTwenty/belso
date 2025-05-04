# belso.utils.detecting

import json
from typing import Any

import yaml
from pydantic import BaseModel
import xml.etree.ElementTree as ET
from google.ai.generativelanguage_v1beta.types import content

from belso.utils.formats import FORMATS
from belso.utils.logging import get_logger

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

        # Direct object type checks
        if isinstance(schema, type) and issubclass(schema, Schema):
            _logger.debug("Detected belso schema format.")
            return FORMATS.BELSO

        if isinstance(schema, type) and issubclass(schema, BaseModel):
            _logger.debug("Detected OpenAI schema format (Pydantic).")
            return FORMATS.OPENAI

        if isinstance(schema, content.Schema):
            _logger.debug("Detected Google Gemini schema format.")
            return FORMATS.GOOGLE

        if isinstance(schema, ET.Element):
            _logger.debug("Detected XML ElementTree schema format.")
            return FORMATS.XML

        if isinstance(schema, dict):
            # Detect based on structure
            if "$schema" in schema and "json-schema.org" in schema["$schema"]:
                _logger.debug("Detected JSON Schema format (Anthropic or Mistral).")
                return FORMATS.ANTHROPIC
            if "type" in schema and schema["type"] == "object" and "properties" in schema:
                if "title" in schema:
                    _logger.debug("Detected LangChain schema format.")
                    return FORMATS.LANGCHAIN
                elif "format" in schema and schema["format"] == "huggingface":
                    _logger.debug("Detected Hugging Face schema format.")
                    return FORMATS.HUGGINGFACE
                else:
                    _logger.debug("Detected Ollama schema format.")
                    return FORMATS.OLLAMA
            _logger.debug("Generic JSON object detected, assuming JSON format.")
            return FORMATS.JSON

        if isinstance(schema, str):
            schema_str = schema.strip()
            # Quick detection: XML
            if schema_str.startswith("<") and schema_str.endswith(">"):
                _logger.debug("Detected XML string schema format.")
                return FORMATS.XML

            # Try parsing as JSON
            try:
                json.loads(schema_str)
                _logger.debug("Successfully parsed JSON string.")
                return FORMATS.JSON
            except json.JSONDecodeError:
                _logger.debug("String is not valid JSON.")

            # Try parsing as YAML
            try:
                parsed_yaml = yaml.safe_load(schema_str)
                if isinstance(parsed_yaml, dict):
                    _logger.debug("Successfully parsed YAML string.")
                    return FORMATS.YAML
            except yaml.YAMLError:
                _logger.debug("String is not valid YAML.")

            _logger.warning("String format could not be recognized.")
            return "unknown"

        _logger.warning("Input schema format could not be detected.")
        return "unknown"

    except Exception as e:
        _logger.error(f"Error during schema format detection: {e}")
        _logger.debug("Detection error details", exc_info=True)
        return "unknown"
