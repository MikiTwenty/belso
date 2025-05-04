# belso.core.schema

from belso.utils import get_logger
from typing import Any, List, Optional, Type, ClassVar, Tuple, final

_logger = get_logger(__name__)

@final
class BaseField:
    """
    A base class for defining fields in a schema.
    """
    __slots__ = (
        "name",
        "type_",
        "description",
        "required",
        "default",
        "enum",
        "range_",
        "exclusive_range",
        "length_range",
        "items_range",
        "properties_range",
        "regex",
        "multiple_of",
        "format_",
    )

    def __init__(
            self,
            name: str,
            type_: Type,
            description: str,
            required: bool = True,
            default: Optional[Any] = None,
            enum: Optional[List[Any]] = None,
            range_: Optional[Tuple[Any, Any]] = None,
            exclusive_range: Optional[Tuple[bool, bool]] = None,
            length_range: Optional[Tuple[int, int]] = None,
            items_range: Optional[Tuple[int, int]] = None,
            properties_range: Optional[Tuple[int, int]] = None,
            regex: Optional[str] = None,
            multiple_of: Optional[float] = None,
            format_: Optional[str] = None
        ) -> None:
        self.name = name
        self.type_ = type_
        self.description = description
        self.required = required
        self.default = default
        self.enum = enum
        self.range_ = range_
        self.exclusive_range = exclusive_range
        self.length_range = length_range
        self.items_range = items_range
        self.properties_range = properties_range
        self.regex = regex
        self.multiple_of = multiple_of
        self.format_ = format_

class Schema:
    """
    A base class for defining schemas.
    """
    fields: ClassVar[List[BaseField]] = []

    @classmethod
    def get_required_fields(cls) -> List[str]:
        """
        Get the names of all required fields in the schema.
        ---
        ### Returns
        - `List[str]`: a list of required field names.
        """
        _logger.debug(f'Getting required fields for {cls.__name__}')
        return [field.name for field in cls.fields if field.required]

    @classmethod
    def get_field_by_name(
        cls,
        name: str
    ) -> Optional[BaseField]:
        """
        Get a field by its name.
        ---
        ### Args
        - `name` (`str`): the name of the field.
        ---
        ### Returns
        - `Optional[belso.core.BaseField]`: the field with the given name, or `None` if not found.
        """
        _logger.debug(f'Getting field {name} for {cls.__name__}')
        for field in cls.fields:
            if field.name == name:
                _logger.debug(f'Found field {name} for {cls.__name__}')
                return field
        _logger.debug(f'Field {name} not found for {cls.__name__}')
        return None
