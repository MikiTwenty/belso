# belso.gui.handlers.field_handlers

from typing import Optional

import gradio as gr

from belso.core.field import Field
from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP
from belso.gui.components.field_editor import open_field_editor_data

def handle_add_field(name, type_, desc, req, default, state: GUIState) -> GUIState:
    """
    Open the field editor to add a new field.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    schema = state.get_active_schema()
    if not schema:
        return state.clone()

    from belso.core.field import Field
    from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP

    py_type = _FILE_TYPE_MAP.get(type_, str)
    new_field = Field(name, py_type, desc, req, default or None)

    if state.selected_field:
        # Edit mode
        schema.fields = [
            new_field if f.name == state.selected_field.name else f
            for f in schema.fields
        ]
    else:
        schema.fields.append(new_field)

    state.set_selected_field(None)
    return state.clone()

def handle_edit_field(
        state: GUIState,
        schema: Schema,
        field: Field
    ) -> GUIState:
    """
    Open the field editor to edit an existing field.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema` (`Schema`): The schema containing the field.
    - `field` (`Field`): The field to edit.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    state.set_selected_field(field)
    return state.clone()

def handle_remove_field(
        state: GUIState,
        schema: Schema,
        field: Field
    ) -> GUIState:
    """
    Remove a field from a schema.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema` (`Schema`): The schema containing the field.
    - `field` (`Field`): The field to remove.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    try:
        schema.fields = [f for f in schema.fields if f.name != field.name]
        return state.clone()
    except Exception as e:
        print(f"Errore nella rimozione campo: {e}")
