# belso.gui.state

import copy
import logging
from typing import Dict, Optional, Type

from belso.core.schema import Schema
from belso.core.field import BaseField

logger = logging.getLogger(__name__)

class GUIState:
    """
    Represents the global state of the GUI.
    Handles schema creation, selection, and field editing state.\n
    ---
    ### Attributes
    - `schemas` (`Dict[str, Type[Schema]]`): All defined schemas by name.
    - `active_schema_name` (`Optional[str]`): Currently selected tab/schema name.
    - `selected_field` (`Optional[BaseField]`): Field selected for editing.
    - `_counter` (`int`): Internal counter for unique schema names.
    """
    def __init__(self) -> None:
        self.schemas: Dict[str, Type[Schema]] = {}
        self.active_schema_name: Optional[str] = None
        self.selected_field: Optional[BaseField] = None
        self._counter: int = 1
        logger.debug("GUI state initialized.")

    def create_schema(
            self,
            name: Optional[str] = None
        ) -> str:
        """
        Create a new empty schema with a unique name if not provided.\n
        ---
        ### Args
        - `name` (`Optional[str]`): Custom schema name (default: SchemaN).\n
        ---
        ### Returns
        - `str`: The name of the created schema.
        """
        logger.debug(f"Creating new schema: \"{name}\".")
        if not name:
            name = f"Schema{self._counter}"
            logger.debug(f"No name provided, using default name: \"{name}\".")
        while name in self.schemas:
            self._counter += 1
            name = f"Schema{self._counter}"
            logger.debug(f"Name already exists, using default name: \"{name}\".")

        # Define a new Schema subclass dynamically
        class NewSchema(Schema):
            fields = []

        NewSchema.__name__ = name
        self.schemas[name] = NewSchema
        self.active_schema_name = name
        self._counter += 1
        return name

    def delete_schema(
            self,
            name: str
        ) -> None:
        """
        Remove a schema from the state.\n
        ---
        ### Args
        - `name` (`str`): Schema name to delete.
        """
        logger.debug(f"Deleting schema \"{name}\"...")
        if name in self.schemas:
            del self.schemas[name]
            if self.active_schema_name == name:
                self.active_schema_name = next(iter(self.schemas), None)

    def get_active_schema(self) -> Optional[Type[Schema]]:
        """
        Retrieve the currently selected schema.\n
        ---
        ### Returns
        - `Optional[Type[Schema]]`: Active schema or None.
        """
        logger.debug(f"Getting active schema: \"{self.active_schema_name}\".")
        return self.schemas.get(self.active_schema_name)

    def set_selected_field(
            self,
            field: Optional[BaseField]
        ) -> None:
        """
        Set the currently selected field (for editing).\n
        ---
        ### Args
        - `field` (`Optional[BaseField]`): Field object or None.
        """
        logger.debug(f"Setting selected field: \"{field}\".")
        self.selected_field = field

    def clone(self) -> "GUIState":
        """
        Clone the entire GUI state (used for deep updates).\n
        ---
        ### Returns
        - `GUIState`: A deep copy of the GUI state.
        """
        logger.debug("Cloning GUI state...")
        return copy.deepcopy(self)
