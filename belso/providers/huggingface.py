from typing import Any, Dict, Type

from belso.utils import get_logger
from belso.core import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils.constants import _HUGGINGFACE_FIELD_MAP
from belso.utils.helpers import (
    map_json_to_python_type,
    map_python_to_json_type,
    create_fallback_schema
)

_logger = get_logger(__name__)

def _convert_field_to_property(field: BaseField) -> Dict[str, Any]:
    """
    Converts a base field into a property definition for Hugging Face.\n
    ---
    ### Args
    - `field` (`belso.core.BaseField`): the field to convert.\n
    ---
    ### Returns
    - `dict`: the property definition.\n
    """
    base_property = {
        "type": map_python_to_json_type(getattr(field, "type_", str)),
        "description": field.description
    }
    for attr, mappings in _HUGGINGFACE_FIELD_MAP.items():
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
    """
    Converts a nested field into a property definition for Hugging Face.\n
    ---
    ### Args
    - `field` (`belso.core.NestedField`): the nested field to convert.\n
    ---
    ### Returns
    - `dict`: the property definition.
    """
    nested_schema = to_huggingface(field.schema)
    return {
        "type": "object",
        "description": field.description,
        "properties": nested_schema.get("properties", {}),
        "required": nested_schema.get("required", [])
    }

def _convert_array_field(field: ArrayField) -> Dict[str, Any]:
    """
    Converts an array field into a property definition for Hugging Face.\n
    ---
    ### Args
    - `field` (`belso.core.ArrayField`): the array field to convert.\n
    ---
    ### Returns
    - `dict`: the property definition.
    """
    if hasattr(field, 'items_schema') and field.items_schema:
        items_schema_dict = to_huggingface(field.items_schema)
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

def to_huggingface(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Converts a belso schema into a Hugging Face schema.\n
    ---
    ### Args
    - `schema` (`belso.core.Schema`): the schema to convert.\n
    ---
    ### Returns
    - `dict`: the Hugging Face schema.
    """
    try:
        schema_name = getattr(schema, "__name__", "unnamed")
        _logger.debug(f"Starting translation of schema '{schema_name}' to Hugging Face format...")

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
            "format": "huggingface",
            "properties": properties,
            "required": schema.get_required_fields()
        }

    except Exception as e:
        _logger.error(f"Error translating schema to Hugging Face format: {e}")
        _logger.debug("Translation error details", exc_info=True)
        return {}

def from_huggingface(
        schema: Dict[str, Any],
        name_prefix: str = "Converted"
    ) -> Type[Schema]:
    """
    Converts a Hugging Face schema into a belso schema.\n
    ---
    ### Args
    - `schema` (`dict`): the Hugging Face schema to convert.
    - `name_prefix` (`str`, optional): the prefix to add to the converted schema name. Defaults to "Converted".\n
    ---
    ### Returns
    - `belso.core.Schema`: the converted belso schema.
    """
    try:
        _logger.debug("Starting conversion from Hugging Face schema to belso format...")

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
                nested_schema = from_huggingface(nested_schema_dict, name_prefix=f"{name_prefix}_{name}")
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
                    item_schema = from_huggingface(item_schema_dict, name_prefix=f"{name_prefix}_{name}")
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

        _logger.debug("Successfully converted Hugging Face schema to belso format.")
        return ConvertedSchema

    except Exception as e:
        _logger.error(f"Error converting Hugging Face schema to belso format: {e}")
        _logger.debug("Conversion error details", exc_info=True)
        return create_fallback_schema()
