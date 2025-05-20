# belso.gui.logic.state

"""
State management module for Belso GUI.
---
This module handles the global state of the UI: current schema, field stack,
breadcrumb navigation, and cached schema list.
"""

from typing import List, Optional
from belso.core.schema import Schema
from belso.utils.logging import get_logger

logger = get_logger(__name__)

class SchemaState:
    """
    Centralized state container for the schema building session.
    """

    def __init__(self) -> None:
        """
        Initializes the schema state.
        """
        self._breadcrumb_stack: List[str] = []
        self._schemas: dict[str, type[Schema]] = {}
        self._current_schema_name: Optional[str] = None
        self._fields_buffer: List = []  # temporary fields for current schema

    def reset(self) -> None:
        """
        Resets the entire state.
        """
        self._breadcrumb_stack.clear()
        self._schemas.clear()
        self._fields_buffer.clear()
        self._current_schema_name = None
        logger.debug("Schema state has been reset.")

    # --- Breadcrumb Navigation ---

    def push_schema(self, name: str):
        """
        Pushes a new schema onto the breadcrumb stack.\n
        ---
        ### Args
        - `name` (`str`): the schema name to push.
        """
        if name not in self._breadcrumb_stack:
            self._breadcrumb_stack.append(name)
        self._current_schema_name = name
        logger.debug(f"Pushed schema to breadcrumb: {name}")

    def pop_schema(self) -> Optional[str]:
        """
        Pops the last schema from the breadcrumb stack.\n
        ---
        ### Returns
        - `Optional[str]`: the new current schema name or None.
        """
        if self._breadcrumb_stack:
            popped = self._breadcrumb_stack.pop()
            logger.debug(f"Popped schema from breadcrumb: {popped}")

        self._current_schema_name = self._breadcrumb_stack[-1] if self._breadcrumb_stack else None
        return self._current_schema_name

    def get_breadcrumb(self) -> List[str]:
        """
        Returns the full breadcrumb path.\n
        ---
        ### Returns
        - `List[str]`: breadcrumb stack.
        """
        return list(self._breadcrumb_stack)

    # --- Schema Metadata ---

    def set_current_schema(self, name: str):
        """
        Sets the current schema by name (without altering breadcrumb).
        """
        self._current_schema_name = name

    def get_current_schema_name(self) -> Optional[str]:
        """
        Gets the name of the currently active schema.\n
        ---
        ### Returns
        - `Optional[str]`: name of current schema.
        """
        return self._current_schema_name

    def get_all_schemas(self) -> List[str]:
        """
        Returns the names of all available schemas.\n
        ---
        ### Returns
        - `List[str]`: all schema names.
        """
        return list(self._schemas.keys())

    def get_schema(self, name: str) -> Optional[type[Schema]]:
        """
        Returns the schema object by name.
        ---
        ### Args
        - `name` (`str`): schema name.
        ---
        ### Returns
        - `Optional[type[Schema]]`: schema class.
        """
        return self._schemas.get(name)

    def set_schema(self, name: str, schema: type[Schema]):
        """
        Registers a schema in the global state.
        ---
        ### Args
        - `name` (`str`): schema name.
        - `schema` (`type[Schema]`): schema class.
        """
        self._schemas[name] = schema
        logger.debug(f"Schema '{name}' registered.")

    # --- Fields Buffer ---

    def set_fields(self, fields: List):
        self._fields_buffer = fields

    def get_fields(self) -> List:
        return self._fields_buffer

    def clear_fields(self):
        self._fields_buffer.clear()


# Global state instance
state = SchemaState()
