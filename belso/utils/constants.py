# belso.utils.constants

from typing import Any
from google.ai.generativelanguage_v1beta.types import content

class FORMATS:
    """
    A class that provides constants for supported schema providers.
    This allows for more readable code when specifying providers in the translate method.
    """
    # Core providers
    BELSO = "belso"

    # LLM providers
    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    MISTRAL = "mistral"
    LANGCHAIN = "langchain"

    # Serialization formats
    JSON = "json"
    XML = "xml"
    YAML = "yaml"

    @classmethod
    def get_all_formats(cls) -> list:
        """
        Get a list of all supported providers.\n
        ---
        ### Returns
        - `list`: a list of all provider constants.
        """
        return [
            cls.BELSO,
            cls.GOOGLE,
            cls.OPENAI,
            cls.ANTHROPIC,
            cls.OLLAMA,
            cls.HUGGINGFACE,
            cls.MISTRAL,
            cls.LANGCHAIN,
            cls.JSON,
            cls.XML,
            cls.YAML
        ]

_JSON_TYPE_MAP = _XML_TYPE_MAP = _YAML_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "any": Any
}

_OLLAMA_FIELD_MAP = _MISTRAL_FIELD_MAP = _LANGCHAIN_FIELD_MAP = _HUGGINGFACE_FIELD_MAP = _ANTHROPIC_FIELD_MAP =   {
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

_OPENAI_FIELD_MAP = {
    "enum": ("enum", None),
    "regex": ("pattern", None),
    "multiple_of": ("multipleOf", None),
    "format_": ("format", None),
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
