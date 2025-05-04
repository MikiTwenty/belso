# belso.utils.mappings.field_mappings

_JSON_FIELD_MAP =   {
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

_PYDANTIC_FIELD_MAP = {
    "enum": ("enum", None),
    "regex": ("pattern", None),
    "multiple_of": ("multipleOf", None),
    "format_": ("format", None),
}
