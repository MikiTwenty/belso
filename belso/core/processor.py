# belso.core.processor

from pathlib import Path
from typing import Any, Dict, Type, Union, Optional

import json
from rich import box
from rich.table import Table
from pydantic import BaseModel
from rich.console import Console

from belso.core.schema import Schema
from belso.core.field import NestedField, ArrayField
from belso.utils import detect_schema_format
from belso.providers import (
    to_google,
    to_ollama,
    to_openai,
    to_anthropic,
    to_langchain,
    to_huggingface,
    to_mistral,
    from_google,
    from_ollama,
    from_openai,
    from_anthropic,
    from_langchain,
    from_huggingface,
    from_mistral
)
from belso.formats import (
    to_json,
    from_json,
    to_xml,
    from_xml,
    to_yaml,
    from_yaml,
)
from belso.utils import FORMATS, FORMATS, get_logger

# Get a module-specific logger
_logger = get_logger(__name__)

_console = Console()

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
                _logger.debug(f"Converting from '{from_format}' to internal belso format...")
                belso_schema = SchemaProcessor.standardize(schema, from_format)
                _logger.info("Successfully converted to belso format.")
            else:
                _logger.debug("Schema is already in belso format, no conversion needed.")
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
                result = to_json(belso_schema)           #  ←  **renamed**
            elif to == FORMATS.XML:
                result = to_xml(belso_schema)            #  ←  **renamed**
            elif to == FORMATS.YAML:
                result = to_yaml(belso_schema)           #  ←  **renamed**
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
        Convert a schema from a specific format to our internal belso format.
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
                _logger.debug("Schema is already in belso format, no conversion needed.")
                return schema

            _logger.debug(f"Standardizing schema from '{from_format}' format to belso format...")

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

            _logger.info(f"Successfully standardized schema to belso format.")
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
            _logger.debug(f"Converting schema from '{from_format}' format to belso format...")
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
        try:
            schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
            _logger.debug(f"Starting validation against schema '{schema_name}'...")

            # Convert string to dict if needed
            if isinstance(data, str):
                _logger.debug("Input data is a string, attempting to parse as JSON...")
                try:
                    data = json.loads(data)
                    _logger.debug("Successfully parsed JSON string.")
                except json.JSONDecodeError as e:
                    _logger.error(f"Failed to parse JSON string: {e}")
                    _logger.debug("JSON parsing error details", exc_info=True)
                    raise ValueError("Invalid JSON string provided")

            # Get required fields
            required_fields = schema.get_required_fields()
            _logger.debug(f"Schema has {len(required_fields)} required fields: {', '.join(required_fields)}")

            # Check required fields
            _logger.debug("Checking for required fields...")
            for field_name in required_fields:
                if field_name not in data:
                    _logger.error(f"Missing required field: '{field_name}'.")
                    raise ValueError(f"Missing required field: {field_name}.")
            _logger.debug("All required fields are present.")

            # Validate field types
            _logger.debug("Validating field types...")
            for field in schema.fields:
                if field.name in data:
                    value = data[field.name]
                    field_type = field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_)

                    # Skip None values for non-required fields
                    if value is None and not field.required:
                        _logger.debug(f"BaseField '{field.name}' has None value, which is allowed for optional fields.")
                        continue

                    # Log the field being validated
                    _logger.debug(f"Validating field '{field.name}' with value '{value}' against type '{field_type}'...")

                    # Type validation
                    if not isinstance(value, field.type_):
                        # Special case for int/float compatibility
                        if field.type_ == float and isinstance(value, int):
                            _logger.debug(f"Converting integer value {value} to float for field '{field.name}'...")
                            data[field.name] = float(value)
                        else:
                            value_type = type(value).__name__
                            _logger.error(f"Type mismatch for field '{field.name}': expected '{field_type}', got '{value_type}'.")
                            raise TypeError(f"BaseField '{field.name}' expected type {field_type}, got {value_type}.")
                    else:
                        _logger.debug(f"BaseField '{field.name}' passed type validation.")

            _logger.debug("All fields passed validation.")
            return data

        except Exception as e:
            if not isinstance(e, (ValueError, TypeError)):
                # Only log unexpected errors, as ValueError and TypeError are already logged
                _logger.error(f"Unexpected error during validation: {e}")
                _logger.debug("Validation error details", exc_info=True)
            raise

    @staticmethod
    def display(
            schema: Any,
            format_type: Optional[str] = None,
            depth: int = 0
        ) -> None:
        """
        Pretty-print a schema using colors and better layout, including nested fields.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to print.
        - `format_type` (`Optional[str]`): format of the schema. Defaults to `None`.
        - `depth` (`int`): indentation level for nested display.
        """
        try:
            if format_type is None:
                format_type = SchemaProcessor.detect_format(schema)
                _logger.debug(f"Auto-detected schema format: '{format_type}'.")

            if format_type != FORMATS.BELSO:
                _logger.debug(f"Converting from '{format_type}' to belso format for printing...")
                belso_schema = SchemaProcessor.standardize(schema, format_type)
            else:
                belso_schema = schema

            def display_schema(schema_cls: Type[Schema], indent: int = 0):
                table = Table(
                    title=f"\n[bold blue]Schema: {schema_cls.__name__}",
                    box=box.ROUNDED,
                    expand=False,
                    show_lines=True
                )

                table.add_column("Field", style="cyan", no_wrap=True)
                table.add_column("Type", style="magenta")
                table.add_column("Required", style="green")
                table.add_column("Default", style="yellow")
                table.add_column("Description", style="white")

                for field in schema_cls.fields:
                    required = "✅" if field.required else "❌"
                    default = str(field.default) if field.default is not None else "-"
                    description = field.description or "-"

                    # Nested field
                    if isinstance(field, NestedField):
                        nested_type = f"object ({field.schema.__name__})"
                        table.add_row(field.name, nested_type, required, default, description)
                    # Array of objects
                    elif isinstance(field, ArrayField) and hasattr(field, "items_type") and isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
                        array_type = f"array[{field.items_type.__name__}]"
                        table.add_row(field.name, array_type, required, default, description)
                    # Primitive
                    else:
                        field_type = field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_)
                        table.add_row(field.name, field_type, required, default, description)

                _console.print(table)

                # Recursive printing of nested fields
                for field in schema_cls.fields:
                    if isinstance(field, NestedField):
                        display_schema(field.schema, indent + 1)
                    elif isinstance(field, ArrayField) and hasattr(field, "items_type") and isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
                        display_schema(field.items_type, indent + 1)

            display_schema(belso_schema)

        except Exception as e:
            _logger.error(f"Error printing schema: {e}")
            _logger.debug("Schema printing error details", exc_info=True)
            _console.print(f"[bold red]Error printing schema: {e}")
