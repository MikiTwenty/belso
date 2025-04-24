# belso.translator.providers.openai

from typing import Type

from pydantic import create_model, Field as PydanticField, BaseModel


from belso.utils.logging import get_logger
from belso.schemas import Schema, BaseField
from belso.utils.schema_helpers import create_fallback_schema

# Replace standard logger with our custom logger
logger = get_logger(__name__)

def to_openai(schema: Type[Schema]) -> Type[BaseModel]:
    """
    Convert a belso schema to OpenAI GPT format.\n
    ---
    ### Args
    - `schema` (`Type[belso.Schema]`): the belso schema to convert.\n
    ---
    ### Returns
    - `Type[pydantic.BaseModel]`: the converted schema.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting translation of schema '{schema_name}' to OpenAI format...")

        field_definitions = {}

        # Build field definitions for Pydantic model
        for field in schema.fields:
            field_type = field.type_
            logger.debug(f"Processing field '{field.name}' of type '{field_type.__name__}'...")

            if not field.required and field.default is not None:
                logger.debug(f"BaseField '{field.name}' is optional with default value: {field.default}.")
                field_definitions[field.name] = (field_type, PydanticField(default=field.default, description=field.description))
            else:
                required_status = "required" if field.required else "optional without default"
                logger.debug(f"BaseField '{field.name}' is {required_status}.")
                field_definitions[field.name] = (field_type, PydanticField(description=field.description))

        # Create a Pydantic model dynamically
        model_name = schema.__name__ if hasattr(schema, "__name__") else "DynamicModel"
        logger.debug(f"Creating Pydantic model '{model_name}' with {len(field_definitions)} fields...")
        pydantic_model = create_model(model_name, **field_definitions)

        logger.debug(f"Successfully created OpenAI schema as Pydantic model '{pydantic_model.__name__}'.")
        return pydantic_model

    except Exception as e:
        logger.error(f"Error translating schema to OpenAI format: {e}")
        logger.debug("Translation error details", exc_info=True)
        # Return a simple fallback model if translation fails
        logger.warning("Returning fallback model due to translation error.")
        return create_model("FallbackModel", text=(str, ...))

def from_openai(schema: Type[BaseModel]) -> Type[Schema]:
    """
    Convert an OpenAI schema to belso format.\n
    ---
    ### Args
    - `schema` (`Type[pydantic.BaseModel]`): the schema to convert.\n
    ---
    ### Returns
    - `Type[belso.Schema]`: the converted belso schema.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting conversion from OpenAI schema '{schema_name}' to belso format...")

        # Create a new Schema class
        class ConvertedSchema(Schema):
            fields = []

        # Get model fields from Pydantic model
        model_fields = schema.model_fields if hasattr(schema, "model_fields") else {}

        # For older Pydantic versions
        if not model_fields and hasattr(schema, "__fields__"):
            logger.debug("Using legacy Pydantic v1 field access.")
            model_fields = schema.__fields__

        logger.debug(f"Found {len(model_fields)} fields in Pydantic model.")

        # Process each field
        for name, field_info in model_fields.items():
            logger.debug(f"Processing field '{name}'.")

            # Extract field type
            if hasattr(field_info, "annotation"):
                field_type = field_info.annotation
                logger.debug(f"BaseField '{name}' has type annotation: {field_type}")
            elif hasattr(field_info, "type_"):
                field_type = field_info.type_
                logger.debug(f"BaseField '{name}' has type_: {field_type}")
            else:
                field_type = str  # Default to string
                logger.debug(f"BaseField '{name}' has no type information, defaulting to str.")

            # Extract description
            description = ""
            if hasattr(field_info, "description"):
                description = field_info.description
                logger.debug(f"BaseField '{name}' has description: '{description}'.")

            # Extract required status
            required = True
            if hasattr(field_info, "default") and field_info.default is not None:
                required = False
                logger.debug(f"BaseField '{name}' is optional with default value.")

            # Extract default value
            default = None
            if hasattr(field_info, "default") and field_info.default is not None:
                default = field_info.default
                logger.debug(f"BaseField '{name}' has default value: {default}.")

            ConvertedSchema.fields.append(
                BaseField(
                    name=name,
                    type_=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        logger.debug(f"Successfully converted OpenAI schema to belso schema with {len(ConvertedSchema.fields)} fields.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting OpenAI schema to belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        return create_fallback_schema()
