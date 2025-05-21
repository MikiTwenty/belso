// Field type parameters mapping
export const FIELD_PARAMS = {
  string:    ["enum", "length_range", "regex", "format_"],
  int:       ["enum", "range_", "exclusive_range", "multiple_of"],
  float:     ["enum", "range_", "exclusive_range", "multiple_of"],
  bool:      ["enum"],
  array:     ["enum", "items_range"],
  object:    ["enum", "properties_range"],
  any:       ["enum"],
};

export const COMMON_PARAMS = ["description", "required", "default"];

// Field type options for dropdown
export const FIELD_TYPES = Object.keys(FIELD_PARAMS);

// Utility to get all valid params for a field type
export function getAllowedParams(type) {
  return Array.from(new Set([...(FIELD_PARAMS[type] || FIELD_PARAMS.any), ...COMMON_PARAMS]));
}

// Default empty field for new field creation
export function emptyField(type = "string") {
  return {
    name: "",
    type,
    required: true,
    description: "",
    default: undefined,
    enum: undefined,
    range_: undefined,
    exclusive_range: undefined,
    multiple_of: undefined,
    length_range: undefined,
    items_range: undefined,
    properties_range: undefined,
    regex: undefined,
    format_: undefined,
    // For nested schemas
    fields: type === "object" ? [] : undefined,
    items_type: type === "array" ? "string" : undefined,
    schemaRef: undefined,
  };
}
