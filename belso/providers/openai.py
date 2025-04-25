# belso.providers.openai

from typing import List, Optional, Type, Tuple

import pydantic
import pydantic.fields
from belso.utils import get_logger
from belso.core import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from pydantic import create_model, Field as PydanticField, BaseModel
from belso.utils.helpers import map_json_to_python_type, create_fallback_schema

_logger = get_logger(__name__)

_OPENAI_FIELD_TO_METADATA_MAPPING = {
    "enum": ("enum", None),
    "regex": ("pattern", None),
    "multiple_of": ("multipleOf", None),
    "format_": ("format", None),
}

def _convert_field_to_pydantic(field: BaseField) -> tuple:
    """
    Converts a base field into a Pydantic field definition.\n
    ---
    ### Args
    - `field` (`belso.core.BaseField`): the field to convert.\n
    ---
    ### Returns
    - `Tuple[Type, pydantic.Field]`: for use with `create_model`.
    """
    _logger.debug(f"Converting field '{field.name}' to Pydantic field...")

    field_type = field.type_
    metadata = {"description": field.description or ""}

    for attr, (key, func) in _OPENAI_FIELD_TO_METADATA_MAPPING.items():
        value = getattr(field, attr, None)
        if value is not None:
            metadata[key] = func(value) if func else value

    if not field.required and field.default is not None:
        return Optional[field_type], PydanticField(default=field.default, **metadata)
    elif not field.required:
        return Optional[field_type], PydanticField(default=None, **metadata)
    else:
        return field_type, PydanticField(..., **metadata)

def _convert_nested_field(field: NestedField) -> tuple:
    """
    Convert a nested field into a Pydantic field.\n
    ---
    ### Args
    - `field` (`belso.core.NestedField`): the nested field.\n
    ---
    ### Returns
    - `Tuple[Type, pydantic.Field]`
    """
    _logger.debug(f"Converting nested field '{field.name}' to Pydantic model...")
    nested_model = to_openai(field.schema)
    return _convert_field_to_pydantic(
        BaseField(
            name=field.name,
            type_=nested_model,
            description=field.description,
            required=field.required,
            default=getattr(field, "default", None)
        )
    )

def _convert_array_field(field: ArrayField) -> Tuple[Type, pydantic.Field]:
    """
    Convert an array field into a Pydantic field.\n
    ---
    ### Args
    - `field` (`belso.core.ArrayField`): the array field.\n
    ---
    ### Returns
    - `Tuple[(type, PydanticField)]`
    """
    _logger.debug(f"Converting array field '{field.name}' to Pydantic list...")

    metadata = {"description": field.description or ""}
    if field.enum:
        metadata["enum"] = field.enum
    if field.items_range:
        metadata["minItems"] = field.items_range[0]
        metadata["maxItems"] = field.items_range[1]

    if isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
        items_model = to_openai(field.items_type)
        list_type = List[items_model]
    else:
        list_type = List[field.items_type]

    if not field.required and field.default is not None:
        return Optional[list_type], PydanticField(default=field.default, **metadata)
    elif not field.required:
        return Optional[list_type], PydanticField(default=None, **metadata)
    else:
        return list_type, PydanticField(..., **metadata)

def to_openai(schema: Type[Schema]) -> Type[BaseModel]:
    """
    Convert a belso schema to OpenAI-compatible Pydantic model.\n
    ---
    ### Args
    - `schema` (`Type[belso.Schema]`): the belso schema.\n
    ---
    ### Returns
    - `Type[pydantic.BaseModel]`: the Pydantic model.
    """
    try:
        schema_name = getattr(schema, "__name__", "GeneratedModel")
        _logger.debug(f"Translating schema '{schema_name}' to OpenAI Pydantic model...")

        field_definitions = {}

        for field in schema.fields:
            if isinstance(field, NestedField):
                field_definitions[field.name] = _convert_nested_field(field)
            elif isinstance(field, ArrayField):
                field_definitions[field.name] = _convert_array_field(field)
            else:
                field_definitions[field.name] = _convert_field_to_pydantic(field)

        model = create_model(schema_name, **field_definitions)
        _logger.debug(f"Pydantic model '{schema_name}' created successfully.")
        return model

    except Exception as e:
        _logger.error(f"Error converting to OpenAI model: {e}")
        _logger.debug("Exception details:", exc_info=True)
        return create_model("FallbackModel", text=(str, ...))

def from_openai(
        schema: Type[BaseModel],
        name_prefix: str = "Converted"
    ) -> Type[Schema]:
    """
    Convert a Pydantic model into a belso Schema.\n
    ---
    ### Args
    - `schema` (`Type[pydantic.BaseModel]`): the Pydantic model.
    - `name_prefix` (`str`, optional): the prefix to add to the schema name. Defaults to "Converted".\n
    ---
    ### Returns
    - `Type[belso.Schema]`: the belso schema.
    """
    try:
        _logger.debug("Starting conversion from Pydantic to belso schema...")

        schema_class_name = f"{name_prefix}Schema"
        ConvertedSchema = type(schema_class_name, (Schema,), {"fields": []})

        model_fields = getattr(schema, "__fields__", {})

        for name, field_info in model_fields.items():
            field_type = field_info.outer_type_ if hasattr(field_info, "outer_type_") else field_info.annotation
            required = getattr(field_info, "required", True)
            default = None
            if hasattr(field_info, "default") and field_info.default is not pydantic.fields._Unset:
                default = field_info.default
            description = getattr(field_info, "description", "")

            # Handle nested models
            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                nested_schema = from_openai(field_type, name_prefix=f"{name_prefix}_{name}")
                ConvertedSchema.fields.append(
                    NestedField(
                        name=name,
                        schema=nested_schema,
                        description=description,
                        required=required,
                        default=default
                    )
                )
                continue

            # Handle list of items
            if getattr(field_type, "__origin__", None) is list:
                item_type = field_type.__args__[0]

                # List di modelli (nested)
                if isinstance(item_type, type) and issubclass(item_type, BaseModel):
                    nested_schema = from_openai(item_type, name_prefix=f"{name_prefix}_{name}")
                    ConvertedSchema.fields.append(
                        ArrayField(
                            name=name,
                            items_type=dict,
                            description=description,
                            required=required,
                            default=default
                        )
                    )
                # List di tipi primitivi (aggiungi questo blocco!)
                else:
                    ConvertedSchema.fields.append(
                        ArrayField(
                            name=name,
                            items_type=item_type,
                            description=description,
                            required=required,
                            default=default
                        )
                    )
                continue

            ConvertedSchema.fields.append(
                BaseField(
                    name=name,
                    type_=map_json_to_python_type(str(field_type)),
                    description=description,
                    required=required,
                    default=default
                )
            )

        _logger.debug("Successfully converted Pydantic model to belso schema.")
        return ConvertedSchema

    except Exception as e:
        _logger.error(f"Error converting from Pydantic model: {e}")
        _logger.debug("Exception details:", exc_info=True)
        return create_fallback_schema()
