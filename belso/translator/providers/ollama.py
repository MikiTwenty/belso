from typing import Any, Dict, Type

from belso.schemas import Schema, Field
from belso.utils.logging import get_logger
from belso.utils.schema_helpers import (
    map_json_to_python_type,
    build_properties_dict,
    create_fallback_schema
)

# Get a module-specific logger
logger = get_logger(__name__)

def to_ollama(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Translate a standard schema to Ollama format.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the schema to translate.\n
    ---
    ### Returns:
    - `Dict[str, Any]`: the translated schema in Ollama format.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting translation of schema '{schema_name}' to Ollama format...")

        if not hasattr(schema, "fields") or not schema.fields:
            raise ValueError(f"Schema '{schema_name}' has no fields defined")

        properties = build_properties_dict(schema)
        required_fields = schema.get_required_fields()

        # Create the schema
        ollama_schema = {
            "type": "object",
            "properties": properties,
            "required": required_fields
        }

        logger.debug("Successfully created Ollama schema.")
        return ollama_schema

    except Exception as e:
        logger.error(f"Error translating schema to Ollama format: {e}")
        logger.debug("Translation error details", exc_info=True)
        return {}

def from_ollama(schema: Dict[str, Any]) -> Type[Schema]:
    """
    Convert an Ollama schema to Belso Schema format.\n
    ---
    ### Args
    - `schema` (`Dict[str, Any]`): the schema to convert.\n
    ---
    ### Returns:
    - `Type[Schema]`: the converted schema as a Belso Schema subclass.
    """
    try:
        logger.debug("Starting conversion from Ollama schema to Belso format...")

        if not isinstance(schema, dict) or "properties" not in schema:
            raise ValueError("Invalid Ollama schema format: missing properties")

        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = "ConvertedFromOllama"
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

            ConvertedSchema.fields.append(
                Field(
                    name=name,
                    type=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        logger.debug(f"Successfully converted Ollama schema to Belso schema with {len(ConvertedSchema.fields)} fields.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Ollama schema to Belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        return create_fallback_schema()
