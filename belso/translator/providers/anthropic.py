import logging
from typing import Any, Dict, Type

from belso.translator.schemas import Schema

logger = logging.getLogger(__name__)

def to_anthropic(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Translate a standard schema to Anthropic Claude format.
    Anthropic Claude uses a JSON schema format similar to OpenAPI.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the schema to convert.\n
    ---
    ### Returns
    - `Dict[str, Any]`: the converted schema.
    """
    try:
        properties = {}
        required_fields = schema.get_required_fields()

        # Build properties for each field
        for field in schema.fields:
            # Map Python types to JSON Schema types
            if field.type == str:
                field_type = "string"
            elif field.type == int:
                field_type = "integer"
            elif field.type == float:
                field_type = "number"
            elif field.type == bool:
                field_type = "boolean"
            elif field.type == list:
                field_type = "array"
            elif field.type == dict:
                field_type = "object"
            else:
                field_type = "string"  # Default to string for unknown types

            properties[field.name] = {
                "type": field_type,
                "description": field.description
            }

            # Add default value if provided
            if not field.required and field.default is not None:
                properties[field.name]["default"] = field.default

        # Create the schema
        anthropic_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": properties,
            "required": required_fields
        }

        return anthropic_schema

    except Exception as e:
        logger.error(f"Error translating schema to Anthropic format: {e}")
        return {}


def from_anthropic(schema: Dict[str, Any]) -> Type[Schema]:
    """
    Convert an Anthropic schema to Belso Schema format.\n
    ---
    ### Args
    - `schema` (`Dict[str, Any]`): the Anthropic schema to convert.\n
    ---
    ### Returns
    - `Type[Schema]`: a standard schema subclass
    """
    try:
        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = "ConvertedFromAnthropic"
            fields = []

        # Type mapping from JSON Schema to Python
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict
        }

        # Extract properties
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        # Convert each property
        for name, prop in properties.items():
            prop_type = prop.get("type", "string")
            field_type = type_mapping.get(prop_type, str)
            description = prop.get("description", "")
            required = name in required_fields
            default = prop.get("default") if not required else None

            ConvertedSchema.fields.append(
                Field(
                    name=name,
                    type=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Anthropic schema to Belso format: {e}")
        # Return a minimal schema if conversion fails
        class FallbackSchema(Schema):
            name = "FallbackSchema"
            fields = [Field(name="text", type=str, description="Fallback field", required=True)]
        return FallbackSchema
