import logging
from typing import Any, Type

from google.ai.generativelanguage_v1beta.types import content

from belso.translator.schemas import Schema, Field

logger = logging.getLogger(__name__)

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

        # Build properties for each field
        for field in schema.fields:
            field_type = type_mapping.get(field.type, content.Type.TYPE_UNSPECIFIED)
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

        return gemini_schema

    except Exception as e:
        logger.error(f"Error translating schema to Gemini format: {e}")
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

        # Convert each property
        for name, prop in properties.items():
            field_type = reverse_type_mapping.get(prop.type, str)
            description = prop.description if hasattr(prop, "description") else ""
            required = name in required_fields

            ConvertedSchema.fields.append(
                Field(
                    name=name,
                    type=field_type,
                    description=description,
                    required=required
                )
            )

        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Google schema to Belso format: {e}")
        # Return a minimal schema if conversion fails
        class FallbackSchema(Schema):
            name = "FallbackSchema"
            fields = [Field(name="text", type=str, description="Fallback field", required=True)]
        return FallbackSchema
