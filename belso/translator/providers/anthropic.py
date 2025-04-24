# belso.translator.providers.anthropic

from typing import Any, Dict, Type

from belso.utils.logging import get_logger
from belso.schemas import Schema, BaseField
from belso.utils.schema_helpers import (
    map_json_to_python_type,
    build_properties_dict,
    create_fallback_schema
)

# Replace standard logger with our custom logger
logger = get_logger(__name__)

def to_anthropic(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Convert a belso schema to Anthropic Claude format.\n
    ---
    ### Args
    - `schema` (`Type[belso.Schema]`): the belso schema to convert.\n
    ---
    ### Returns
    - `Dict[str, Any]`: the converted schema.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting translation of schema '{schema_name}' to Anthropic format...")

        properties = build_properties_dict(schema)
        required_fields = schema.get_required_fields()

        logger.debug(f"Found {len(schema.fields)} fields, {len(required_fields)} required.")

        # Create the schema
        anthropic_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": properties,
            "required": required_fields
        }

        logger.debug("Successfully created Anthropic schema.")
        return anthropic_schema

    except Exception as e:
        logger.error(f"Error translating schema to Anthropic format: {e}")
        logger.debug("Translation error details", exc_info=True)
        return {}


def from_anthropic(schema: Dict[str, Any]) -> Type[Schema]:
    """
    Convert an Anthropic schema to belso format.\n
    ---
    ### Args
    - `schema` (`Dict[str, Any]`): the Anthropic schema to convert.\n
    ---
    ### Returns
    - `Type[belso.Schema]`: the converted belso schema.
    """
    try:
        logger.debug("Starting conversion from Anthropic schema to belso format...")

        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = "ConvertedFromAnthropic"
            fields = []

        # Extract properties
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        logger.debug(f"Found {len(properties)} properties, {len(required_fields)} required fields.")

        # Convert each property
        for name, prop in properties.items():
            prop_type = prop.get("type", "string")
            field_type = map_json_to_python_type(prop_type)
            description = prop.get("description", "")
            required = name in required_fields
            default = prop.get("default") if not required else None

            logger.debug(f"Converting property '{name}' of JSON Schema type '{prop_type}' to Python type '{field_type.__name__}'...")
            logger.debug(f"Property '{name}' is {'required' if required else 'optional'}.")

            if default is not None:
                logger.debug(f"Property '{name}' has default value: {default}.")

            ConvertedSchema.fields.append(
                BaseField(
                    name=name,
                    type_=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        logger.debug(f"Successfully converted Anthropic schema to belso schema with {len(ConvertedSchema.fields)} fields.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Anthropic schema to belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        return create_fallback_schema()
