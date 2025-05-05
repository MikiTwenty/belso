# belso.gui.utils

from typing import List
from belso.utils.logging import get_logger

_logger = get_logger(__name__)

class DynamicField:
    def __init__(
            self,
            name: str,
            type_: str,
            description: str,
            required: bool = True,
            enum: List[str] = None,
            regex: str = None,
            range_: tuple = None,
            multiple_of: float = None,
            length_range: tuple = None,
            items_range: tuple = None,
            nested_schema: str = None,
            items_type: str = None
        ) -> None:
        """
        Dynamic field constructor.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `type_` (`str`): the type of the field.
        - `description` (`str`): the description of the field.
        - `required` (`bool`, optional): whether the field is required. Defaults to `True`.
        - `enum` (`List[str]`, optional): the enum of the field. Defaults to `None`.
        - `regex` (`str`, optional): the regex of the field. Defaults to `None`.
        - `range_` (`tuple`, optional): the range of the field. Defaults to `None`.
        - `multiple_of` (`float`, optional): the multiple of the field. Defaults to `None`.
        - `length_range` (`tuple`, optional): the length range of the field. Defaults to `None`.
        - `items_range` (`tuple`, optional): the items range of the field. Defaults to `None`.
        - `nested_schema` (`str`, optional): the nested schema of the field. Defaults to `None`.
        - `items_type` (`str`, optional): the items type of the field. Defaults to `None`.
        """
        self.name = name
        self.type_ = type_
        self.description = description
        self.required = required
        self.enum = enum
        self.regex = regex
        self.range_ = range_
        self.multiple_of = multiple_of
        self.length_range = length_range
        self.items_range = items_range
        self.nested_schema = nested_schema
        self.items_type = items_type
        _logger.debug(f"Dynamic field {name} initialized.")
