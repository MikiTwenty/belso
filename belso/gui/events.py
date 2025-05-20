# belso.gui.events

from typing import Optional
from belso.core.field import Field
from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.gui.components.field_editor import open_field_editor


def handle_add_schema(state: GUIState) -> None:
    """
    Adds a new empty schema to the editor.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    """
    state.create_schema()

def handle_switch_schema(
        state: GUIState,
        schema_name: str
    ) -> None:
    """
    Set the active tab to the selected schema.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema_name` (`str`): The schema name to switch to.
    """
    if schema_name in state.schemas:
        state.active_schema_name = schema_name

def handle_add_field(
        state: GUIState,
        schema_name: Optional[str] = None
    ) -> None:
    """
    Open the field editor to add a new field.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema_name` (`Optional[str]`): The target schema to which the field is added.
    """
    schema = state.schemas.get(schema_name or state.active_schema_name)
    if schema:
        state.set_selected_field(None)
        open_field_editor(state, schema)

def handle_edit_field(
        state: GUIState,
        schema: Schema,
        field: Field
    ) -> None:
    """
    Open the field editor to edit an existing field.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema` (`Schema`): The schema containing the field.
    - `field` (`Field`): The field to edit.
    """
    state.set_selected_field(field)
    open_field_editor(state, schema, existing_field=field)

def handle_remove_field(
        state: GUIState,
        schema: Schema,
        field: Field
    ) -> None:
    """
    Remove a field from a schema.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema` (`Schema`): The schema containing the field.
    - `field` (`Field`): The field to remove.
    """
    try:
        schema.fields = [f for f in schema.fields if f.name != field.name]
    except Exception as e:
        print(f"Errore nella rimozione campo: {e}")
