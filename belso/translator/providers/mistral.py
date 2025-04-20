from typing import Any, Dict, Type

from belso.schemas import Schema, Field
from belso.utils.logging import get_logger

# Get a module-specific logger
logger = get_logger(__name__)

def to_mistral(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Translate a standard schema to Mistral AI format.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    ---
    ### Returns
    - `Dict[str, Any]`: the converted schema as a dictionary.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting translation of schema '{schema_name}' to Mistral format...")

        properties = {}
        required_fields = schema.get_required_fields()

        logger.debug(f"Found {len(schema.fields)} fields, {len(required_fields)} required.")

        # Build properties for each field
        for field in schema.fields:
            logger.debug(f"Processing field '{field.name}' of type '{field.type.__name__}'...")

            # Determine JSON Schema type
            if field.type == str:
                json_type = "string"
            elif field.type == int:
                json_type = "integer"
            elif field.type == float:
                json_type = "number"
            elif field.type == bool:
                json_type = "boolean"
            elif field.type == list:
                json_type = "array"
            elif field.type == dict:
                json_type = "object"
            else:
                json_type = "string"  # Default
                logger.debug(f"Unknown type for field '{field.name}', defaulting to 'string'.")

            logger.debug(f"Mapped field '{field.name}' to JSON Schema type '{json_type}'.")

            properties[field.name] = {
                "type": json_type,
                "description": field.description
            }

            # Add default value if provided
            if not field.required and field.default is not None:
                properties[field.name]["default"] = field.default
                logger.debug(f"Added default value for field '{field.name}': {field.default}.")

        # Create the schema
        mistral_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": properties,
            "required": required_fields
        }

        logger.debug("Successfully created Mistral schema.")
        return mistral_schema

    except Exception as e:
        logger.error(f"Error translating schema to Mistral format: {e}")
        logger.debug("Translation error details", exc_info=True)
        return {}

def from_mistral(schema: Dict[str, Any]) -> Type[Schema]:
    """
    Convert a Mistral AI schema to Belso Schema format.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    ---
    ### Returns
    - `Type`: the converted schema as a Belso Schema subclass.
    """
    try:
        logger.debug("Starting conversion from Mistral schema to Belso format...")

        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = "ConvertedFromMistral"
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

        logger.debug(f"Found {len(properties)} properties, {len(required_fields)} required fields.")

        # Convert each property
        for name, prop in properties.items():
            prop_type = prop.get("type", "string")
            field_type = type_mapping.get(prop_type, str)
            description = prop.get("description", "")
            required = name in required_fields
            default = prop.get("default") if not required else None

            logger.debug(f"Converting property '{name}' of JSON Schema type '{prop_type}' to Python type '{field_type.__name__}'...")
            logger.debug(f"Property '{name}' is {'required' if required else 'optional'}.")

            if default is not None:
                logger.debug(f"Property '{name}' has default value: {default}.")

            ConvertedSchema.fields.append(
                Field(
                    name=name,
                    type=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        logger.debug(f"Successfully converted Mistral schema to Belso schema with {len(ConvertedSchema.fields)} fields.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Mistral schema to Belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        class FallbackSchema(Schema):
            name = "FallbackSchema"
            fields = [Field(name="text", type=str, description="Fallback field", required=True)]
        logger.warning("Returning fallback schema due to conversion error.")
        return FallbackSchema
