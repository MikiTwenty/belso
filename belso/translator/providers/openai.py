import logging
from typing import Type

from pydantic import create_model, Field as PydanticField, BaseModel

from belso.translator.schemas import Schema, Field

logger = logging.getLogger(__name__)

def to_openai(schema: Type[Schema]) -> Type:
    """
    Translate a standard schema to OpenAI GPT format (Pydantic model).\n
    ---
    ### Args
    - `schema`: the schema to translate.\n
    ---
    ### Returns
    - `Type`: the translated schema as a Pydantic model.
    """
    try:
        field_definitions = {}

        # Build field definitions for Pydantic model
        for field in schema.fields:
            field_type = field.type
            if not field.required and field.default is not None:
                field_definitions[field.name] = (field_type, PydanticField(default=field.default, description=field.description))
            else:
                field_definitions[field.name] = (field_type, PydanticField(description=field.description))

        # Create a Pydantic model dynamically
        model_name = schema.__name__ if hasattr(schema, "__name__") else "DynamicModel"
        pydantic_model = create_model(model_name, **field_definitions)

        return pydantic_model

    except Exception as e:
        logger.error(f"Error translating schema to GPT format: {e}")
        # Return a simple fallback model if translation fails
        return create_model("FallbackModel", text=(str, ...))

def from_openai(schema: Type[BaseModel]) -> Type[Schema]:
    """
    Convert an OpenAI schema (Pydantic model) to Belso Schema format.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    ---
    ### Returns
    - `Type`: the converted schema as a standard Schema subclass.
    """
    try:
        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = schema.__name__ if hasattr(schema, "__name__") else "ConvertedFromOpenAI"
            fields = []

        # Get model fields from Pydantic model
        model_fields = schema.model_fields if hasattr(schema, "model_fields") else {}

        # For older Pydantic versions
        if not model_fields and hasattr(schema, "__fields__"):
            model_fields = schema.__fields__

        # Process each field
        for name, field_info in model_fields.items():
            # Extract field type
            if hasattr(field_info, "annotation"):
                field_type = field_info.annotation
            elif hasattr(field_info, "type_"):
                field_type = field_info.type_
            else:
                field_type = str  # Default to string

            # Extract description
            description = ""
            if hasattr(field_info, "description"):
                description = field_info.description

            # Extract required status
            required = True
            if hasattr(field_info, "default") and field_info.default is not None:
                required = False

            # Extract default value
            default = None
            if hasattr(field_info, "default") and field_info.default is not None:
                default = field_info.default

            ConvertedSchema.fields.append(
                Field(
                    name=name,
                    type=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting OpenAI schema to Belso format: {e}")
        # Return a minimal schema if conversion fails
        class FallbackSchema(Schema):
            name = "FallbackSchema"
            fields = [Field(name="text", type=str, description="Fallback field", required=True)]
        return FallbackSchema
