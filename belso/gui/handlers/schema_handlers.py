# belso.gui.handlers.schema_handlers

import logging

from belso.gui.state import GUIState

logger = logging.getLogger(__name__)

def handle_add_schema(state: GUIState) -> GUIState:
    """
    Adds a new empty schema to the editor.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    logger.info(f"Adding new schema...")
    state.create_schema()
    logger.info(f"New schema added: \"{state.active_schema_name}\".")
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
