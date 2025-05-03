# belso.core.field

from __future__ import annotations   # keeps forward annotations as strings

import builtins
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
    Factory class that returns the correct `BaseField` subtype
    (`BaseField`, `NestedField`, or `ArrayField`).
    """
    def __new__(
            cls,
            name: str,
            type: Any,
            description: str = "",
            required: bool = True,
            default: Optional[Any] = None,
            enum: Optional[List[Any]] = None,
            range: Optional[tuple] = None,
            exclusive_range: Optional[tuple] = None,
            length_range: Optional[tuple] = None,
            items_range: Optional[tuple] = None,
            properties_range: Optional[tuple] = None,
            regex: Optional[str] = None,
            multiple_of: Optional[float] = None,
            format: Optional[str] = None,
        ) -> Union[
            "belso.core.BaseField",
            "belso.core.NestedField",
            "belso.core.ArrayField",
        ]:
        """
        Decide which concrete *Field* class to instantiate.\n
        ---
        ### Args
        - `name` (`str`): field name shown to the user.
        - `type` (`Type`): annotation or runtime type hint.
        - `description` (`str`, optional): description of the field.
        - `required` (`bool`, optional): whether the field is required.
        - `default` (`Any`, optional): default value for the field.
        - `enum` (`List[Any]`, optional): list of valid values for the field.
        - `range` (`tuple`, optional): range of valid values for the field.
        - `exclusive_range` (`tuple`, optional): range of valid values for the field.
        - `length_range` (`tuple`, optional): range of valid values for the field.
        - `items_range` (`tuple`, optional): range of valid values for the field.
        - `properties_range` (`tuple`, optional): range of valid values for the field.
        - `regex` (`str`, optional): regular expression for validating the field.
        - `multiple_of` (`float`, optional): multiple of valid values for the field.
        - `format` (`str`, optional): format of valid values for the field.\n
        ---
        ### Returns
        - `Union[BaseField, NestedField, ArrayField]`: the new field.
        """
        origin = get_origin(type)
        args = get_args(type)

        kwargs = dict(
            name=name,
            description=description,
            required=required,
            default=default,
            enum=enum,
            range_=range,
            exclusive_range=exclusive_range,
            length_range=length_range,
            items_range=items_range,
            properties_range=properties_range,
            regex=regex,
            multiple_of=multiple_of,
            format_=format,
        )

        # Lists
        if origin in (list, List):
            item_type = args[0] if args else str
            is_schema = (
                isinstance(item_type, builtins.type)
                and issubclass(item_type, Schema)
            )
            kwargs["items_type"] = dict if is_schema else item_type
            _logger.debug(f"[Field] -> ArrayField<{item_type}>")
            return ArrayField(**kwargs)

        # Schemas
        if (
            isinstance(type, builtins.type)
            and issubclass(type, Schema)
        ):
            _logger.debug(f"[Field] -> NestedField<{type.__name__}>")
            return NestedField(schema=type, **kwargs)

        # Primitives or custom types
        _logger.debug(f"[Field] -> BaseField<{type}>")
        return BaseField(type_=type, **kwargs)
