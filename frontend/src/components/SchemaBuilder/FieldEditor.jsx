import React from "react";
import { getAllowedParams, FIELD_TYPES, emptyField } from "./constants";
import "./styles.css";

export default function FieldEditor({ field, index, onFieldChange, onRemoveField, schemas = [], selectedSchemaIdx = 0, onFieldSchemaRef }) {
  const allowedParams = getAllowedParams(field.type);
  // For nested schema selection
  const schemaOptions = schemas.filter((_, idx) => idx !== selectedSchemaIdx);

  // Only show param if value is not undefined, null, or empty string
  function showParam(param) {
    return allowedParams.includes(param) && field[param] !== undefined && field[param] !== null && field[param] !== "";
  }

  return (
    <div className="field-editor">
      <div className="field-editor-header">
        <input
          className="field-name-input"
          placeholder="Field name"
          value={field.name}
          onChange={e => onFieldChange(index, "name", e.target.value)}
        />
        <select
          className="field-type-select"
          value={field.type}
          onChange={e => onFieldChange(index, "type", e.target.value)}
        >
          {FIELD_TYPES.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
        <label className="field-required-label">
          <input
            type="checkbox"
            checked={!!field.required}
            onChange={e => onFieldChange(index, "required", e.target.checked)}
          /> Required
        </label>
        <button className="field-remove-button" onClick={() => onRemoveField(index)}>Remove</button>
      </div>

      {/* Dynamic params - only show if value is specified or being edited */}
      <div className="field-params">
        {showParam("description") && (
          <div className="field-param-container" style={{ flex: 1, minWidth: 200 }}>
            <label>Description:</label>
            <input
              placeholder="Field description"
              value={field.description}
              onChange={e => onFieldChange(index, "description", e.target.value)}
            />
          </div>
        )}
        {showParam("default") && (
          <div className="field-param-container">
            <label>Default Value:</label>
            <input
              placeholder="Default value"
              value={field.default}
              onChange={e => onFieldChange(index, "default", e.target.value)}
            />
          </div>
        )}
        {/* Repeat for all other params, using showParam(param) */}
        {allowedParams.includes("enum") && (field.enum || field.enum === "") && (
          <div className="field-param-container">
            <label>Enum Values:</label>
            <input
              placeholder="Value1, Value2, Value3"
              value={field.enum}
              onChange={e => {
                onFieldChange(index, "enum", e.target.value);
              }}
              style={{ width: 180 }}
              title="Enter values separated by commas"
            />
          </div>
        )}
        {allowedParams.includes("range_") && (field.range_ || field.range_ === "") && (
          <div className="field-param-container">
            <label>Range (min,max):</label>
            <input
              placeholder="0,100"
              value={field.range_}
              onChange={e => onFieldChange(index, "range_", e.target.value)}
            />
          </div>
        )}
        {allowedParams.includes("exclusive_range") && (field.exclusive_range || field.exclusive_range === "") && (
          <div className="field-param-container">
            <label>Exclusive Range:</label>
            <input
              placeholder="true,false"
              value={field.exclusive_range}
              onChange={e => onFieldChange(index, "exclusive_range", e.target.value)}
            />
          </div>
        )}
        {allowedParams.includes("length_range") && (field.length_range || field.length_range === "") && (
          <div className="field-param-container">
            <label>Length Range:</label>
            <input
              placeholder="1,100"
              value={field.length_range}
              onChange={e => onFieldChange(index, "length_range", e.target.value)}
            />
          </div>
        )}
        {allowedParams.includes("items_range") && (field.items_range || field.items_range === "") && (
          <div className="field-param-container">
            <label>Items Range:</label>
            <input
              placeholder="1,10"
              value={field.items_range}
              onChange={e => onFieldChange(index, "items_range", e.target.value)}
            />
          </div>
        )}
        {allowedParams.includes("properties_range") && (field.properties_range || field.properties_range === "") && (
          <div className="field-param-container">
            <label>Properties Range:</label>
            <input
              placeholder="1,10"
              value={field.properties_range}
              onChange={e => onFieldChange(index, "properties_range", e.target.value)}
            />
          </div>
        )}
        {allowedParams.includes("regex") && (field.regex || field.regex === "") && (
          <div className="field-param-container">
            <label>Regex Pattern:</label>
            <input
              placeholder="^[a-z]+$"
              value={field.regex}
              onChange={e => onFieldChange(index, "regex", e.target.value)}
            />
          </div>
        )}
        {allowedParams.includes("multiple_of") && (field.multiple_of || field.multiple_of === "") && (
          <div className="field-param-container">
            <label>Multiple Of:</label>
            <input
              placeholder="2"
              value={field.multiple_of}
              onChange={e => onFieldChange(index, "multiple_of", e.target.value)}
            />
          </div>
        )}
        {allowedParams.includes("format_") && (field.format_ || field.format_ === "") && (
          <div className="field-param-container">
            <label>Format:</label>
            <input
              placeholder="email"
              value={field.format_}
              onChange={e => onFieldChange(index, "format_", e.target.value)}
            />
          </div>
        )}
      </div>

      {/* Nested schema reference for object type */}
      {field.type === "object" && schemaOptions.length > 0 && (
        <div className="field-param-container">
          <label>Reference Schema:</label>
          <select
            value={field.schemaRef || ""}
            onChange={e => onFieldSchemaRef(index, e.target.value)}
          >
            <option value="">-- None --</option>
            {schemaOptions.map((schema, idx) => (
              <option key={schema.name} value={schema.name}>{schema.name}</option>
            ))}
          </select>
        </div>
      )}

      {/* Nested fields for object type if not referencing another schema */}
      {field.type === "object" && !field.schemaRef && field.fields && (
        <div className="nested-fields-container">
          <h4>Nested Fields (Schema: {field.name || "Unnamed"})</h4>
          <NestedFieldList
            fields={field.fields}
            onFieldsChange={(nestedFields) => onFieldChange(index, "fields", nestedFields)}
            schemas={schemas}
            selectedSchemaIdx={selectedSchemaIdx}
          />
        </div>
      )}

      {/* Items type for array */}
      {field.type === "array" && (
        <div className="array-items-type">
          <div className="field-param-container">
            <label>Items Type:</label>
            <select
              className="array-items-select"
              value={field.items_type || "string"}
              onChange={e => onFieldChange(index, "items_type", e.target.value)}
            >
              {FIELD_TYPES.filter(t => t !== "array").map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
        </div>
      )}
    </div>
  );
}

// Helper component for nested fields
function NestedFieldList({ fields, onFieldsChange, schemas = [], selectedSchemaIdx = 0 }) {
  function handleNestedFieldChange(idx, prop, value) {
    const updatedFields = [...fields];
    if (prop === "type") {
      const currentName = updatedFields[idx].name;
      const currentRequired = updatedFields[idx].required;
      updatedFields[idx] = emptyField(value);
      updatedFields[idx].name = currentName;
      updatedFields[idx].required = currentRequired;
    } else {
      updatedFields[idx][prop] = value;
    }
    onFieldsChange(updatedFields);
  }

  function addNestedField() {
    onFieldsChange([...fields, emptyField("string")]);
  }

  function removeNestedField(idx) {
    onFieldsChange(fields.filter((_, i) => i !== idx));
  }

  // For nested schema selection
  const schemaOptions = schemas.filter((_, idx) => idx !== selectedSchemaIdx);

  return (
    <div className="nested-fields-list">
      {fields.map((field, idx) => (
        <div key={idx} className="nested-field-item">
          <div className="nested-field-header">
            <input
              className="nested-field-name"
              placeholder="Field name"
              value={field.name}
              onChange={e => handleNestedFieldChange(idx, "name", e.target.value)}
            />
            <select
              className="nested-field-type"
              value={field.type}
              onChange={e => handleNestedFieldChange(idx, "type", e.target.value)}
            >
              {FIELD_TYPES.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
            <label className="nested-field-required">
              <input
                type="checkbox"
                checked={!!field.required}
                onChange={e => handleNestedFieldChange(idx, "required", e.target.checked)}
              /> Required
            </label>
            <button
              className="nested-field-remove"
              onClick={() => removeNestedField(idx)}
            >
              Remove
            </button>
          </div>
          {/* Show description field for all nested fields */}
          <input
            className="nested-field-description"
            placeholder="Description"
            value={field.description || ""}
            onChange={e => handleNestedFieldChange(idx, "description", e.target.value)}
          />
          {/* Nested schema reference for object type */}
          {field.type === "object" && schemaOptions.length > 0 && (
            <div className="field-param-container">
              <label>Reference Schema:</label>
              <select
                value={field.schemaRef || ""}
                onChange={e => handleNestedFieldChange(idx, "schemaRef", e.target.value)}
              >
                <option value="">-- None --</option>
                {schemaOptions.map((schema, idx) => (
                  <option key={schema.name} value={schema.name}>{schema.name}</option>
                ))}
              </select>
            </div>
          )}
          {/* Handle nested objects recursively if not referencing another schema */}
          {field.type === "object" && !field.schemaRef && (
            <div className="nested-fields-container" style={{ marginLeft: "1rem" }}>
              <h4>Sub-Schema: {field.name || "Unnamed"}</h4>
              <NestedFieldList
                fields={field.fields || []}
                onFieldsChange={(nestedFields) => handleNestedFieldChange(idx, "fields", nestedFields)}
                schemas={schemas}
                selectedSchemaIdx={selectedSchemaIdx}
              />
            </div>
          )}
        </div>
      ))}
      <button
        className="add-nested-field-button"
        onClick={addNestedField}
      >
        + Add Nested Field
      </button>
    </div>
  );
}
