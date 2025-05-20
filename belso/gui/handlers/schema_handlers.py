# belso.gui.handlers.schema_handlers

from belso.gui.state import GUIState

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
    state.create_schema()
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
    if schema_name in state.schemas:
        state.active_schema_name = schema_name
    return state.clone()
