from typing import Any, List, Optional, Type, ClassVar, Tuple, Union
from belso.utils.logging import get_logger

logger = get_logger(__name__)

class BaseField:
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
            format_: Optional[str] = None,
            not_: Optional[dict] = None,
            any_of: Optional[List[dict]] = None,
            one_of: Optional[List[dict]] = None,
            all_of: Optional[List[dict]] = None
        ) -> None:
        """
        Initialize a new BaseField instance.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `type_` (`Type`): the expected Python type.
        - `description` (`str`): a user-facing description of the field.
        - `required` (`bool`): marks the field as required. Defaults to `True`.
        - `default` (`Optional[Any]`): the default value, if any.
        - `enum` (`Optional[List[Any]]`): enumeration of accepted values.
        - `range_` (`Optional[Tuple]`): min and max for numbers or comparable types (inclusive).
        - `exclusive_range` (`Optional[Tuple[bool, bool]]`): exclusivity of min and max bounds.
        - `length_range` (`Optional[Tuple[int, int]]`): valid length for strings/arrays.
        - `items_range` (`Optional[Tuple[int, int]]`): number of elements for arrays.
        - `properties_range` (`Optional[Tuple[int, int]]`): number of keys for objects.
        - `regex` (`Optional[str]`): regex the value must match.
        - `multiple_of` (`Optional[float]`): value must be a multiple of this number.
        - `format_` (`Optional[str]`): semantic hints (e.g., 'email', 'date-time').
        - `not_`, `any_of`, `one_of`, `all_of`: schema composition constructs (used mainly by OpenAI, partially by Mistral and LangChain).
        """
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
        self.not_ = not_
        self.any_of = any_of
        self.one_of = one_of
        self.all_of = all_of

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
        logger.debug(f'Getting required fields for {cls.__name__}')
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
        - `Optional[belso.schemas.BaseField]`: the field with the given name, or `None` if not found.
        """
        logger.debug(f'Getting field {name} for {cls.__name__}')
        for field in cls.fields:
            if field.name == name:
                logger.debug(f'Found field {name} for {cls.__name__}')
                return field
        logger.debug(f'Field {name} not found for {cls.__name__}')
        return None
