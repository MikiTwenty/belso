from typing import Any, Dict, Type, Union

from belso.translator.utils import detect_schema_format
from belso.translator.providers import (
    to_google,
    to_ollama,
    to_openai,
    to_anthropic,
    from_google,
    from_ollama,
    from_openai,
    from_anthropic
)
from belso.translator.serialization import (
    schema_to_json,
    json_to_schema,
    schema_to_xml,
    xml_to_schema
)

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
        return detect_schema_format(schema)

    @staticmethod
    def translate(
            schema: Any,
            to: str,
            from_format: str = None
        ) -> Union[Dict[str, Any], Type, str]:
        """
        Translate a schema to a specific format.
        This method can automatically detect the input schema format and convert it
        to our internal format before translating to the target format.\n
        ---
        ### Args
        - `schema`: the schema to translate.\n
        - `to`: the target format (`"google"`, `"ollama"`, `"openai"`, `"anthropic"`, `"json"`, `"xml"`).\n
        - `from_format`: optional format hint for the input schema.
        If `None`, the format will be auto-detected.\n
        ---
        ### Returns
        - `Dict[str, Any]`: the translated schema in the target format.\n
        - `Type`: the translated schema as a pydantic model.\n
        - `str`: the translated schema as XML string.
        """
        # Detect input format if not specified
        if from_format is None:
            from_format = detect_schema_format(schema)

        # Convert to our internal format if needed
        if from_format != "belso":
            belso_schema = SchemaTranslator.standardize(schema, from_format)
        else:
            belso_schema = schema

        # Translate to target format
        if to == "google":
            return to_google(belso_schema)
        elif to == "ollama":
            return to_ollama(belso_schema)
        elif to == "openai":
            return to_openai(belso_schema)
        elif to == "anthropic":
            return to_anthropic(belso_schema)
        elif to == "json":
            return schema_to_json(belso_schema)
        elif to == "xml":
            return schema_to_xml(belso_schema)
        else:
            raise ValueError(f"Provider {to} not supported.")

    @staticmethod
    def standardize(
            schema: Any,
            from_format: str
        ) -> Type:
        """
        Convert a schema from a specific format to our internal Belso format.\n
        ---
        ### Args
        - `schema`: the schema to convert.\n
        - `from_format`: the format of the input schema (`"google"`, `"ollama"`, `"openai"`, `"anthropic"`, `"json"`, `"xml"`).\n
        ---
        ### Returns
        - `Type`: the converted schema as a Belso Schema subclass.
        """
        if from_format == "google":
            return from_google(schema)
        elif from_format == "ollama":
            return from_ollama(schema)
        elif from_format == "openai":
            return from_openai(schema)
        elif from_format == "anthropic":
            return from_anthropic(schema)
        elif from_format == "json":
            return json_to_schema(schema)
        elif from_format == "xml":
            return xml_to_schema(schema)
        else:
            raise ValueError(f"Conversion from {from_format} format is not supported.")

    @staticmethod
    def to_json(
            schema: Type,
            file_path: str = None
        ) -> Dict[str, Any]:
        """
        Convert a schema to standardized JSON format and optionally save to a file.\n
        ---
        ### Args
        - `schema`: the schema to convert.\n
        - `file_path`: optional path to save the JSON to a file.\n
        ---
        ### Returns
        - `Dict[str, Any]`: the schema in JSON format.
        """
        # First ensure we have a Belso schema
        format_type = SchemaTranslator.detect_format(schema)
        if format_type != "belso":
            belso_schema = SchemaTranslator.standardize(schema, format_type)
        else:
            belso_schema = schema

        return schema_to_json(belso_schema, file_path)

    @staticmethod
    def from_json(json_input: Union[Dict[str, Any], str]) -> Type:
        """
        Convert JSON data or a JSON file to a Belso schema.\n
        ---
        ### Args
        - `json_input`: either a JSON dictionary or a file path to a JSON file.\n
        ---
        ### Returns
        - `Type`: the converted schema as a Belso Schema subclass.
        """
        return json_to_schema(json_input)

    @staticmethod
    def to_xml(
            schema: Type,
            file_path: str = None
        ) -> str:
        """
        Convert a schema to XML format and optionally save to a file.\n
        ---
        ### Args
        - `schema`: the schema to convert.\n
        - `file_path`: optional path to save the XML to a file.\n
        ---
        ### Returns
        - `str`: the schema in XML format.
        """
        # First ensure we have a Belso schema
        format_type = SchemaTranslator.detect_format(schema)
        if format_type != "belso":
            belso_schema = SchemaTranslator.standardize(schema, format_type)
        else:
            belso_schema = schema

        return schema_to_xml(belso_schema, file_path)

    @staticmethod
    def from_xml(xml_input: Union[str, Any]) -> Type:
        """
        Convert XML data or an XML file to a Belso schema.\n
        ---
        ### Args
        - `xml_input`: either an XML string, Element, or a file path to an XML file.\n
        ---
        ### Returns
        - `Type`: the converted schema as a Belso Schema subclass.
        """
        return xml_to_schema(xml_input)
