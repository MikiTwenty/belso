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
        logger.debug("Initializing GUI state...")
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

        # Ensure the initial name is unique before creating the class
        unique_name = name
        temp_counter = self._counter
        while unique_name in self.schemas:
            temp_counter += 1
            unique_name = f"Schema{temp_counter}" if not name or name.startswith("Schema") else f"{name}{temp_counter - self._counter +1}"

        if name != unique_name :
             logger.debug(f"Name \"{name}\" already exists or is a base name, using unique name: \"{unique_name}\".")
             name = unique_name

        self._counter = temp_counter # Update main counter if it was used

        # Define a new Schema subclass dynamically
        class NewSchema(Schema):
            fields = []

        NewSchema.__name__ = name
        self.schemas[name] = NewSchema
        self.active_schema_name = name
        # Increment counter only if the base "Schema" name was used and incremented
        if name.startswith("Schema") and name[len("Schema"):].isdigit():
            self._counter = max(self._counter, int(name[len("Schema"):]) + 1)
        else:
            self._counter +=1 # general increment if a custom name was provided or for next default
        return name

    def rename_schema(
            self,
            old_name: str,
            new_name: str
        ) -> bool:
        """
        Rename a schema.\n
        ---
        ### Args
        - `old_name` (`str`): The current name of the schema.
        - `new_name` (`str`): The new name for the schema.\n
        ---
        ### Returns
        - `bool`: True if renaming was successful, False otherwise.
        """
        logger.debug(f"Attempting to rename schema \"{old_name}\" to \"{new_name}\".")
        if not new_name or not new_name.strip():
            logger.warning("New schema name cannot be empty.")
            return False
        if old_name not in self.schemas:
            logger.warning(f"Schema \"{old_name}\" not found for renaming.")
            return False
        if new_name == old_name:
            logger.info(f"New name \"{new_name}\" is the same as the old name. No change.")
            return True
        if new_name in self.schemas:
            logger.warning(f"Schema name \"{new_name}\" already exists. Cannot rename.")
            return False

        schema_obj = self.schemas.pop(old_name)
        schema_obj.__name__ = new_name # Update the internal name of the schema class
        self.schemas[new_name] = schema_obj

        if self.active_schema_name == old_name:
            self.active_schema_name = new_name
            logger.debug(f"Active schema set to \"{self.active_schema_name}\".")

        logger.info(f"Schema \"{old_name}\" renamed to \"{new_name}\" successfully.")
        return True

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
            logger.info(f"Schema \"{name}\" deleted successfully.")
            if self.active_schema_name == name:
                self.active_schema_name = next(iter(self.schemas), None)
                logger.debug(f"Active schema set to \"{self.active_schema_name}\".")
        else:
            logger.warning(f"Schema \"{name}\" not found for deletion.")

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
