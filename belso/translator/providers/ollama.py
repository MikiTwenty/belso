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

logger = get_logger(__name__)

def to_ollama(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Convert a belso schema to Ollama-compatible JSON Schema format.
    ---
    ### Args
    - `schema` (`Type[Schema]`): the belso schema to convert.
    ---
    ### Returns
    - `Dict[str, Any]`: the converted JSON schema dictionary.
    """
    try:
        schema_name = getattr(schema, "__name__", "unnamed")
        logger.debug(f"Starting translation of schema '{schema_name}' to Ollama format...")

        def convert_field_to_property(field: BaseField) -> Dict[str, Any]:
            def _range_props():
                props = {}
                if field.range_:
                    props["minimum"] = field.range_[0]
                    props["maximum"] = field.range_[1]
                if field.exclusive_range:
                    if field.exclusive_range[0]:
                        props["exclusiveMinimum"] = field.range_[0]
                    if field.exclusive_range[1]:
                        props["exclusiveMaximum"] = field.range_[1]
                return props

            def _length_props():
                props = {}
                if field.length_range:
                    props["minLength"] = field.length_range[0]
                    props["maxLength"] = field.length_range[1]
                return props

            def _items_props():
                props = {}
                if field.items_range:
                    props["minItems"] = field.items_range[0]
                    props["maxItems"] = field.items_range[1]
                return props

            def _properties_props():
                props = {}
                if field.properties_range:
                    props["minProperties"] = field.properties_range[0]
                    props["maxProperties"] = field.properties_range[1]
                return props

            base = {
                "type": map_python_to_json_type(getattr(field, "type_", str)),
                "description": field.description
            }
            if field.default is not None:
                base["default"] = field.default
            if field.enum:
                base["enum"] = field.enum
            if field.regex:
                base["pattern"] = field.regex
            if field.multiple_of:
                base["multipleOf"] = field.multiple_of
            if field.format_:
                base["format"] = field.format_

            base.update(_range_props())
            base.update(_length_props())
            base.update(_items_props())
            base.update(_properties_props())

            return base

        def convert_nested(field: NestedField) -> Dict[str, Any]:
            nested = to_ollama(field.schema)
            return {
                "type": "object",
                "description": field.description,
                "properties": nested.get("properties", {}),
                "required": nested.get("required", [])
            }

        def convert_array(field: ArrayField) -> Dict[str, Any]:
            if hasattr(field, 'items_schema') and field.items_schema:
                items_schema_dict = to_ollama(field.items_schema)
                items_schema = {
                    "type": "object",
                    "properties": items_schema_dict.get("properties", {}),
                    "required": items_schema_dict.get("required", [])
                }
            else:
                items_schema = {"type": map_python_to_json_type(field.items_type)}

            result = {
                "type": "array",
                "description": field.description,
                "items": items_schema
            }
            if field.items_range:
                result["minItems"] = field.items_range[0]
                result["maxItems"] = field.items_range[1]
            return result

        properties = {}
        for field in schema.fields:
            if isinstance(field, NestedField):
                properties[field.name] = convert_nested(field)
            elif isinstance(field, ArrayField):
                properties[field.name] = convert_array(field)
            else:
                properties[field.name] = convert_field_to_property(field)

        return {
            "type": "object",
            "properties": properties,
            "required": schema.get_required_fields()
        }

    except Exception as e:
        logger.error(f"Error translating schema to Ollama format: {e}")
        logger.debug("Translation error details", exc_info=True)
        return {}

def from_ollama(schema: Dict[str, Any]) -> Type[Schema]:
    """
    Convert an Ollama-compatible JSON schema into a belso Schema.
    ---
    ### Args
    - `schema` (`Dict[str, Any]`): the JSON schema dictionary.
    ---
    ### Returns
    - `Type[Schema]`: the converted belso Schema.
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
                    NestedField(name=name, schema=nested_schema, description=description, required=required)
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
                        ArrayField(name=name, items_type=dict, description=description, required=required)
                    )
                else:
                    item_type = map_json_to_python_type(items.get("type", "string"))
                    ConvertedSchema.fields.append(
                        ArrayField(name=name, items_type=item_type, description=description, required=required)
                    )
            else:
                field_type = map_json_to_python_type(prop_type)
                ConvertedSchema.fields.append(
                    BaseField(name=name, type_=field_type, description=description, required=required, default=default)
                )

        logger.debug("Successfully converted Ollama schema to belso schema.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting Ollama schema to belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        return create_fallback_schema()
