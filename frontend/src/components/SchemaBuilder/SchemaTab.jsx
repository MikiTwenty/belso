import React from "react";
import "./styles.css";

export default function SchemaTab({
  schema,
  index,
  isSelected,
  onSelect,
  onRename,
  onRemove,
  canRemove
}) {
  return (
    <div
      className={`schema-tab ${isSelected ? 'selected' : ''}`}
      onClick={() => onSelect(index)}
    >
      <input
        className="schema-tab-input"
        value={schema.name}
        onChange={e => onRename(index, e.target.value)}
      />
      {canRemove && (
        <button
          className="schema-tab-remove"
          onClick={e => {
            e.stopPropagation();
            onRemove(index);
          }}
        >
          ×
        </button>
      )}
    </div>
  );
}
