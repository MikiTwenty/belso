# belso.providers.base.json_schema

from typing import Any, Dict, Type, Callable, Optional

from belso.utils.logging import get_logger
from belso.core.schema import Schema, BaseField
from belso.utils.mappings.field_mappings import _JSON_FIELD_MAP
from belso.core.field import NestedField, ArrayField
from belso.utils.helpers import (
    map_json_to_python_type,
    map_python_to_json_type,
    create_fallback_schema
)

_logger = get_logger(__name__)

def convert_field_to_property(
        field: BaseField
    ) -> Dict[str, Any]:
    """
    Converts a base field into a JSON schema property using a specific mapping.\n
    ---
    ### Args
    - `field` (`BaseField`): the field to convert.\n
    ---
    ### Returns
    - `dict`: the property dictionary.
    """
    base_property = {
        "type": map_python_to_json_type(getattr(field, "type_", str)),
        "description": field.description
    }
    for attr, mappings in _JSON_FIELD_MAP.items():
        value = getattr(field, attr, None)
        if value is not None:
            if isinstance(mappings, list):
                for key, func in mappings:
                    base_property[key] = func(value)
            else:
                key, func = mappings
                base_property[key] = func(value) if func else value
    return base_property

def convert_nested_field(
        field: NestedField,
        to_func: Callable[[Type[Schema]], Dict[str, Any]]
    ) -> Dict[str, Any]:
    """
    Converts a nested field into a JSON schema property using a specific mapping.\n
    ---
    ### Args
    - `field` (`NestedField`): the field to convert.
    - `to_func` (`Callable[[Type[Schema]], Dict[str, Any]]`): the function to convert the nested schema.\n
    ---
    ### Returns
    - `dict`: the property dictionary.
    """
    nested_schema = to_func(field.schema)
    return {
        "type": "object",
        "description": field.description,
        "properties": nested_schema.get("properties", {}),
        "required": nested_schema.get("required", [])
    }

def convert_array_field(
        field: ArrayField,
        to_func: Callable[[Type[Schema]], Dict[str, Any]]
    ) -> Dict[str, Any]:
    """
    Converts an array field into a JSON schema property using a specific mapping.\n
    ---
    ### Args
    - `field` (`ArrayField`): the field to convert.
    - `to_func` (`Callable[[Type[Schema]], Dict[str, Any]]`): the function to convert the nested schema.\n
    ---
    ### Returns
    - `dict`: the property dictionary.
    """
    if hasattr(field, 'items_schema') and field.items_schema:
        items_schema_dict = to_func(field.items_schema)
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

def to_json_schema(
        schema: Type[Schema],
        extra_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
    """
    Converts a belso schema into a generic JSON schema format.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the schema to convert.
    - `extra_metadata` (`dict`, optional): extra metadata to add to the schema.\n
    ---
    ### Returns
    - `dict`: the JSON schema.
    """
    try:
        _logger.debug(f"Translating schema '{schema.__name__}' to generic JSON schema format...")

        properties = {}
        for field in schema.fields:
            if isinstance(field, NestedField):
                properties[field.name] = convert_nested_field(field, lambda s: to_json_schema(s, _JSON_FIELD_MAP))
            elif isinstance(field, ArrayField):
                properties[field.name] = convert_array_field(field, lambda s: to_json_schema(s, _JSON_FIELD_MAP))
            else:
                properties[field.name] = convert_field_to_property(field)

        schema_dict = {
            "type": "object",
            "properties": properties,
            "required": schema.get_required_fields()
        }

        if extra_metadata:
            schema_dict.update(extra_metadata)

        return schema_dict

    except Exception as e:
        _logger.error(f"Error converting to JSON schema: {e}")
        return {}

def from_json_schema(
        schema: Dict[str, Any],
        reverse_type_func: Callable[[str], Any],
        from_func: Callable[[Dict[str, Any], str], Type[Schema]],
        schema_name: str = "Schema"
    ) -> Type[Schema]:
    """
    Converts a generic JSON schema into a belso schema.\n
    ---
    ### Args
    - `schema` (`dict`): the schema to convert.
    - `reverse_type_func` (`Callable[[str], Any]`): the function to reverse the type mapping.
    - `from_func` (`Callable[[Dict[str, Any], str], Type[Schema]]`): the function to convert the nested schema.
    - `schema_name` (`str`, optional): the name of the schema.\n
    ---
    ### Returns
    - `Type[Schema]`: the converted schema.
    """
    try:
        _logger.debug("Starting conversion from generic JSON schema to belso format...")

        ConvertedSchema = type(f"{schema_name}Schema", (Schema,), {"fields": []})

        properties = schema.get("properties", {})
        required_fields = set(schema.get("required", []))

        for name, prop in properties.items():
            prop_type = prop.get("type", "string")
            description = prop.get("description", "")
            required = name in required_fields
            default = prop.get("default") if not required else None

            if prop_type == "object" and "properties" in prop:
                nested = from_func(prop, schema_name=f"{name}")
                ConvertedSchema.fields.append(NestedField(name=name, schema=nested, description=description, required=required, default=default))
            elif prop_type == "array" and "items" in prop:
                items = prop["items"]
                if items.get("type") == "object" and "properties" in items:
                    item_schema = from_func(items, schema_name=f"{name}")
                    ConvertedSchema.fields.append(ArrayField(name=name, items_type=dict, description=description, required=required, default=default))
                else:
                    item_type = reverse_type_func(items.get("type", "string"))
                    ConvertedSchema.fields.append(ArrayField(name=name, items_type=item_type, description=description, required=required, default=default))
            else:
                ConvertedSchema.fields.append(BaseField(name=name, type_=reverse_type_func(prop_type), description=description, required=required, default=default))

        return ConvertedSchema

    except Exception as e:
        _logger.error(f"Error converting from JSON schema: {e}")
        return create_fallback_schema()

def json_provider(extra_metadata:Optional[dict]=None):
    """
    Decorator that converts a belso schema into a generic JSON schema format and vice versa.\n
    ---
    ### Args
    - `extra_metadata` (`Optional[dict]`): extra metadata to add to the schema.\n
    ---
    ### Returns
    - `tuple`: a tuple containing the `to_func` and `from_func` functions.
    """
    def wrapper(func):
        def to_func(schema: Type[Schema]) -> Dict[str, Any]:
            """
            Converts a belso schema into JSON Schema format for the given provider.\n
            ---
            ### Args
            - `schema` (`Type[Schema]`): belso schema to convert.\n
            ---
            ### Returns
            - `Dict[str, Any]`: JSON Schema representation.
            """
            return to_json_schema(schema, extra_metadata=extra_metadata)
        def from_func(
                schema: Dict[str, Any],
                schema_name: str = "Schema"
            ) -> Type[Schema]:
            """
            Converts a JSON Schema dict into a belso schema.\n
            ---
            ### Args
            - `schema` (`Dict[str, Any]`): JSON schema dictionary.
            - `schema_name` (`str`): optional name for the resulting Schema class.\n
            ---
            ### Returns
            - `Type[Schema]`: reconstructed belso schema.
            """
            return from_json_schema(schema, map_json_to_python_type, from_func, schema_name)
        return to_func, from_func
    return wrapper
