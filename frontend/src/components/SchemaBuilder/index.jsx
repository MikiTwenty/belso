import React, { useState, useEffect } from "react";
import SchemaTabList from "./SchemaTabList";
import FieldList from "./FieldList";
import { emptyField } from "./constants";
import "./styles.css";

export default function SchemaBuilder() {
  // --- State for multiple schemas (tabs) ---
  const [schemas, setSchemas] = useState([
    { name: "Schema1", fields: [emptyField()] }
  ]);
  const [selectedIdx, setSelectedIdx] = useState(0);

  // --- Schema management functions ---
  function addSchema() {
    setSchemas([...schemas, { name: `Schema${schemas.length + 1}`, fields: [emptyField()] }]);
    setSelectedIdx(schemas.length); // auto-switch to new tab
  }

  function renameSchema(idx, newName) {
    setSchemas(schemas.map((s, i) => i === idx ? { ...s, name: newName } : s));
  }

  function removeSchema(idx) {
    if (schemas.length === 1) return;
    const next = idx > 0 ? idx - 1 : 0;
    setSchemas(schemas.filter((_, i) => i !== idx));
    setSelectedIdx(next);
  }

  // --- Field management functions ---
  function handleFieldChange(idx, prop, value) {
    let fields = [...schemas[selectedIdx].fields];
    // If switching type, reset type-specific params
    if (prop === "type") {
      fields[idx] = { ...emptyField(value), name: fields[idx].name };
    } else {
      fields[idx][prop] = value;
    }
    updateFields(fields);
  }

  // --- Nested schema reference support ---
  function handleFieldSchemaRef(idx, schemaName) {
    let fields = [...schemas[selectedIdx].fields];
    fields[idx].schemaRef = schemaName;
    updateFields(fields);
  }

  function updateFields(fields) {
    setSchemas(schemas.map((s, i) => i === selectedIdx ? { ...s, fields } : s));
  }

  function addField(type = "string") {
    updateFields([...schemas[selectedIdx].fields, emptyField(type)]);
  }

  function removeField(idx) {
    updateFields(schemas[selectedIdx].fields.filter((_, i) => i !== idx));
  }

  // --- Generate schema output ---
  function generateSchemaOutput() {
    // Process the schemas to handle nested fields properly
    const processedSchemas = schemas.map(schema => {
      return {
        ...schema,
        fields: schema.fields.map(processField)
      };
    });

    return JSON.stringify(processedSchemas, null, 2);
  }

  // Process field to handle nested fields and enum values
  function processField(field) {
    const processed = { ...field };

    // Parse enum values if they exist
    if (field.enum && typeof field.enum === 'string') {
      processed.enum = field.enum.split(',').map(item => item.trim()).filter(Boolean);
    }

    // Handle nested fields for objects
    if (field.type === 'object' && Array.isArray(field.fields)) {
      processed.fields = field.fields.map(processField);
    }

    // Handle array item type
    if (field.type === 'array' && field.items_type) {
      processed.items_type = field.items_type;
    }

    return processed;
  }

  return (
    <div className="schema-builder-root">
      <div className="schema-tabs">
        {/* Schema Tabs */}
        <SchemaTabList
          schemas={schemas}
          selectedIdx={selectedIdx}
          onSelectSchema={setSelectedIdx}
          onRenameSchema={renameSchema}
          onRemoveSchema={removeSchema}
          onAddSchema={addSchema}
        />
      </div>
      <div className="schema-layout">
        {/* Field List - Left Column */}
        <div className="schema-content">
          <h3>Schema Builder</h3>
          <FieldList
            fields={schemas[selectedIdx].fields}
            onFieldChange={handleFieldChange}
            onRemoveField={removeField}
            onAddField={addField}
            schemas={schemas}
            selectedSchemaIdx={selectedIdx}
            onFieldSchemaRef={handleFieldSchemaRef}
          />
        </div>
        {/* Schema Output - Right Column */}
        <div className="schema-output">
          <h3>Schema Visualizer</h3>
          <pre className="output-preview" style={{maxHeight: 'calc(100vh - 120px)', overflow: 'auto'}}>
            {generateSchemaOutput()}
          </pre>
        </div>
      </div>
    </div>
  );
}
