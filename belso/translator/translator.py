from typing import Any, Dict, Type, Union, Optional

from belso.translator.utils import detect_schema_format
from belso.translator.providers import (
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
from belso.translator.serialization import (
    schema_to_json,
    json_to_schema,
    schema_to_xml,
    xml_to_schema
)
from belso.utils import PROVIDERS
from belso.utils.logging import get_logger
from belso.utils.schema_helpers import (
    is_schema_supported,
    create_fallback_schema
)

# Get a module-specific logger
logger = get_logger(__name__)

class SchemaTranslator:
    @staticmethod
    def detect_format(schema: Any) -> str:
        """
        Detect the format of a schema.\n
        ---
        ### Args
        - `schema`: the schema to detect.\n
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
        ) -> Union[Dict[str, Any], Type, str]:
        """
        Translate a schema to a specific format.
        This method can automatically detect the input schema format and convert it
        to our internal format before translating to the target format.\n
        ---
        ### Args
        - `schema` (`Any`): the schema to translate.
        - `to` (`str`): the target format. Can be a string or a `belso.utils.PROVIDERS` attribute.
        - `from_format` (`Optional[str]`): optional format hint for the input schema, if `None`, the format will be auto-detected.\n
        ---
        ### Returns
        - `Union[Dict[str, Any], Type, str]`: the translated schema in the target format.
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
                belso_schema = SchemaTranslator.standardize(schema, from_format)
                logger.info("Successfully converted to belso format.")
            else:
                logger.debug("Schema is already in belso format, no conversion needed.")
                belso_schema = schema

            if not is_schema_supported(belso_schema, to):
                return create_fallback_schema(belso_schema)

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
        ) -> Type:
        """
        Convert a schema from a specific format to our internal belso format.\n
        ---
        ### Args
        - `schema`: the schema to convert.
        - `from_format`: the format of the input schema (`"google"`, `"ollama"`, `"openai"`, `"anthropic"`, `"json"`, `"xml"`).\n
        ---
        ### Returns
        - `Type`: the converted schema as a belso Schema subclass.
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
        - `Dict[str, Any]`: the schema in JSON format.
        """
        try:
            logger.debug("Converting schema to JSON format...")

            # First ensure we have a belso schema
            format_type = SchemaTranslator.detect_format(schema)
            if format_type != "belso":
                logger.debug(f"Schema is in '{format_type}' format, converting to belso format first...")
                belso_schema = SchemaTranslator.standardize(schema, format_type)
                logger.info("Successfully converted JSON to belso format.")
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
    def from_json(json_input: Union[Dict[str, Any], str]) -> Type:
        """
        Convert JSON data or a JSON file to a belso schema.\n
        ---
        ### Args
        - `json_input` (`Union[Dict[str, Any], str]`): either a JSON dictionary or a file path to a JSON file.\n
        ---
        ### Returns
        - `Type`: the converted schema as a belso Schema subclass.
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
        - `schema` (`Type`): the schema to convert.\n
        - `file_path` (`Optional[str]`): optional path to save the XML to a file.\n
        ---
        ### Returns
        - `str`: the schema in XML format.
        """
        try:
            logger.debug("Converting schema to XML format...")

            # First ensure we have a belso schema
            format_type = SchemaTranslator.detect_format(schema)
            if format_type != "belso":
                logger.debug(f"Schema is in '{format_type}' format, converting to belso format first...")
                belso_schema = SchemaTranslator.standardize(schema, format_type)
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
    def from_xml(xml_input: Union[str, Any]) -> Type:
        """
        Convert XML data or an XML file to a belso schema.\n
        ---
        ### Args
        - `xml_input` (`Union[str, Any]`): either an XML string, Element, or a file path to an XML file.\n
        ---
        ### Returns
        - `Type`: the converted schema as a belso Schema subclass.
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
