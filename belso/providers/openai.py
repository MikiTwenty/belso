# belso.providers.openai

from typing import Type, Optional, List
from pydantic import create_model, Field as PydanticField, BaseModel

from belso.utils import get_logger
from belso.core import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils.helpers import create_fallback_schema

logger = get_logger(__name__)

def to_openai(schema: Type[Schema]) -> Type[BaseModel]:
    """
    Convert a belso schema to OpenAI GPT format.\n
    ---
    ### Args
    - `schema` (`Type[belso.Schema]`): the belso schema to convert.\n
    ---
    ### Returns
    - `Type[belso.schemas.BaseModel]`: the converted Pydantic model.
    """
    try:
        schema_name = getattr(schema, "__name__", "GeneratedModel")
        logger.debug(f"Translating schema '{schema_name}' to OpenAI format...")

        def convert_field(field: BaseField) -> tuple:
            """
            Converts a single field into a (type, PydanticField) tuple.
            """
            field_type = field.type_
            metadata = {"description": field.description or ""}

            if field.enum:
                metadata["enum"] = field.enum
            if field.regex:
                metadata["pattern"] = field.regex
            if field.multiple_of:
                metadata["multipleOf"] = field.multiple_of
            if field.format_:
                metadata["format"] = field.format_

            if isinstance(field, NestedField):
                field_type = to_openai(field.schema)
            elif isinstance(field, ArrayField):
                if isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
                    item_model = to_openai(field.items_type)
                    field_type = List[item_model]
                else:
                    field_type = List[field.items_type]

            if not field.required and field.default is not None:
                return (Optional[field_type], PydanticField(default=field.default, **metadata))
            elif not field.required:
                return (Optional[field_type], PydanticField(default=None, **metadata))
            else:
                return (field_type, PydanticField(..., **metadata))

        field_definitions = {
            field.name: convert_field(field)
            for field in schema.fields
        }

        return create_model(schema_name, **field_definitions)

    except Exception as e:
        logger.error(f"Error in to_openai: {e}")
        logger.debug("Details:", exc_info=True)
        return create_model("FallbackModel", text=(str, ...))

def from_openai(schema: Type[BaseModel]) -> Type[Schema]:
    """
    Convert a Pydantic OpenAI schema to belso format.
    ---
    ### Args
    - `schema` (`Type[BaseModel]`): the Pydantic model to convert.
    ---
    ### Returns
    - `Type[Schema]`: the converted belso schema.
    """
    try:
        logger.debug("Starting conversion from Pydantic to belso schema...")

        class ConvertedSchema(Schema):
            fields = []

        model_fields = getattr(schema, "__fields__", {})  # Pydantic v1 & v2 compatibility

        for name, field_info in model_fields.items():
            field_type = field_info.outer_type_ if hasattr(field_info, "outer_type_") else field_info.annotation
            required = field_info.required if hasattr(field_info, "required") else True
            default = field_info.default if hasattr(field_info, "default") else None
            description = field_info.field_info.description if hasattr(field_info.field_info, "description") else ""

            # Nested model
            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                nested_schema = from_openai(field_type)
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

            # Array of nested or base
            if getattr(field_type, "__origin__", None) is list:
                item_type = field_type.__args__[0]
                if isinstance(item_type, type) and issubclass(item_type, BaseModel):
                    nested_item_schema = from_openai(item_type)
                    ConvertedSchema.fields.append(
                        ArrayField(
                            name=name,
                            items_type=dict,
                            description=description,
                            required=required,
                            default=default
                        )
                    )
                    continue
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

            # BaseField fallback
            ConvertedSchema.fields.append(
                BaseField(
                    name=name,
                    type_=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error in from_openai: {e}")
        logger.debug("Details:", exc_info=True)
        return create_fallback_schema()
