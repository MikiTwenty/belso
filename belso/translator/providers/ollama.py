from typing import Any, Dict, Type

from belso.utils.logging import get_logger
from belso.schemas import Schema, BaseField
from belso.schemas.nested import NestedField, ArrayField
from belso.utils.schema_helpers import (
    map_json_to_python_type,
    map_python_to_json_type,
    build_properties_dict,
    create_fallback_schema
)

# Get a module-specific logger
logger = get_logger(__name__)

def to_ollama(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Convert a belso schema to Ollama format.
    ---
    ### Args
    - `schema` (`Type[belso.Schema]`): the belso schema to convert.
    ---
    ### Returns:
    - `Dict[str, Any]`: the converted schema.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting translation of schema '{schema_name}' to Ollama format...")

        if not hasattr(schema, "fields") or not schema.fields:
            raise ValueError(f"Schema '{schema_name}' has no fields defined")

        def convert_field_to_property(field: BaseField) -> Dict[str, Any]:
            if isinstance(field, NestedField):
                nested_schema = to_ollama(field.schema)
                return {
                    "type": "object",
                    "description": field.description,
                    "properties": nested_schema.get("properties", {}),
                    "required": nested_schema.get("required", [])
                }
            elif isinstance(field, ArrayField):
                if hasattr(field, 'items_schema') and field.items_schema:
                    items_schema_dict = to_ollama(field.items_schema)
                    items_schema = {
                        "type": "object",
                        "properties": items_schema_dict.get("properties", {}),
                        "required": items_schema_dict.get("required", [])
                    }
                else:
                    items_schema = {"type": map_python_to_json_type(field.items_type)}
                return {
                    "type": "array",
                    "description": field.description,
                    "items": items_schema
                }
            else:
                prop = {
                    "type": map_python_to_json_type(field.type_),
                    "description": field.description
                }
                if not field.required and field.default is not None:
                    prop["default"] = field.default
                return prop

        properties = {
            field.name: convert_field_to_property(field)
            for field in schema.fields
        }

        required_fields = schema.get_required_fields()

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
    Convert an Ollama JSON schema to belso Schema format, including nested objects and arrays.
    ---
    ### Args
    - `schema` (`Dict[str, Any]`): the JSON schema to convert.
    ---
    ### Returns
    - `Type[Schema]`: a new belso Schema class.
    """
    try:
        logger.debug("Starting conversion from Ollama schema to belso format...")

        if not isinstance(schema, dict) or "properties" not in schema:
            raise ValueError("Invalid Ollama schema format: missing 'properties'")

        class ConvertedSchema(Schema):
            name = "ConvertedFromOllama"
            fields = []

        properties = schema.get("properties", {})
        required_fields = set(schema.get("required", []))

        for name, prop in properties.items():
            prop_type = prop.get("type", "string")
            description = prop.get("description", "")
            required = name in required_fields
            default = prop.get("default") if not required else None

            if prop_type == "object" and "properties" in prop:
                nested_schema_dict = {
                    "type": "object",
                    "properties": prop.get("properties", {}),
                    "required": prop.get("required", [])
                }
                nested_schema = from_ollama(nested_schema_dict)
                ConvertedSchema.fields.append(
                    NestedField(
                        name=name,
                        schema=nested_schema,
                        description=description,
                        required=required
                    )
                )
            elif prop_type == "array" and "items" in prop:
                items = prop["items"]
                if items.get("type") == "object" and "properties" in items:
                    item_schema_dict = {
                        "type": "object",
                        "properties": items.get("properties", {}),
                        "required": items.get("required", [])
                    }
                    item_schema = from_ollama(item_schema_dict)
                    ConvertedSchema.fields.append(
                        ArrayField(
                            name=name,
                            items_type=dict,
                            description=description,
                            required=required
                        )
                    )
                else:
                    item_type = map_json_to_python_type(items.get("type", "string"))
                    ConvertedSchema.fields.append(
                        ArrayField(
                            name=name,
                            items_type=item_type,
                            description=description,
                            required=required
                        )
                    )
            else:
                field_type = map_json_to_python_type(prop_type)
                ConvertedSchema.fields.append(
                    BaseField(
                        name=name,
                        type_=field_type,
                        description=description,
                        required=required,
                        default=default
                    )
                )

        logger.debug("Successfully converted Ollama schema to belso schema.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Ollama schema to belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        return create_fallback_schema()
