# belso.gui.utils

"""
DynamicField Class
---
Temporary field representation during UI schema editing, later converted into proper Field instances.
"""

from typing import List, Optional, Tuple
from belso.utils.logging import get_logger

_logger = get_logger(__name__)

class DynamicField:
    def __init__(
            self,
            name: str,
            type_: str,
            description: str,
            required: bool = True,
            enum: Optional[List[str]] = None,
            regex: Optional[str] = None,
            range_: Optional[Tuple[float, float]] = None,
            multiple_of: Optional[float] = None,
            length_range: Optional[Tuple[int, int]] = None,
            items_range: Optional[Tuple[int, int]] = None,
            nested_schema: Optional[str] = None,
            items_type: Optional[str] = None,
            default: Optional[any] = None
        ) -> None:
        """
        Dynamic field constructor.
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `type_` (`str`): the type of the field.
        - `description` (`str`): the description of the field.
        - `required` (`bool`, optional): whether the field is required. Defaults to `True`.
        - `enum` (`List[str]`, optional): list of allowed values.
        - `regex` (`str`, optional): regex pattern for validation.
        - `range_` (`Tuple[float, float]`, optional): value range.
        - `multiple_of` (`float`, optional): restrict to multiples.
        - `length_range` (`Tuple[int, int]`, optional): string length range.
        - `items_range` (`Tuple[int, int]`, optional): list item count range.
        - `nested_schema` (`str`, optional): reference to nested schema.
        - `items_type` (`str`, optional): type of array items.
        - `default` (`any`, optional): default value (used for export consistency).
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
        self.default = default

        _logger.debug(f"Dynamic field '{name}' initialized of type '{type_}'")
