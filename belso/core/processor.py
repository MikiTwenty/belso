# belso.core.processor

from typing import Any, Dict, Type, Union, Optional

from pydantic import BaseModel

from belso.core.schema import Schema
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
    schema_to_json,
    json_to_schema,
    schema_to_xml,
    xml_to_schema
)
from belso.utils import PROVIDERS, get_logger

# Get a module-specific logger
logger = get_logger(__name__)

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
        logger.debug("Delegating schema format detection...")
        format_type = detect_schema_format(schema)
        logger.info(f"Detected schema format: {format_type}.")
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
        - `to` (`str`): the target format. Can be a string or a `belso.utils.PROVIDERS` attribute.
        - `from_format` (`Optional[str]`): optional format hint for the input schema. If `None`, the format will be auto-detected. Defaults to `None`.\n
        ---
        ### Returns
        - `Dict[str, Any]` | `Type[pydantic.BaseModel]` | `str`: the converted schema.
        """
        try:
            logger.debug(f"Starting schema translation to '{to}' format...")

            # Detect input format if not specified
            if from_format is None:
                logger.debug("No source format specified, auto-detecting...")
                from_format = detect_schema_format(schema)
                logger.info(f"Auto-detected source format: '{from_format}'.")
            else:
                logger.debug(f"Using provided source format: '{from_format}'.")

            # Convert to our internal format if needed
            if from_format != PROVIDERS.BELSO:
                logger.debug(f"Converting from '{from_format}' to internal belso format...")
                belso_schema = SchemaProcessor.standardize(schema, from_format)
                logger.info("Successfully converted to belso format.")
            else:
                logger.debug("Schema is already in belso format, no conversion needed.")
                belso_schema = schema

            # Validate the schema before translation
            if not SchemaProcessor.is_valid_schema(belso_schema):
                logger.warning("Schema validation failed before translation.")
                # You might want to decide whether to continue or raise an exception

            # Translate to target format
            logger.debug(f"Translating from belso format to '{to}' format...")
            if to == PROVIDERS.GOOGLE:
                result = to_google(belso_schema)
            elif to == PROVIDERS.OLLAMA:
                result = to_ollama(belso_schema)
            elif to == PROVIDERS.OPENAI:
                result = to_openai(belso_schema)
            elif to == PROVIDERS.ANTHROPIC:
                result = to_anthropic(belso_schema)
            elif to == PROVIDERS.LANGCHAIN:
                result = to_langchain(belso_schema)
            elif to == PROVIDERS.HUGGINGFACE:
                result = to_huggingface(belso_schema)
            elif to == PROVIDERS.MISTRAL:
                result = to_mistral(belso_schema)
            elif to == PROVIDERS.JSON:
                result = schema_to_json(belso_schema)
            elif to == PROVIDERS.XML:
                result = schema_to_xml(belso_schema)
            else:
                logger.error(f"Unsupported target format: '{to}'.")
                raise ValueError(f"Provider {to} not supported.")

            logger.info(f"Successfully translated schema to '{to}' format.")
            return result

        except Exception as e:
            logger.error(f"Error during schema translation: {e}")
            logger.debug("Translation error details", exc_info=True)
            raise

    @staticmethod
    def standardize(
            schema: Any,
            from_format: str
        ) -> Type[Schema]:
        """
        Convert a schema from a specific format to our internal belso format.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to convert.
        - `from_format` (`str`): the format of the input schema (`"google"`, `"ollama"`, `"openai"`, `"anthropic"`, `"json"`, `"xml"`).\n
        ---
        ### Returns
        - `Type[belso.Schema]`: the converted belso schema.
        """
        try:
            logger.debug(f"Standardizing schema from '{from_format}' format to belso format...")

            if from_format == "google":
                logger.debug("Converting from Google format...")
                result = from_google(schema)
            elif from_format == "ollama":
                logger.debug("Converting from Ollama format...")
                result = from_ollama(schema)
            elif from_format == "openai":
                logger.debug("Converting from OpenAI format...")
                result = from_openai(schema)
            elif from_format == "anthropic":
                logger.debug("Converting from Anthropic format...")
                result = from_anthropic(schema)
            elif from_format == "langchain":
                logger.debug("Converting from Langchain format...")
                result = from_langchain(schema)
            elif from_format == "huggingface":
                logger.debug("Converting from Hugging Face format...")
                result = from_huggingface(schema)
            elif from_format == "mistral":
                logger.debug("Converting from Mistral format...")
                result = from_mistral(schema)
            elif from_format == "json":
                logger.debug("Converting from JSON format...")
                result = json_to_schema(schema)
            elif from_format == "xml":
                logger.debug("Converting from XML format...")
                result = xml_to_schema(schema)
            else:
                logger.error(f"Unsupported source format: '{from_format}'")
                raise ValueError(f"Conversion from {from_format} format is not supported.")

            logger.info(f"Successfully standardized schema to belso format.")
            return result

        except Exception as e:
            logger.error(f"Error during schema standardization: {e}")
            logger.debug("Standardization error details", exc_info=True)
            raise

    # Serialization methods
    @staticmethod
    def to_json(
            schema: Type,
            file_path: Optional[str] = None
        ) -> Dict[str, Any]:
        """
        Convert a schema to standardized JSON format and optionally save to a file.\n
        ---
        ### Args
        - `schema` (`Type`): the schema to convert.\n
        - `file_path` (`Optional[str]`): optional path to save the JSON to a file.\n
        ---
        ### Returns
        - `Dict[str, Any]`: the converted schema.
        """
        try:
            logger.debug("Converting schema to JSON format...")

            # First ensure we have a belso schema
            format_type = SchemaProcessor.detect_format(schema)
            if format_type != "belso":
                logger.debug(f"Schema is in '{format_type}' format, converting to belso format first...")
                belso_schema = SchemaProcessor.standardize(schema, format_type)
                logger.info("Successfully converted to belso format.")
            else:
                logger.debug("Schema is already in belso format, no conversion needed.")
                belso_schema = schema

            # Save path info for logging
            path_info = f" and saving to '{file_path}'" if file_path else ""
            logger.debug(f"Converting belso schema to JSON{path_info}...")

            result = schema_to_json(belso_schema, file_path)
            logger.info("Successfully converted belso schema to JSON format.")
            return result

        except Exception as e:
            logger.error(f"Error during schema to JSON conversion: {e}")
            logger.debug("JSON conversion error details", exc_info=True)
            raise

    @staticmethod
    def from_json(json_input: Union[Dict[str, Any], str]) -> Type[Schema]:
        """
        Convert JSON data or a JSON file to a belso schema.\n
        ---
        ### Args
        - `json_input` (`Union[Dict[str, Any], str]`): either a JSON dictionary or a file path to a JSON file.\n
        ---
        ### Returns
        - `Type[belso.Schema]`: the converted belso schema.
        """
        try:
            # Log different message based on input type
            if isinstance(json_input, str):
                logger.debug(f"Converting JSON from file '{json_input}' to belso schema...")
            else:
                logger.debug("Converting JSON dictionary to belso schema...")

            result = json_to_schema(json_input)
            logger.info("Successfully converted JSON to belso schema.")
            return result

        except Exception as e:
            logger.error(f"Error during JSON to schema conversion: {e}")
            logger.debug("JSON conversion error details", exc_info=True)
            raise

    @staticmethod
    def to_xml(
            schema: Type,
            file_path: Optional[str] = None
        ) -> str:
        """
        Convert a schema to XML format and optionally save to a file.\n
        ---
        ### Args
        - `schema` (`Type[belso.Schema]`): the schema to convert.\n
        - `file_path` (`Optional[str]`): optional path to save the XML to a file.\n
        ---
        ### Returns
        - `str`: the converted schema.
        """
        try:
            logger.debug("Converting schema to XML format...")

            # First ensure we have a belso schema
            format_type = SchemaProcessor.detect_format(schema)
            if format_type != "belso":
                logger.debug(f"Schema is in '{format_type}' format, converting to belso format first...")
                belso_schema = SchemaProcessor.standardize(schema, format_type)
                logger.info("Successfully converted to belso format.")
            else:
                logger.debug("Schema is already in belso format, no conversion needed.")
                belso_schema = schema

            # Save path info for logging
            path_info = f" and saving to '{file_path}'" if file_path else ""
            logger.debug(f"Converting belso schema to XML{path_info}...")

            result = schema_to_xml(belso_schema, file_path)
            logger.info("Successfully converted belso schema to XML format.")
            return result

        except Exception as e:
            logger.error(f"Error during schema to XML conversion: {e}")
            logger.debug("XML conversion error details", exc_info=True)
            raise

    @staticmethod
    def from_xml(xml_input: Union[str, Any]) -> Type[Schema]:
        """
        Convert XML data or an XML file to a belso schema.\n
        ---
        ### Args
        - `xml_input` (`Union[str, Any]`): either an XML string, Element, or a file path to an XML file.\n
        ---
        ### Returns
        - `Type[belso.Schema]`: the converted belso schema.
        """
        try:
            # Log different message based on input type
            if isinstance(xml_input, str):
                if xml_input.strip().startswith("<"):
                    logger.debug("Converting XML string to belso schema...")
                else:
                    logger.debug(f"Converting XML from file '{xml_input}' to belso schema...")
            else:
                logger.debug("Converting XML Element to belso schema...")

            result = xml_to_schema(xml_input)
            logger.info("Successfully converted XML to belso schema.")
            return result

        except Exception as e:
            logger.error(f"Error during XML to schema conversion: {e}")
            logger.debug("XML conversion error details", exc_info=True)
            raise

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
            logger.debug(f"Starting validation against schema '{schema_name}'...")

            # Convert string to dict if needed
            if isinstance(data, str):
                logger.debug("Input data is a string, attempting to parse as JSON...")
                try:
                    data = json.loads(data)
                    logger.debug("Successfully parsed JSON string.")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON string: {e}")
                    logger.debug("JSON parsing error details", exc_info=True)
                    raise ValueError("Invalid JSON string provided")

            # Get required fields
            required_fields = schema.get_required_fields()
            logger.debug(f"Schema has {len(required_fields)} required fields: {', '.join(required_fields)}")

            # Check required fields
            logger.debug("Checking for required fields...")
            for field_name in required_fields:
                if field_name not in data:
                    logger.error(f"Missing required field: '{field_name}'.")
                    raise ValueError(f"Missing required field: {field_name}.")
            logger.debug("All required fields are present.")

            # Validate field types
            logger.debug("Validating field types...")
            for field in schema.fields:
                if field.name in data:
                    value = data[field.name]
                    field_type = field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_)

                    # Skip None values for non-required fields
                    if value is None and not field.required:
                        logger.debug(f"BaseField '{field.name}' has None value, which is allowed for optional fields.")
                        continue

                    # Log the field being validated
                    logger.debug(f"Validating field '{field.name}' with value '{value}' against type '{field_type}'...")

                    # Type validation
                    if not isinstance(value, field.type_):
                        # Special case for int/float compatibility
                        if field.type_ == float and isinstance(value, int):
                            logger.debug(f"Converting integer value {value} to float for field '{field.name}'...")
                            data[field.name] = float(value)
                        else:
                            value_type = type(value).__name__
                            logger.error(f"Type mismatch for field '{field.name}': expected '{field_type}', got '{value_type}'.")
                            raise TypeError(f"BaseField '{field.name}' expected type {field_type}, got {value_type}.")
                    else:
                        logger.debug(f"BaseField '{field.name}' passed type validation.")

            logger.debug("All fields passed validation.")
            return data

        except Exception as e:
            if not isinstance(e, (ValueError, TypeError)):
                # Only log unexpected errors, as ValueError and TypeError are already logged
                logger.error(f"Unexpected error during validation: {e}")
                logger.debug("Validation error details", exc_info=True)
            raise

    @staticmethod
    def is_valid_schema(schema: Any) -> bool:
        """
        Check if a schema is valid.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to validate.\n
        ---
        ### Returns
        - `bool`: True if the schema is valid, False otherwise.
        """
        try:
            # Implement schema validation logic here
            # This would be migrated from the Validator class
            return True
        except Exception as e:
            logger.error(f"Schema validation error: {e}")
            return False
