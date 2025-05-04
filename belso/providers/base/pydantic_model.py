# belso.providers.base.pydantic_model

from __future__ import annotations

from typing import Dict, Any, Callable, List, Optional, Tuple, Type, get_origin

from pydantic import BaseModel, Field as PydanticField, create_model

from belso.utils.logging import get_logger
from belso.core.schema import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils.mappings.field_mappings import _PYDANTIC_FIELD_MAP

import pydantic.fields

_logger = get_logger(__name__)

def _convert_field_to_pydantic(field: BaseField) -> Tuple[Type, PydanticField]:
    """
    Converts a base field into a Pydantic field definition.\n
    ---
    ### Args
    - `field` (`BaseField`): the field to convert.\n
    ---
    ### Returns
    - `Tuple[Type, PydanticField]`: the field type and PydanticField instance.
    """
    _logger.debug(f"Converting field '{field.name}' to Pydantic field...")
    field_type = field.type_
    metadata = {"description": field.description or ""}

    for attr, (key, func) in _PYDANTIC_FIELD_MAP.items():
        value = getattr(field, attr, None)
        if value is not None:
            metadata[key] = func(value) if func else value

    if not field.required and field.default is not None:
        return Optional[field_type], PydanticField(default=field.default, **metadata)
    elif not field.required:
        return Optional[field_type], PydanticField(default=None, **metadata)
    else:
        return field_type, PydanticField(..., **metadata)

def _convert_nested_field(
        field: NestedField,
        to_func: Callable[[Type[Schema]], Dict[str, Any]]
    ) -> Tuple[Type, PydanticField]:
    """
    Converts a NestedField to a Pydantic field definition.\n
    ---
    ### Args
    - `field` (`NestedField`): the nested field to convert.
    - `to_func` (`Callable[[Type[Schema]], Dict[str, Any]]`): the function to convert nested schemas.\n
    ---
    ### Returns
    - `Tuple[Type, PydanticField]`: the nested field type and PydanticField instance.
    """
    model = to_func(field.schema)
    return _convert_field_to_pydantic(
        BaseField(
            name=field.name,
            type_=model,
            description=field.description,
            required=field.required,
            default=field.default
        )
    )

def _convert_array_field(
        field: ArrayField,
        to_func: Callable[[Type[Schema]], Dict[str, Any]]
    ) -> Tuple[Type, PydanticField]:
    """
    Converts an ArrayField to a Pydantic field definition.\n
    ---
    ### Args
    - `field` (`ArrayField`): the array field to convert.
    - `to_func` (`Callable[[Type[Schema]], Dict[str, Any]]`): the function to convert nested schemas.
    ---
    ### Returns
    - `Tuple[Type, PydanticField]`: the array field type and PydanticField instance.
    """
    metadata = {"description": field.description or ""}
    if field.enum:
        metadata["enum"] = field.enum
    if field.items_range:
        metadata["minItems"] = field.items_range[0]
        metadata["maxItems"] = field.items_range[1]

    if isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
        items_model = to_func(field.items_type)
        list_type = List[items_model]
    else:
        list_type = List[field.items_type]

    if not field.required and field.default is not None:
        return Optional[list_type], PydanticField(default=field.default, **metadata)
    elif not field.required:
        return Optional[list_type], PydanticField(default=None, **metadata)
    else:
        return list_type, PydanticField(..., **metadata)

def to_pydantic_model(schema: Type[Schema]) -> Type[BaseModel]:
    """
    Converts a belso Schema to a Pydantic model.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the belso schema.\n
    ---
    ### Returns
    - `Type[BaseModel]`: the Pydantic model.
    """
    schema_name = getattr(schema, "__name__", "GeneratedModel")
    _logger.debug(f"Creating Pydantic model '{schema_name}'...")
    fields = {}
    for f in schema.fields:
        if isinstance(f, NestedField):
            fields[f.name] = _convert_nested_field(f, to_pydantic_model)
        elif isinstance(f, ArrayField):
            fields[f.name] = _convert_array_field(f, to_pydantic_model)
        else:
            fields[f.name] = _convert_field_to_pydantic(f)

    return create_model(schema_name, **fields)

def from_pydantic_model(
        schema: Type[BaseModel],
        schema_name: str = "Schema"
    ) -> Type[Schema]:
    """
    Converts a Pydantic model back to a belso Schema.\n
    ---
    ### Args
    - `schema` (`Type[BaseModel]`): the Pydantic model.
    - `schema_name` (`str`): base name of the resulting belso schema.\n
    ---
    ### Returns
    - `Type[Schema]`: the belso schema.
    """
    ConvertedSchema = type(f"{schema_name}Schema", (Schema,), {"fields": []})
    for name, field_info in schema.__fields__.items():
        field_type = field_info.outer_type_ if hasattr(field_info, "outer_type_") else field_info.annotation
        required = getattr(field_info, "required", True)
        default = None if field_info.default is pydantic.fields._Unset else field_info.default
        description = getattr(field_info, "description", "")

        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            nested = from_pydantic_model(field_type, schema_name=name)
            ConvertedSchema.fields.append(NestedField(name, nested, description, required, default))
        elif get_origin(field_type) in (list, List):
            item_type = field_type.__args__[0]
            if isinstance(item_type, type) and issubclass(item_type, BaseModel):
                ConvertedSchema.fields.append(ArrayField(name, dict, description, required, default))
            else:
                ConvertedSchema.fields.append(ArrayField(name, item_type, description, required, default))
        else:
            ConvertedSchema.fields.append(BaseField(name, field_type, description, required, default))

    return ConvertedSchema

def pydantic_provider():
    """
    Factory wrapper for OpenAI/LangChain style Pydantic models.\n
    ---
    ### Returns
    - `tuple`: (`to_func`, `from_func`) for schema conversion.
    """
    return lambda _: (to_pydantic_model, from_pydantic_model)
