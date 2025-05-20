# belso.gui.components.schema_tree

from typing import Type

import gradio as gr

from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.core.field import NestedField, ArrayField
from belso.gui.handlers import handle_edit_field, handle_remove_field

def render_schema_tree(
        schema: Type[Schema],
        state_component: gr.State,
        state_value: GUIState,
        depth: int = 0
    ) -> None:
    """
    Renders a tree view of fields in the given schema.
    Recursively handles nested fields.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): The schema whose fields to display.
    - `state_component` (`gr.State`): The state component for the GUI.
    - `state_value` (`GUIState`): The current GUI state_value.
    - `depth` (`int`): Level of indentation for nested fields.
    """
    if not schema or not hasattr(schema, "fields"):
        return

    for field in schema.fields:
        indent = "&nbsp;" * (depth * 4)
        label = f"{indent}🔹 <b>{field.name}</b> ({field.type_.__name__})"

        with gr.Row():
            gr.HTML(label)
            gr.Button("✏️", elem_id=f"edit-{field.name}").click(
                fn=lambda s: handle_edit_field(s, schema, field),
                inputs=[state_component],
                outputs=[state_component],
            )

            gr.Button("🗑️", elem_id=f"del-{field.name}").click(
                fn=lambda s: handle_remove_field(s, schema, field),
                inputs=[state_component],
                outputs=[state_component],
            )

        # Handle nested schema or array of schema
        if isinstance(field, NestedField):
            render_schema_tree(field.schema, state_value, depth + 1)
        elif isinstance(field, ArrayField):
            # If item type is a schema, render it
            if hasattr(field.items_type, "fields"):
                render_schema_tree(field.items_type, state_value, depth + 1)
