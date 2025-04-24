# belso.schemas.nested

from typing import Type

from belso.schemas import Schema, BaseField
from belso.utils.logging import get_logger

logger = get_logger(__name__)

class NestedField(BaseField):
    """
    BaseField class for nested schemas.
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
        - `schema` (`Type[belso.Schema]`): the nested schema.
        - `description` (`str`): the description of the field. Defaults to an empty string.
        - `required` (`bool`): whether the field is required. Defaults to `True`.
        """
        super().__init__(name=name, type=dict, description=description, required=required)
        self.schema = schema

class ArrayField(BaseField):
    """
    BaseField class for arrays of items.
    """
    def __init__(
            self,
            name: str,
            items_type: Type = str,
            description: str = "",
            required: bool = True
        ) -> None:
        """
        Initialize an array field.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `items_type` (`Type`): the type of items in the array. Defaults to `str`.
        - `description` (`str`): the description of the field. Defaults to an empty string.
        - `required` (`bool`): whether the field is required. Defaults to `True`.
        """
        super().__init__(name=name, type=list, description=description, required=required)
        self.items_type = items_type
