# belso.gui.handlers.field_handlers

import logging

from belso.core.field import Field
from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP

logger = logging.getLogger(__name__)

def handle_add_field(
        name: str,
        type_: str,
        desc: str,
        req: str,
        default: str,
        state: GUIState
    ) -> GUIState:
    """
    Open the field editor to add a new field.\n
    ---
    ### Args
    - `name` (`str`): The name of the field.
    - `type_` (`str`): The type of the field.
    - `desc` (`str`): The description of the field.
    - `req` (`bool`): Whether the field is required.
    - `default` (`str`): The default value of the field.
    - `state` (`GUIState`): The current GUI state.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    schema = state.get_active_schema()
    if not schema:
        logger.warning("No active schema found.")
        return state.clone()

    py_type = _FILE_TYPE_MAP.get(type_, str)
    new_field = Field(name, py_type, desc, req, default or None)

    if state.selected_field:
        logger.info("Editing existing field...")
        # Edit mode
        schema.fields = [
            new_field if f.name == state.selected_field.name else f
            for f in schema.fields
        ]
    else:
        logger.info("Adding new field...")
        schema.fields.append(new_field)

    state.set_selected_field(None)
    return state.clone()

def handle_edit_field(
        state: GUIState,
        field: Field
    ) -> GUIState:
    """
    Open the field editor to edit an existing field.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
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
    logger.info(f"Removing field \"{field.name}\" from schema \"{schema.name}\".")
    try:
        schema.fields = [f for f in schema.fields if f.name != field.name]
        logger.info("Field removed successfully.")
        return state.clone()
    except Exception as e:
        logger.error(f"Errore nella rimozione campo: {e}")
