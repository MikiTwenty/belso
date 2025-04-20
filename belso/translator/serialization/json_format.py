import json
from typing import Dict, Any, Type, Union

from belso.translator.schemas import Schema, Field

def schema_to_json(
        schema: Type[Schema],
        file_path: str = None
    ) -> Dict[str, Any]:
    """
    Convert a Belso Schema to a standardized JSON format and optionally save to a file.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    - `file_path`: optional path to save the JSON to a file.\n
    ---
    ### Returns
    - `Dict[str, Any]`: the schema in JSON format.
    """
    fields_json = []

    for field in schema.fields:
        # Convert Python type to string representation
        type_str = field.type.__name__ if hasattr(field.type, "__name__") else str(field.type)

        field_json = {
            "name": field.name,
            "type": type_str,
            "description": field.description,
            "required": field.required
        }

        # Only include default if it exists
        if field.default is not None:
            field_json["default"] = field.default

        fields_json.append(field_json)

    schema_json = {
        "name": schema.name,
        "fields": fields_json
    }

    # Save to file if path is provided
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(schema_json, f, indent=2)

    return schema_json

def json_to_schema(json_input: Union[Dict[str, Any], str]) -> Type[Schema]:
    """
    Convert a standardized JSON format or JSON file to a Belso Schema.\n
    ---
    ### Args
    - `json_input`: either a JSON dictionary or a file path to a JSON file.\n
    ---
    ### Returns
    - `Type[Schema]`: the Belso Schema.
    """
    # Check if input is a file path
    if isinstance(json_input, str):
        # Try to load as a file
        try:
            with open(json_input, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load JSON from file: {e}")
    else:
        # Assume it's already a JSON dictionary
        json_data = json_input

    # Create a new Schema class
    class LoadedSchema(Schema):
        name = json_data.get("name", "LoadedSchema")
        fields = []

    # Type mapping from string to Python types
    type_mapping = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "any": Any
    }

    # Process each field
    for field_data in json_data.get("fields", []):
        field_type_str = field_data.get("type", "str")
        field_type = type_mapping.get(field_type_str.lower(), str)

        field = Field(
            name=field_data.get("name", ""),
            type=field_type,
            description=field_data.get("description", ""),
            required=field_data.get("required", True),
            default=field_data.get("default")
        )

        LoadedSchema.fields.append(field)

    return LoadedSchema
