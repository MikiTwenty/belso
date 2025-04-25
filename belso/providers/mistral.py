# belso.providers.mistral

from typing import Any, Dict, Type

from belso.utils import get_logger
from belso.core import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils.helpers import (
    map_json_to_python_type,
    map_python_to_json_type,
    create_fallback_schema
)

_logger = get_logger(__name__)

_MISTRAL_FIELD_TO_PROPERTY_MAPPING = {
    "default": ("default", None),
    "enum": ("enum", None),
    "regex": ("pattern", None),
    "multiple_of": ("multipleOf", None),
    "format_": ("format", None),
    "range_": [("minimum", lambda r: r[0]), ("maximum", lambda r: r[1])],
    "exclusive_range": [("exclusiveMinimum", lambda r: r[0]), ("exclusiveMaximum", lambda r: r[1])],
    "length_range": [("minLength", lambda r: r[0]), ("maxLength", lambda r: r[1])],
    "items_range": [("minItems", lambda r: r[0]), ("maxItems", lambda r: r[1])],
    "properties_range": [("minProperties", lambda r: r[0]), ("maxProperties", lambda r: r[1])]
}

def _convert_field_to_property(field: BaseField) -> Dict[str, Any]:
    base_property = {
        "type": map_python_to_json_type(getattr(field, "type_", str)),
        "description": field.description
    }
    for attr, mappings in _MISTRAL_FIELD_TO_PROPERTY_MAPPING.items():
        value = getattr(field, attr, None)
        if value is not None:
            if isinstance(mappings, list):
                for key, func in mappings:
                    base_property[key] = func(value)
            else:
                key, func = mappings
                base_property[key] = func(value) if func else value
    return base_property

def _convert_nested_field(field: NestedField) -> Dict[str, Any]:
    nested_schema = to_mistral(field.schema)
    return {
        "type": "object",
        "description": field.description,
        "properties": nested_schema.get("properties", {}),
        "required": nested_schema.get("required", [])
    }

def _convert_array_field(field: ArrayField) -> Dict[str, Any]:
    if hasattr(field, 'items_schema') and field.items_schema:
        items_schema_dict = to_mistral(field.items_schema)
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

def to_mistral(schema: Type[Schema]) -> Dict[str, Any]:
    try:
        schema_name = getattr(schema, "__name__", "unnamed")
        _logger.debug(f"Starting translation of schema '{schema_name}' to Mistral format...")

        properties = {}
        for field in schema.fields:
            if isinstance(field, NestedField):
                properties[field.name] = _convert_nested_field(field)
            elif isinstance(field, ArrayField):
                properties[field.name] = _convert_array_field(field)
            else:
                properties[field.name] = _convert_field_to_property(field)

        return {
            "type": "object",
            "properties": properties,
            "required": schema.get_required_fields()
        }

    except Exception as e:
        _logger.error(f"Error translating schema to Mistral format: {e}")
        _logger.debug("Translation error details", exc_info=True)
        return {}

def from_mistral(schema: Dict[str, Any], name_prefix: str = "Converted") -> Type[Schema]:
    try:
        _logger.debug("Starting conversion from Mistral schema to belso format...")

        schema_class_name = f"{name_prefix}Schema"
        ConvertedSchema = type(schema_class_name, (Schema,), {"fields": []})

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
                nested_schema = from_mistral(nested_schema_dict, name_prefix=f"{name_prefix}_{name}")
                ConvertedSchema.fields.append(
                    NestedField(
                        name=name,
                        schema=nested_schema,
                        description=description,
                        required=required,
                        default=default
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
                    item_schema = from_mistral(item_schema_dict, name_prefix=f"{name_prefix}_{name}")
                    ConvertedSchema.fields.append(
                        ArrayField(
                            name=name,
                            items_type=dict,
                            description=description,
                            required=required,
                            default=default
                        )
                    )
                else:
                    item_type = map_json_to_python_type(items.get("type", "string"))
                    ConvertedSchema.fields.append(
                        ArrayField(
                            name=name,
                            items_type=item_type,
                            description=description,
                            required=required,
                            default=default
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

        _logger.debug("Successfully converted Mistral schema to belso format.")
        return ConvertedSchema

    except Exception as e:
        _logger.error(f"Error converting Mistral schema to belso format: {e}")
        _logger.debug("Conversion error details", exc_info=True)
        return create_fallback_schema()
