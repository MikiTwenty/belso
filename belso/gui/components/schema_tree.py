# belso.gui.components.schema_tree

from typing import Type

import gradio as gr

from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.core.field import NestedField, ArrayField
from belso.gui.events import handle_edit_field, handle_remove_field

def render_schema_tree(
        schema: Type[Schema],
        state: GUIState,
        depth: int = 0
    ) -> None:
    """
    Renders a tree view of fields in the given schema.
    Recursively handles nested fields.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): The schema whose fields to display.
    - `state` (`GUIState`): The current GUI state.
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
                lambda f=field: handle_edit_field(state, schema, f),
                outputs=[],
            )
            gr.Button("🗑️", elem_id=f"del-{field.name}").click(
                lambda f=field: handle_remove_field(state, schema, f),
                outputs=[]
            )

        # Handle nested schema or array of schema
        if isinstance(field, NestedField):
            render_schema_tree(field.schema, state, depth + 1)
        elif isinstance(field, ArrayField):
            # If item type is a schema, render it
            if hasattr(field.items_type, "fields"):
                render_schema_tree(field.items_type, state, depth + 1)
