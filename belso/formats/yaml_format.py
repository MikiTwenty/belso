# belso.formats.yaml_format

import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from belso.core import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils import get_logger
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

def _add_prefix(base: str, prefix: str) -> str:
    """
    Add `prefix` only if `base` does **not** already start with it.
    """
    return base if (not prefix or base.startswith(prefix)) else f"{prefix}{base}"

def _field_dict(f: BaseField) -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "name": f.name,
        "type": f.type_.__name__ if hasattr(f.type_, "__name__") else str(f.type_),
        "description": f.description,
        "required": f.required,
    }
    if f.default is not None:
        d["default"] = f.default
    return d

def _to_yaml(
        schema: Type[Schema], *,
        root_prefix: str = ""
    ) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "name": _add_prefix(schema.__name__, root_prefix),
        "fields": []
    }

    for fld in schema.fields:
        # nested object
        if isinstance(fld, NestedField):
            fd = _field_dict(fld)
            fd["schema"] = _to_yaml(fld.schema, root_prefix="")         # **no extra prefix**
            data["fields"].append(fd)
            continue

        # array
        if isinstance(fld, ArrayField):
            fd = _field_dict(fld)
            fd["items_type"] = (
                fld.items_type.__name__ if hasattr(fld.items_type, "__name__") else str(fld.items_type)
            )
            if fld.items_schema:
                fd["items_schema"] = _to_yaml(fld.items_schema, root_prefix="")
            data["fields"].append(fd)
            continue

        # primitive
        data["fields"].append(_field_dict(fld))

    return data

def to_yaml(
        schema: Type[Schema],
        file_path: Optional[Union[str, Path]] = None,
        name_prefix: str = ""
    ) -> str:
    """
    Serialise `schema` to YAML.  `name_prefix` is applied **once** to the
    root schema only; children keep their own names untouched.
    """
    try:
        data = _to_yaml(schema, root_prefix=name_prefix)
        yaml_text = yaml.dump(data, sort_keys=False, allow_unicode=True)
        if file_path:
            Path(file_path).write_text(yaml_text, encoding="utf-8")
        return yaml_text
    except Exception as e: # pragma: no cover
        _logger.error(f"Error converting schema to YAML: {e}", exc_info=True)
        return "name: ErrorSchema\nfields: []\n"

def _from_yaml(data: Dict[str, Any]) -> Type[Schema]:
    class DynamicSchema(Schema):
        fields: list = []

    DynamicSchema.__name__ = data.get("name", "LoadedSchema")

    for fld in data.get("fields", []):
        name: str = fld["name"]
        required: bool = fld.get("required", True)
        default = fld.get("default")
        descr = fld.get("description", "")

        # nested
        if "schema" in fld:
            nested_schema = _from_yaml(fld["schema"])
            DynamicSchema.fields.append(
                NestedField(name=name, schema=nested_schema,
                            description=descr, required=required, default=default)
            )
            continue

        # array
        if "items_schema" in fld:
            items_schema = _from_yaml(fld["items_schema"])
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
        py_type = _TYPE_MAP.get(fld.get("type", "str").lower(), str)
        DynamicSchema.fields.append(
            BaseField(name=name, type_=py_type, description=descr,
                      required=required, default=default)
        )

    return DynamicSchema

def from_yaml(
        yaml_input: Union[str, Path, Dict[str, Any]],
        name_prefix: str = ""
    ) -> Type[Schema]:
    """
    Load YAML (string / file / dict) into a belso Schema.
    `name_prefix` is applied **only** to the root schema name.
    """
    try:
        if isinstance(yaml_input, (str, Path)):
            text = Path(yaml_input).read_text(encoding="utf-8") if Path(yaml_input).exists() else yaml_input
            data = yaml.safe_load(text)
        else:
            data = yaml_input

        schema_cls = _from_yaml(data)
        schema_cls.__name__ = _add_prefix(schema_cls.__name__, name_prefix)
        return schema_cls

    except Exception as e:                                                   # pragma: no cover
        _logger.error(f"Error loading schema from YAML: {e}", exc_info=True)
        return create_fallback_schema()
