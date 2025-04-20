import logging
from typing import Any, Dict, Type

from belso.translator.schemas import Schema, Field

logger = logging.getLogger(__name__)

def to_ollama(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Translate a standard schema to Ollama format.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    ---
    ### Returns
    - `Dict[str, Any]`: the converted schema as a dictionary.
    """
    try:
        properties = {}
        required_fields = schema.get_required_fields()

        # Build properties for each field
        for field in schema.fields:
            properties[field.name] = {
                "type": "string" if field.type == str else "number" if field.type in [int, float] else "boolean" if field.type == bool else "array" if field.type == list else "object",
                "description": field.description
            }

        # Create the schema
        ollama_schema = {
            "type": "object",
            "properties": properties,
            "required": required_fields
        }

        return ollama_schema

    except Exception as e:
        logger.error(f"Error translating schema to Ollama format: {e}")
        return {}

def from_ollama(schema: Dict[str, Any]) -> Type[Schema]:
    """
    Convert an Ollama schema to Belso Schema format.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    ---
    ### Returns
    - `Type`: the converted schema as a Belso Schema subclass.
    """
    try:
        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = "ConvertedFromOllama"
            fields = []

        # Type mapping from Ollama to Python
        type_mapping = {
            "string": str,
            "number": float,
            "integer": int,
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
        logger.error(f"Error converting Ollama schema to Belso format: {e}")
        # Return a minimal schema if conversion fails
        class FallbackSchema(Schema):
            name = "FallbackSchema"
            fields = [Field(name="text", type=str, description="Fallback field", required=True)]
        return FallbackSchema
