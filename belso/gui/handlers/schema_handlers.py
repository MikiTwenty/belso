# belso.gui.handlers.schema_handlers

import logging
from typing import Tuple

from belso.gui.state import GUIState

logger = logging.getLogger(__name__)

def handle_add_schema(state: GUIState) -> Tuple[GUIState, str]:
    """
    Adds a new empty schema to the editor.\n
    ---
    ### Args
    - `state` (`GUIState`): the current GUI state.\n
    ---
    ### Returns
    - `Tuple[GUIState, str]`: the updated GUI state and the name of the new schema.
    """
    logger.info(f"Adding new schema...")
    state.create_schema()
    logger.info(f"New schema added: \"{state.active_schema_name}\".")
    return state.clone(), state.active_schema_name

def handle_rename_schema(
        state: GUIState,
        old_name: str,
        new_name: str
    ) -> GUIState:
    """
    Renames a schema in the GUI state.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `old_name` (`str`): The current name of the schema.
    - `new_name` (`str`): The new name for the schema.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    logger.info(f"Handling rename schema request: from \"{old_name}\" to \"{new_name}\".")
    if not new_name.strip():
        logger.warning("New schema name cannot be empty.")
        return state.clone()

    success = state.rename_schema(old_name, new_name)
    if success:
        logger.info(f"Schema renamed from \"{old_name}\" to \"{new_name}\".")
    else:
        logger.warning(f"Failed to rename schema from \"{old_name}\" to \"{new_name}\".")
    return state.clone()

def handle_switch_schema(
        state: GUIState,
        schema_name: str
    ) -> GUIState:
    """
    Set the active tab to the selected schema.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema_name` (`str`): The schema name to switch to.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    logger.info(f"Switching to schema: \"{schema_name}\".")
    if schema_name in state.schemas:
        state.active_schema_name = schema_name
        logger.info(f"Switched to schema: \"{schema_name}\".")
    else:
        logger.warning(f"Schema not found: \"{schema_name}\".")
    return state.clone()
