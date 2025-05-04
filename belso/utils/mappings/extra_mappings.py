# belso.utils.mappings.extra_mappings

from belso.providers import (
    to_google, from_google,
    to_ollama, from_ollama,
    to_openai, from_openai,
    to_anthropic, from_anthropic,
    to_langchain, from_langchain,
    to_huggingface, from_huggingface,
    to_mistral, from_mistral
)
from belso.serialization import (
    to_json, from_json,
    to_xml, from_xml,
    to_yaml, from_yaml
)
from belso.utils.formats import FORMATS

_CONVERT_TO_MAP = {
    FORMATS.GOOGLE: to_google,
    FORMATS.OLLAMA: to_ollama,
    FORMATS.OPENAI: to_openai,
    FORMATS.ANTHROPIC: to_anthropic,
    FORMATS.LANGCHAIN: to_langchain,
    FORMATS.HUGGINGFACE: to_huggingface,
    FORMATS.MISTRAL: to_mistral,
    FORMATS.JSON: to_json,
    FORMATS.XML: to_xml,
    FORMATS.YAML: to_yaml,
}

_CONVERT_FROM_MAP = {
    FORMATS.GOOGLE: from_google,
    FORMATS.OLLAMA: from_ollama,
    FORMATS.OPENAI: from_openai,
    FORMATS.ANTHROPIC: from_anthropic,
    FORMATS.LANGCHAIN: from_langchain,
    FORMATS.HUGGINGFACE: from_huggingface,
    FORMATS.MISTRAL: from_mistral,
    FORMATS.JSON: from_json,
    FORMATS.XML: from_xml,
    FORMATS.YAML: from_yaml,
}

_SAVE_TO_MAP = {
    ".json": to_json,
    ".xml": to_xml,
    ".yaml": to_yaml,
    ".yml": to_yaml,
}

_LOAD_FROM_MAP = {
    ".json": from_json,
    ".xml": from_xml,
    ".yaml": from_yaml,
    ".yml": from_yaml,
}
