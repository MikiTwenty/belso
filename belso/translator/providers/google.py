from typing import Any, Type

from google.ai.generativelanguage_v1beta.types import content

from belso.schemas import Schema, Field
from belso.utils.logging import get_logger
from belso.utils.schema_helpers import create_fallback_schema

logger = get_logger(__name__)

def to_google(schema: Type[Schema]) -> content.Schema:
    """
    Translate a standard schema to Google Gemini format.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`) : the Belso schema to translate.\n
    ---
    ### Returns
    - `content.Schema`: a Google Gemini schema in dict format for use in the API.
    """
    try:
        logger.debug(f"Starting translation of schema '{schema.__name__ if hasattr(schema, '__name__') else 'unnamed'}' to Google format...")

        # Type mapping for Gemini
        type_mapping = {
            list: content.Type.ARRAY,
            bool: content.Type.BOOLEAN,
            str: content.Type.STRING,
            float: content.Type.NUMBER,
            int: content.Type.INTEGER,
            dict: content.Type.OBJECT,
            Any: content.Type.TYPE_UNSPECIFIED,
        }

        properties = {}
        required_fields = schema.get_required_fields()

        logger.debug(f"Found {len(schema.fields)} fields, {len(required_fields)} required.")

        # Build properties for each field
        for field in schema.fields:
            field_type = type_mapping.get(field.type, content.Type.TYPE_UNSPECIFIED)
            logger.debug(f"Mapping field '{field.name}' of type '{field.type.__name__}' to Google type '{field_type}'...")

            properties[field.name] = content.Schema(
                type=field_type,
                description=field.description
            )

        # Create the schema
        gemini_schema = content.Schema(
            type=content.Type.OBJECT,
            properties=properties,
            required=required_fields
        )

        logger.debug("Successfully created Google schema.")
        return gemini_schema

    except Exception as e:
        logger.error(f"Error translating schema to Gemini format: {e}")
        logger.debug("Translation error details", exc_info=True)
        return {}

def from_google(schema: content.Schema) -> Type[Schema]:
    """
    Convert a Google Gemini schema to Belso Schema format.\n
    ---
    ### Args
    - `schema` (`content.Schema`) : the Google Gemini schema to convert.\n
    ---
    ### Returns
    - `Type[Schema]`: a standard schema.
    """
    try:
        logger.debug("Starting conversion from Google schema to Belso format...")

        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = "ConvertedFromGoogle"
            fields = []

        # Type mapping from Google to Python
        reverse_type_mapping = {
            content.Type.ARRAY: list,
            content.Type.BOOLEAN: bool,
            content.Type.STRING: str,
            content.Type.NUMBER: float,
            content.Type.INTEGER: int,
            content.Type.OBJECT: dict,
            content.Type.TYPE_UNSPECIFIED: Any,
        }

        # Extract properties
        properties = schema.properties if hasattr(schema, "properties") else {}
        required_fields = schema.required if hasattr(schema, "required") else []

        logger.debug(f"Found {len(properties)} properties, {len(required_fields)} required fields.")

        # Convert each property
        for name, prop in properties.items():
            field_type = reverse_type_mapping.get(prop.type, str)
            description = prop.description if hasattr(prop, "description") else ""
            required = name in required_fields

            logger.debug(f"Converting property '{name}' of Google type '{prop.type}' to Python type '{field_type.__name__}'...")

            ConvertedSchema.fields.append(
                Field(
                    name=name,
                    type=field_type,
                    description=description,
                    required=required
                )
            )

        logger.debug(f"Successfully converted Google schema to Belso schema with {len(ConvertedSchema.fields)} fields.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Google schema to Belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        return create_fallback_schema()
