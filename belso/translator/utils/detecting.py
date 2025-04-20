from typing import Any
import xml.etree.ElementTree as ET

from pydantic import BaseModel
from google.ai.generativelanguage_v1beta.types import content

from belso.translator.schemas import Schema

def detect_schema_format(schema: Any) -> str:
    """
    Detect the format of the input schema.\n
    ---
    ### Args
    - `schema`: the schema to detect.\n
    ---
    ### Returns
    - `str`: the detected format as a string.
    """
    # Check if it's our custom Schema format
    if isinstance(schema, type) and issubclass(schema, Schema):
        return "belso"

    # Check if it's a Google Gemini schema
    if isinstance(schema, content.Schema):
        return "google"

    # Check if it's a Pydantic model (OpenAI)
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        return "openai"

    # Check if it's an XML Element
    if isinstance(schema, ET.Element):
        return "xml"

    # Check if it's a string (could be XML or a file path)
    if isinstance(schema, str):
        # Check if it looks like XML
        if schema.strip().startswith("<") and schema.strip().endswith(">"):
            return "xml"

    # Check if it's an Anthropic or Ollama schema (JSON Schema)
    if isinstance(schema, dict):
        if "$schema" in schema and "http://json-schema.org" in schema["$schema"]:
            return "anthropic"
        elif "type" in schema and schema["type"] == "object" and "properties" in schema:
            # Basic check for Ollama schema
            return "ollama"
        elif "name" in schema and "fields" in schema and isinstance(schema["fields"], list):
            # Check for our JSON format
            return "json"

    return "unknown"
