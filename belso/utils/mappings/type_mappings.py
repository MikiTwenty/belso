# belso.utils.mappings.type_mappings

from typing import Any
from google.ai.generativelanguage_v1beta.types import content

_FILE_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "any": Any
}

_GOOGLE_TYPE_MAP = {
    str: content.Type.STRING,
    int: content.Type.INTEGER,
    float: content.Type.NUMBER,
    bool: content.Type.BOOLEAN,
    list: content.Type.ARRAY,
    dict: content.Type.OBJECT,
    Any: content.Type.TYPE_UNSPECIFIED
}

_REVERSE_GOOGLE_TYPE_MAP = {v: k for k, v in _GOOGLE_TYPE_MAP.items()}
