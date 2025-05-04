# belso.core.processor

from pathlib import Path
from typing import Any, Dict, Type, Union, Optional

import json
from pydantic import BaseModel

from belso.core.schema import Schema
from belso.tools import display_schema, validate_schema
from belso.utils import (
    detect_schema_format,
    FORMATS,
    get_logger
)
from belso.providers import (
    to_google, from_google,
    to_ollama, from_ollama,
    to_openai, from_openai,
    to_anthropic, from_anthropic,
    to_langchain, from_langchain,
    to_huggingface, from_huggingface,
    to_mistral, from_mistral
)
from belso.formats import (
    to_json, from_json,
    to_xml, from_xml,
    to_yaml, from_yaml
)

_logger = get_logger(__name__)

class SchemaProcessor:
    """
    A unified class for schema processing, including translation and validation.
    This class combines the functionality of the previous Translator and Validator classes.
    """
    @staticmethod
    def detect_format(schema: Any) -> str:
        """
        Detect the format of a schema.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to detect.\n
        ---
        ### Returns
        - `str`: the detected format as a string.
        """
        _logger.debug("Delegating schema format detection...")
        format_type = detect_schema_format(schema)
        _logger.info(f"Detected schema format: {format_type}.")
        return format_type

    @staticmethod
    def translate(
            schema: Any,
            to: str,
            from_format: Optional[str] = None
        ) -> Union[Dict[str, Any], Type[BaseModel], str]:
        """
        Translate a schema to a specific format.
        This method can automatically detect the input schema format and convert it
        to our internal format before translating to the target format.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to translate.
        - `to` (`str`): the target format. Can be a string or a `belso.utils.FORMATS` attribute.
        - `from_format` (`Optional[str]`): optional format hint for the input schema. If `None`, the format will be auto-detected. Defaults to `None`.\n
        ---
        ### Returns
        - `Dict[str, Any]` | `Type[pydantic.BaseModel]` | `str`: the converted schema.
        """
        try:
            _logger.debug(f"Starting schema translation to '{to}' format...")

            # Detect input format if not specified
            if from_format is None:
                _logger.debug("No source format specified, auto-detecting...")
                from_format = detect_schema_format(schema)
                _logger.info(f"Auto-detected source format: '{from_format}'.")
            else:
                _logger.debug(f"Using provided source format: '{from_format}'.")

            # Convert to our internal format if needed
            if from_format != FORMATS.BELSO:
                _logger.debug(f"Converting from '{from_format}' to internal 'belso' format...")
                belso_schema = SchemaProcessor.standardize(schema, from_format)
                _logger.debug(f"Successfully converted from '{from_format}' to 'belso' format.")
            else:
                _logger.debug("Schema is already in 'belso' format, no conversion needed.")
                belso_schema = schema

            # Translate to target format
            _logger.debug(f"Translating from belso format to '{to}' format...")
            if to == FORMATS.GOOGLE:
                result = to_google(belso_schema)
            elif to == FORMATS.OLLAMA:
                result = to_ollama(belso_schema)
            elif to == FORMATS.OPENAI:
                result = to_openai(belso_schema)
            elif to == FORMATS.ANTHROPIC:
                result = to_anthropic(belso_schema)
            elif to == FORMATS.LANGCHAIN:
                result = to_langchain(belso_schema)
            elif to == FORMATS.HUGGINGFACE:
                result = to_huggingface(belso_schema)
            elif to == FORMATS.MISTRAL:
                result = to_mistral(belso_schema)
            elif to == FORMATS.JSON:
                result = to_json(belso_schema)
            elif to == FORMATS.XML:
                result = to_xml(belso_schema)
            elif to == FORMATS.YAML:
                result = to_yaml(belso_schema)
            else:
                _logger.error(f"Unsupported target format: '{to}'.")
                raise ValueError(f"Provider {to} not supported.")

            _logger.info(f"Successfully translated schema to '{to}' format.")
            return result

        except Exception as e:
            _logger.error(f"Error during schema translation: {e}")
            _logger.debug("Translation error details", exc_info=True)
            raise

    @staticmethod
    def standardize(
            schema: Any,
            from_format: Optional[str] = None
        ) -> Type[Schema]:
        """
        Convert a schema from a specific format to our internal 'belso' format.
        If from_format is not specified, it will be auto-detected.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to convert.
        - `from_format` (`Optional[str]`): the format of the input schema. If `None`, the format will be auto-detected. Defaults to `None`.\n
        ---
        ### Returns
        - `Type[belso.Schema]`: the converted belso schema.
        """
        try:
            # Detect input format if not specified
            if from_format is None:
                _logger.debug("No source format specified, auto-detecting...")
                from_format = detect_schema_format(schema)
                _logger.info(f"Auto-detected source format: '{from_format}'.")
            else:
                _logger.debug(f"Using provided source format: '{from_format}'.")

            if from_format == FORMATS.BELSO:
                _logger.debug("Schema is already in 'belso' format, no conversion needed.")
                return schema

            _logger.debug(f"Standardizing schema from '{from_format}' format to 'belso' format...")

            if from_format == FORMATS.GOOGLE:
                _logger.debug("Converting from Google format...")
                result = from_google(schema)
            elif from_format == FORMATS.OLLAMA:
                _logger.debug("Converting from Ollama format...")
                result = from_ollama(schema)
            elif from_format == FORMATS.OPENAI:
                _logger.debug("Converting from OpenAI format...")
                result = from_openai(schema)
            elif from_format == FORMATS.ANTHROPIC:
                _logger.debug("Converting from Anthropic format...")
                result = from_anthropic(schema)
            elif from_format == FORMATS.LANGCHAIN:
                _logger.debug("Converting from Langchain format...")
                result = from_langchain(schema)
            elif from_format == FORMATS.HUGGINGFACE:
                _logger.debug("Converting from Hugging Face format...")
                result = from_huggingface(schema)
            elif from_format == FORMATS.MISTRAL:
                _logger.debug("Converting from Mistral format...")
                result = from_mistral(schema)
            elif from_format == FORMATS.JSON:
                _logger.debug("Converting from JSON format...")
                result = from_json(schema)
            elif from_format == FORMATS.XML:
                _logger.debug("Converting from XML format...")
                result = from_xml(schema)
            elif from_format == FORMATS.YAML:
                _logger.debug("Converting from YAML format...")
                result = from_yaml(schema)
            else:
                _logger.error(f"Unsupported source format: '{from_format}'")
                raise ValueError(f"Conversion from {from_format} format is not supported.")

            _logger.info(f"Successfully standardized schema to 'belso' format.")
            return result

        except Exception as e:
            _logger.error(f"Error during schema standardization: {e}")
            _logger.debug("Standardization error details", exc_info=True)
            raise

    @staticmethod
    def save(
            schema: Any,
            path: Union[str, Path]
        ) -> None:
        """
        Save a schema to a file in the specified format.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to save.
        - `path` (`Union[str, Path]`): the path to save the schema to.\n
        """
        from_format = detect_schema_format(schema)
        if from_format != FORMATS.BELSO:
            _logger.debug(f"Converting schema from '{from_format}' format to 'belso' format...")
            schema = SchemaProcessor.standardize(schema, from_format)
        if path.endswith(".json"):
            to_json(schema, path)
        elif path.endswith(".xml"):
            to_xml(schema, path)
        elif path.endswith(".yaml") or path.endswith(".yml"):
            to_yaml(schema, path)
        else:
            _logger.error(f"Unsupported format for saving: '{from_format}'")

    @staticmethod
    def load(path: Union[str, Path]) -> Any:
        """
        Load a schema from a file in the specified format.\n
        ---
        ### Args
        - `path` (`Union[str, Path]`): the path to the file to load.\n
        ---
        ### Returns
        - `Any`: the loaded schema.
        """
        if path.endswith(".json"):
            return from_json(path)
        elif path.endswith(".xml"):
            return from_xml(path)
        elif path.endswith(".yaml") or path.endswith(".yml"):
            return from_yaml(path)
        else:
            _logger.error(f"Unsupported file format for loading: '{path}'")

    @staticmethod
    def validate(
            data: Union[Dict[str, Any], str],
            schema: Type[Schema]
        ) -> Dict[str, Any]:
        """
        Validate that the provided data conforms to the given schema.\n
        ---
        ### Args
        - `data` (`Union[Dict[str, Any], str]`): the data to validate (either a dict or JSON string).
        - `schema` (`Type[belso.Schema]`): the schema to validate against.\n
        ---
        ### Returns:
        - `Dict[str, Any]`: the validated data.
        """
        return validate_schema(data, schema)

    @staticmethod
    def display(
            schema: Any,
            format_type: Optional[str] = None,
        ) -> None:
        """
        Pretty-print a schema using colors and better layout, including nested fields.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to print.
        - `format_type` (`Optional[str]`): format of the schema. Defaults to `None`.
        """
        if format_type is None:
            format_type = SchemaProcessor.detect_format(schema)
            _logger.debug(f"Auto-detected schema format: '{format_type}'.")

        if format_type != FORMATS.BELSO:
            _logger.debug(f"Converting from '{format_type}' to 'belso' format for printing...")
            belso_schema = SchemaProcessor.standardize(schema, format_type)
        else:
            belso_schema = schema

        display_schema(belso_schema)
