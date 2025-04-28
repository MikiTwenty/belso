# belso.formats.json_format

import json
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from belso.utils import get_logger
from belso.core import Schema, BaseField
from belso.utils.constants import _JSON_TYPE_MAP
from belso.core.field import NestedField, ArrayField
from belso.utils.helpers import create_fallback_schema

_logger = get_logger(__name__)

def _add_prefix(
        base: str,
        prefix: str
    ) -> str:
    """
    Apply `prefix` only if `base` does not already start with it.\n
    ---
    ### Args
    - `base` (`str`): original string.
    - `prefix` (`str`): prefix to apply.\n
    ---
    ### Returns
    - `str`: `base` prefixed with `prefix` if needed.
    """
    return base if not prefix or base.startswith(prefix) else f"{prefix}{base}"

def _field_dict(field: BaseField) -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "name": field.name,
        "type": field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_),
        "description": field.description,
        "required": field.required,
    }
    if field.default is not None:
        d["default"] = field.default
    return d

def _to_json(
        schema: Type[Schema], *,
        root_prefix: str = ""
    ) -> Dict[str, Any]:
    """
    Serialize `schema` in a dict JSON-ready.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): schema to serialize.
    - `root_prefix` (`str`, optional): prefix to apply to the root schema name.\n
    ---
    ### Returns
    - `Dict[str, Any]`: dict JSON-ready representation of `schema`.
    """
    schema_json: Dict[str, Any] = {
        "name": _add_prefix(schema.__name__, root_prefix),
        "fields": []
    }

    for fld in schema.fields:
        # nested object
        if isinstance(fld, NestedField):
            fld_dict = _field_dict(fld)
            fld_dict["schema"] = _to_json(fld.schema, root_prefix="")
            schema_json["fields"].append(fld_dict)
            continue

        # array
        if isinstance(fld, ArrayField):
            fld_dict = _field_dict(fld)
            fld_dict["items_type"] = (
                fld.items_type.__name__ if hasattr(fld.items_type, "__name__") else str(fld.items_type)
            )
            if fld.items_schema:
                fld_dict["items_schema"] = _to_json(fld.items_schema, root_prefix="")
            schema_json["fields"].append(fld_dict)
            continue

        # primitive
        schema_json["fields"].append(_field_dict(fld))

    return schema_json

def to_json(
        schema: Type[Schema],
        file_path: Optional[Union[str, Path]] = None,
        name_prefix: str = "",
    ) -> Dict[str, Any]:
    """
    Serialize `schema` in JSON format.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): schema to serialize.
    - `file_path` (`Optional[Union[str, Path]]`, optional): path to save the JSON file.
    - `name_prefix` (`str`, optional): prefix to apply to the root schema name.\n
    ---
    ### Returns
    - `Dict[str, Any]`: dict JSON-ready representation of `schema`.
    """
    try:
        data = _to_json(schema, root_prefix=name_prefix)
        if file_path:
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=2)
        return data
    except Exception as exc:  # pragma: no cover
        _logger.error("Error converting schema to JSON: %s", exc, exc_info=True)
        return {"name": "ErrorSchema", "fields": []}

def _from_json(data: Dict[str, Any]) -> Type[Schema]:
    """
    Load JSON data into a belso Schema.\n
    ---
    ### Args
    - `data` (`Dict[str, Any]`): JSON data to load.\n
    ---
    ### Returns
    - `Type[Schema]`: belso Schema loaded from JSON data.
    """
    class DynamicSchema(Schema):
        fields: list = []

    DynamicSchema.__name__ = data.get("name", "LoadedSchema")

    for fld in data.get("fields", []):
        name: str = fld["name"]
        required: bool = fld.get("required", True)
        default = fld.get("default")
        descr = fld.get("description", "")

        # nested object
        if "schema" in fld:
            nested_schema = _from_json(fld["schema"])
            DynamicSchema.fields.append(
                NestedField(name=name, schema=nested_schema, description=descr,
                            required=required, default=default)
            )
            continue

        # array
        if "items_schema" in fld:
            items_schema = _from_json(fld["items_schema"])
            DynamicSchema.fields.append(
                ArrayField(name=name, items_type=list, items_schema=items_schema,
                           description=descr, required=required, default=default)
            )
            continue
        if fld.get("type", "").lower() == "list":
            DynamicSchema.fields.append(
                ArrayField(name=name, items_type=str,
                           description=descr, required=required, default=default)
            )
            continue

        # primitive
        py_type = _JSON_TYPE_MAP.get(fld.get("type", "str").lower(), str)
        DynamicSchema.fields.append(
            BaseField(name=name, type_=py_type, description=descr,
                      required=required, default=default)
        )

    return DynamicSchema

def from_json(
        json_input: Union[str, Path, Dict[str, Any]],
        name_prefix: str = ""
    ) -> Type[Schema]:
    """
    Load JSON (string / file / dict) into a belso Schema.\n
    ---
    ### Args
    - `json_input` (`Union[str, Path, Dict[str, Any]]`): JSON input to load.
    - `name_prefix` (`str`, optional): prefix to apply to the root schema name.\n
    ---
    ### Returns
    - `Type[Schema]`: belso Schema loaded from JSON input.
    """
    try:
        if isinstance(json_input, (str, Path)):
            with open(json_input, "r", encoding="utf-8") as fp:
                data = json.load(fp)
        else:
            data = json_input

        schema_cls = _from_json(data)
        schema_cls.__name__ = _add_prefix(schema_cls.__name__, name_prefix)
        return schema_cls

    except Exception as exc:  # pragma: no cover
        _logger.error("Error loading schema from JSON: %s", exc, exc_info=True)
        return create_fallback_schema()
