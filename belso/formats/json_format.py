# belso.formats.json_format

import json
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from belso.utils import get_logger
from belso.core import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils.helpers import create_fallback_schema

_logger = get_logger(__name__)

_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "any": Any
}

def _add_prefix(
        base: str,
        prefix: str
    ) -> str:
    """
    Applica `prefix` solo se `base` non lo possiede già in testa.
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
    schema_json: Dict[str, Any] = {
        "name": _add_prefix(schema.__name__, root_prefix),
        "fields": []
    }

    for fld in schema.fields:
        # nested object
        if isinstance(fld, NestedField):
            fld_dict = _field_dict(fld)
            # nessun nuovo prefisso – manteniamo il nome originale del nested schema
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
    Serializza `schema` in un dizionario JSON-ready e, se indicato,
    lo salva su disco.
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
    class DynamicSchema(Schema):
        fields: list = []

    DynamicSchema.__name__ = data.get("name", "LoadedSchema")

    for fld in data.get("fields", []):
        name: str = fld["name"]
        required: bool = fld.get("required", True)
        default = fld.get("default")
        descr = fld.get("description", "")

        # ------- nested object ---------------------------------------------
        if "schema" in fld:
            nested_schema = _from_json(fld["schema"])
            DynamicSchema.fields.append(
                NestedField(name=name, schema=nested_schema, description=descr,
                            required=required, default=default)
            )
            continue

        # ------- array ------------------------------------------------------
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

        # ------- primitive --------------------------------------------------
        py_type = _TYPE_MAP.get(fld.get("type", "str").lower(), str)
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
    Carica uno schema JSON (dict o file) in un `belso.Schema`.
    Applica, se richiesto, un prefisso **solo** al nome dello
    schema root, senza toccare i nomi già presenti nei nested.
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
