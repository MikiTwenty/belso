# belso.gui.components.schema_tree

import logging
from typing import Type

import gradio as gr

from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.core.field import NestedField, ArrayField
from belso.gui.handlers import handle_edit_field, handle_remove_field

logger = logging.getLogger(__name__)

def render_schema_tree(
        schema: Type[Schema],
        state_component: gr.State,
        state: GUIState,
        depth: int = 0
    ) -> None:
    """
    Renders a tree view of fields in the given schema.
    Recursively handles nested fields.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): The schema whose fields to display.
    - `state_component` (`gr.State`): The state component for the GUI.
    - `state` (`GUIState`): The current GUI state.
    - `depth` (`int`): Level of indentation for nested fields.
    """
    if not schema or not hasattr(schema, "fields"):
        logger.warning(f"Invalid schema: {schema}")
        return

    for field in schema.fields:
        indent = "&nbsp;" * (depth * 4)
        label = f"{indent}🔹 <b>{field.name}</b> ({field.type_.__name__})"

        with gr.Row():
            gr.HTML(label)
            gr.Button("✏️", size="sm", elem_id=f"edit-{schema.__name__}-{field.name}").click(
                fn=lambda s,
                current_field=field: handle_edit_field(s, current_field), # Use current_field in lambda
                inputs=[state_component],
                outputs=[state_component],
            )

            gr.Button("🗑️", size="sm", elem_id=f"del-{schema.__name__}-{field.name}").click(
                fn=lambda s,
                current_schema=schema,
                current_field=field:handle_remove_field(s, current_schema, current_field), # Use current_schema and current_field
                inputs=[state_component],
                outputs=[state_component],
            )

        # Handle nested schema or array of schema
        if isinstance(field, NestedField):
            render_schema_tree(field.schema, state_component, state, depth + 1)
        elif isinstance(field, ArrayField):
            # If item type is a schema, render it
            if hasattr(field.items_type, "fields"): # Check if items_type is a class with fields
                render_schema_tree(field.items_type, state_component, state, depth + 1)
