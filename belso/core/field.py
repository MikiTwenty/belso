# belso.core.field

from typing import Type, Optional, Any, List, Dict, Union, get_origin, get_args

from belso.utils import get_logger
from belso.core.schema import Schema, BaseField

_logger = get_logger(__name__)

class NestedField(BaseField):
    """
    BaseField class for nested schemas.
    Supports all advanced validation parameters passed via BaseField.\n
    Used by:
    - OpenAI
    - Google
    - Ollama
    - Anthropic
    - Mistral
    - LangChain
    - HuggingFace
    """
    def __init__(
            self,
            name: str,
            schema: Type[Schema],
            description: str = "",
            required: bool = True,
            default: Optional[Any] = None,
            enum: Optional[List[Any]] = None,
            range_: Optional[tuple] = None,
            exclusive_range: Optional[tuple] = None,
            length_range: Optional[tuple] = None,
            items_range: Optional[tuple] = None,
            properties_range: Optional[tuple] = None,
            regex: Optional[str] = None,
            multiple_of: Optional[float] = None,
            format_: Optional[str] = None
        ) -> None:
        super().__init__(
            name=name,
            type_=dict,
            description=description,
            required=required,
            default=default,
            enum=enum,
            range_=range_,
            exclusive_range=exclusive_range,
            length_range=length_range,
            items_range=items_range,
            properties_range=properties_range,
            regex=regex,
            multiple_of=multiple_of,
            format_=format_
        )
        self.schema = schema

class ArrayField(BaseField):
    """
    BaseField class for arrays of items.
    Supports all advanced validation parameters passed via BaseField.\n
    Used by:
    - OpenAI
    - Google
    - Ollama
    - Anthropic
    - Mistral
    - LangChain
    - HuggingFace
    """
    def __init__(
            self,
            name: str,
            items_type: Type = str,
            description: str = "",
            required: bool = True,
            default: Optional[Any] = None,
            enum: Optional[List[Any]] = None,
            range_: Optional[tuple] = None,
            exclusive_range: Optional[tuple] = None,
            length_range: Optional[tuple] = None,
            items_range: Optional[tuple] = None,
            properties_range: Optional[tuple] = None,
            regex: Optional[str] = None,
            multiple_of: Optional[float] = None,
            format_: Optional[str] = None,
            not_: Optional[Dict] = None
        ) -> None:
        super().__init__(
            name=name,
            type_=list,
            description=description,
            required=required,
            default=default,
            enum=enum,
            range_=range_,
            exclusive_range=exclusive_range,
            length_range=length_range,
            items_range=items_range,
            properties_range=properties_range,
            regex=regex,
            multiple_of=multiple_of,
            format_=format_
        )
        self.items_type = items_type

class Field:
    """
    Factory class that returns BaseField, NestedField, or ArrayField instances,
    depending on the type provided by the user.
    """
    def __new__(
            cls,
            name: str,
            type_: Any,
            description: str = "",
            required: bool = True,
            default: Optional[Any] = None,
            enum: Optional[List[Any]] = None,
            range_: Optional[tuple] = None,
            exclusive_range: Optional[tuple] = None,
            length_range: Optional[tuple] = None,
            items_range: Optional[tuple] = None,
            properties_range: Optional[tuple] = None,
            regex: Optional[str] = None,
            multiple_of: Optional[float] = None,
            format_: Optional[str] = None
        ) -> Union['belso.core.BaseField', 'belso.core.NestedField', 'belso.core.ArrayField']:
        """
        Create a new Field instance based on the provided type hint.\n
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
        - `format_` (`Optional[str]`): semantic hints (e.g., 'email', 'date-time').\n
        ---
        ### Returns
        - `Union[belso.core.BaseField, belso.core.NestedField, belso.core.ArrayField]`: the created field instance.
        """
        origin = get_origin(type_)
        args = get_args(type_)

        kwargs = dict(
            name=name,
            description=description,
            required=required,
            default=default,
            enum=enum,
            range_=range_,
            exclusive_range=exclusive_range,
            length_range=length_range,
            items_range=items_range,
            properties_range=properties_range,
            regex=regex,
            multiple_of=multiple_of,
            format_=format_
        )

        # Handle list types (e.g., List[str], List[MySchema])
        if origin is list or origin is List:
            item_type = args[0] if args else str
            kwargs['items_type'] = dict if isinstance(item_type, type) and issubclass(item_type, Schema) else item_type
            _logger.debug(f"[Field] -> ArrayField<{item_type}>")
            return ArrayField(**kwargs)

        # Handle nested schemas
        if isinstance(type_, type) and issubclass(type_, Schema):
            _logger.debug(f"[Field] -> NestedField<{type_.__name__}>")
            return NestedField(schema=type_, **kwargs)

        # Default: primitive type field
        _logger.debug(f"[Field] -> BaseField<{type_}>")
        return BaseField(type_=type_, **kwargs)
