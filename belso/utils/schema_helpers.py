from typing import Dict, Type, Any

from belso.schemas import Schema, Field

# Common type mappings
PYTHON_TO_JSON_TYPE_MAPPING = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object"
}

JSON_TO_PYTHON_TYPE_MAPPING = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict
}

SUPPORT_NESTED_SCHEMA = [
    "openai",
    "google",
    "anthropic",
    "mistral"
]

def create_fallback_schema() -> Type[Schema]:
    """
    Create a standard fallback schema when conversion fails.\n
    ---
    ### Returns
    - `Type[Schema]`: the fallback schema.
    """
    class FallbackSchema(Schema):
        name = "FallbackSchema"
        fields = [Field(name="text", type=str, description="Fallback field", required=True)]
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
    return PYTHON_TO_JSON_TYPE_MAPPING.get(field_type, "string")

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
    return JSON_TO_PYTHON_TYPE_MAPPING.get(json_type, str)

def build_properties_dict(schema: Type[Schema]) -> Dict[str, Dict[str, Any]]:
    """
    Build a properties dictionary from a schema for JSON Schema formats.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the schema to build the properties dictionary from.\n
    ---
    ### Returns
    - `Dict[str, Dict[str, Any]]`: the properties dictionary.
    """
    properties = {}

    for field in schema.fields:
        json_type = map_python_to_json_type(field.type)

        property_def = {
            "type": json_type,
            "description": field.description
        }

        # Add default value if provided and field is not required
        if not field.required and field.default is not None:
            property_def["default"] = field.default

        properties[field.name] = property_def

    return properties

def is_schema_supported(
        schema: Type[Schema],
        provider: str
    ) -> bool:
    """
    Check if a schema is supported by a provider.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the schema to check.
    - `provider` (`str`): the provider to check against.\n
    ---
    ### Returns
    - `bool`: `True` if the schema is supported, `False` otherwise.
    """
    # Basic support check - can be extended with provider-specific logic
    if not hasattr(schema, "fields") or not schema.fields:
        return False

    # Verifica se lo schema è annidato
    has_nested_schema = False
    for field in schema.fields:
        if issubclass(field.type, Schema):
            has_nested_schema = True
            break

    # Se lo schema è annidato, verifica se il provider lo supporta
    if has_nested_schema:
        return provider.lower() in SUPPORT_NESTED_SCHEMA

    # Se lo schema non è annidato, tutti i provider lo supportano
    return True
