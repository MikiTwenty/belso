# belso.gui.logic.handlers

"""
Event Handlers for Gradio interactions in Belso GUI.
---
Defines logic for buttons, dropdown changes, and field/table updates.
"""

from belso.gui.logic.state import state
from belso.gui.logic.schema_manager import (
    create_schema,
    get_schema_fields,
    export_schema,
    import_schema_from_json
)
from belso.gui.logic.field_builder import build_field_from_inputs
from belso.gui.components.schema_toolbar import refresh_breadcrumb

import gradio as gr

def on_create_schema(name: str) -> tuple:
    """
    Creates a new schema and updates dropdown and breadcrumb.\n
    ---
    ### Args
    - `name` (`str`): name of the new schema.\n
    ---
    ### Returns
    - `tuple`: updated dropdown choices and value.
    """
    if not name:
        return gr.update(),  # no change

    create_schema(name)
    state.push_schema(name)
    return gr.update(choices=state.get_all_schemas(), value=name), refresh_breadcrumb()

def on_schema_change(name: str) -> list:
    """
    Updates the field table when a schema is selected.\n
    ---
    ### Args
    - `name` (`str`): selected schema name.\n
    ---
    ### Returns
    - `list`: updated field rows.
    """
    state.set_current_schema(name)
    return get_schema_fields(name)

def on_add_field(*inputs) -> tuple:
    """
    Adds a field to the current schema in progress.\n
    ---
    ### Args
    - `*inputs`: all field UI inputs.\n
    ---
    ### Returns
    - `tuple`: status message and updated field table.
    """
    field, msg = build_field_from_inputs(*inputs)
    if field:
        current_fields = state.get_fields()
        current_fields.append(field)
        state.set_fields(current_fields)

    table_data = get_schema_fields(state.get_current_schema_name())
    return msg, table_data

def on_export_schema(
        schema_name: str,
        fmt: str
    ) -> str:
    """
    Exports the schema in the selected format.\n
    ---
    ### Args
    - `schema_name` (`str`): name of the schema.
    - `fmt` (`str`): export format.\n
    ---
    ### Returns
    - `str`: schema as JSON string.
    """
    return export_schema(schema_name, fmt)

def on_import_schema(json_str: str) -> str:
    """
    Imports a schema from a JSON string.\n
    ---
    ### Args
    - `json_str` (`str`): JSON input.\n
    ---
    ### Returns
    - `str`: status message.
    """
    return import_schema_from_json(json_str)
