import React from "react";
import FieldEditor from "./FieldEditor";

export default function FieldList({ fields, onFieldChange, onRemoveField, onAddField, schemas, selectedSchemaIdx, onFieldSchemaRef }) {
  return (
    <div>
      {fields.map((field, idx) => (
        <FieldEditor
          key={idx}
          field={field}
          index={idx}
          onFieldChange={onFieldChange}
          onRemoveField={onRemoveField}
          schemas={schemas}
          selectedSchemaIdx={selectedSchemaIdx}
          onFieldSchemaRef={onFieldSchemaRef}
        />
      ))}
      <div style={{ margin: "10px 0" }}>
        <button onClick={() => onAddField()}>+ Add Field</button>
      </div>
    </div>
  );
}
