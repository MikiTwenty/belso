# belso.utils.helpers

from typing import Dict, Type, Any

from belso.core import Schema, BaseField

# Common type mappings
_PYTHON_TO_JSON_TYPE_MAPPING = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object"
}

_JSON_TO_PYTHON_TYPE_MAPPING = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict
}

def create_fallback_schema() -> Type[Schema]:
    """
    Create a standard fallback schema when conversion fails.\n
    ---
    ### Returns
    - `Type[belso.Schema]`: the fallback schema.
    """
    class FallbackSchema(Schema):
        name = "FallbackSchema"
        fields = [
            BaseField(
                name="text",
                type_=str,
                description="Fallback field",
                required=True
            )
        ]
    return FallbackSchema

def map_python_to_json_type(field_type: Type) -> str:
    """
    Map Python type to JSON Schema type.\n
    ---
    ### Args
    - `field_type` (`Type`): the Python type to map.\n
    ---
    ### Returns
    - `str`: the JSON Schema type.
    """
    return _PYTHON_TO_JSON_TYPE_MAPPING.get(field_type, "string")

def map_json_to_python_type(json_type: str) -> Type:
    """
    Map JSON Schema type to Python type.\n
    ---
    ### Args
    - `json_type` (`str`): the JSON Schema type to map.\n
    ---
    ### Returns
    - `Type`: the Python type.
    """
    return _JSON_TO_PYTHON_TYPE_MAPPING.get(json_type, str)

def build_properties_dict(schema: Type[Schema]) -> Dict[str, Dict[str, Any]]:
    """
    Build a properties dictionary from a schema for JSON Schema formats.\n
    ---
    ### Args
    - `schema` (`Type[belso.Schema]`): the schema to build the properties dictionary from.\n
    ---
    ### Returns
    - `Dict[str, Dict[str, Any]]`: the properties dictionary.
    """
    properties = {}

    for field in schema.fields:
        json_type = map_python_to_json_type(field.type_)

        property_def = {
            "type": json_type,
            "description": field.description
        }

        # Add default value if provided and field is not required
        if not field.required and field.default is not None:
            property_def["default"] = field.default

        properties[field.name] = property_def

    return properties
