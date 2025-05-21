import React from "react";
import SchemaTab from "./SchemaTab";
import "./styles.css";

export default function SchemaTabList({
  schemas,
  selectedIdx,
  onSelectSchema,
  onRenameSchema,
  onRemoveSchema,
  onAddSchema
}) {
  return (
    <div className="schema-tab-list">
      <div className="schema-tabs">
        {schemas.map((schema, idx) => (
          <SchemaTab
            key={idx}
            schema={schema}
            index={idx}
            isSelected={idx === selectedIdx}
            onSelect={onSelectSchema}
            onRename={onRenameSchema}
            onRemove={onRemoveSchema}
            canRemove={schemas.length > 1}
          />
        ))}
      </div>
      <button className="add-schema-button" onClick={onAddSchema}>+ Add schema</button>
    </div>
  );
}
