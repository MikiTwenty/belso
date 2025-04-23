from typing import Type, Optional

from belso.schemas import Schema, Field
from belso.utils.logging import get_logger

logger = get_logger(__name__)

class NestedField(Field):
    """
    Field class for nested schemas.
    """
    def __init__(
            self,
            name: str,
            schema: Type[Schema],
            description: str = "",
            required: bool = True
        ) -> None:
        """
        Initialize a nested field.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `schema` (`Type[Schema]`): the nested schema.
        - `description` (`Optional[str]`): the description of the field. Defaults to an empty string.
        - `required` (`Optional[bool]`): whether the field is required. Defaults to `True`.
        """
        super().__init__(name=name, type=dict, description=description, required=required)
        self.schema = schema

class ArrayField(Field):
    """
    Field class for arrays of items.
    """
    def __init__(
            self,
            name: str,
            items_type: Type = str,
            items_schema: Optional[Type[Schema]] = None,
            description: str = "",
            required: bool = True
        ) -> None:
        """
        Initialize an array field.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `items_type` (`Type`, optional): the type of items in the array. Defaults to `str`.
        - `items_schema` (`Type[Schema]`, optional): the schema of items in the array. Defaults to `None`.
        - `description` (`str`, optional): the description of the field. Defaults to an empty string.
        - `required` (`bool`, optional): whether the field is required. Defaults to `True`.
        """
        super().__init__(name=name, type=list, description=description, required=required)
        self.items_type = items_type
        self.items_schema = items_schema
