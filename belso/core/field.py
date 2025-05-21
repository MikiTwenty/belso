# belso.core.field

from __future__ import annotations

import builtins
from typing import Type, Optional, Any, List, Dict, Union, get_origin, get_args

from beartype import beartype

from belso.utils import get_logger
from belso.core.schema import Schema, BaseField

_logger = get_logger(__name__)

# Common parameters for all fields
_COMMON_PARAMS = {"name", "description", "required", "default"}

# Validation parameters for each type
_VALIDATION_PARAMS: Dict[Type, set] = {
    str: {"enum", "length_range", "regex", "format_"},
    int: {"enum", "range_", "exclusive_range", "multiple_of"},
    float: {"enum", "range_", "exclusive_range", "multiple_of"},
    bool: {"enum"},
    list: {"enum", "items_range"},
    dict: {"enum", "properties_range"},
    Any: {"enum"}
}

def _validate_field_params(
        type_: Type,
        **kwargs
    ) -> Dict[str, Any]:
    """
    Validate field parameters based on the given type.\n
    ---
    ### Args
    - `type_` (`Type`): type of the field.
    - `**kwargs`: keyword arguments containing field parameters.\n
    ---
    ### Returns
    - `Dict[str, Any]`: validated field parameters.
    """
    base_type = get_origin(type_) or type_

    if isinstance(type_, type) and issubclass(type_, Schema):
        base_type = dict

    allowed_keys = _VALIDATION_PARAMS.get(base_type, _VALIDATION_PARAMS[Any])
    all_valid_keys = allowed_keys | _COMMON_PARAMS

    valid_params = {}
    for param, value in kwargs.items():
        if value is not None and param in all_valid_keys:
            valid_params[param] = value
        elif value is not None:
            _logger.warning(
                f"Parametro '{param}' ignorato per il tipo {base_type.__name__}. "
                f"Parametri validi: {sorted(all_valid_keys)}"
            )

    return valid_params

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
    __slots__ = BaseField.__slots__ + ("schema",)

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
        # Valida i parametri per il tipo dict
        valid_params = _validate_field_params(
            dict,
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

        super().__init__(
            name=name,
            type_=dict,
            description=description,
            required=required,
            default=default,
            **{k: v for k, v in valid_params.items() if k not in ['name', 'description', 'required', 'default']}
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
    __slots__ = BaseField.__slots__ + ("items_type",)

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
            format_: Optional[str] = None
        ) -> None:
        # Valida i parametri per il tipo list
        valid_params = _validate_field_params(
            list,
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

        super().__init__(
            name=name,
            type_=list,
            description=description,
            required=required,
            default=default,
            **{k: v for k, v in valid_params.items() if k not in ['name', 'description', 'required', 'default']}
        )
        self.items_type = items_type

class Field:
    """
    Factory class that returns the correct `BaseField` subtype
    (`BaseField`, `NestedField`, or `ArrayField`).
    """
    @beartype
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
            BaseField,
            NestedField,
            ArrayField,
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

        # Valida i parametri per il tipo specifico
        valid_params = _validate_field_params(
            type,
            **kwargs
        )

        # Aggiungi i parametri base
        valid_params.update({
            'name': name,
            'type_': type,
            'description': description,
            'required': required,
            'default': default,
        })

        return BaseField(**valid_params)
