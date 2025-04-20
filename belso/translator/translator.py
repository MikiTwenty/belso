import logging
from typing import Any, Dict, Type

from pydantic import create_model, Field as PydanticField
from google.ai.generativelanguage_v1beta.types import content

from belso.translator.schemas import Schema

logger = logging.getLogger(__name__)

class SchemaTranslator:
    @staticmethod
    def to_gemini(schema: Type[Schema]) -> content.Schema:
        """
        Translate a standard schema to Google Gemini format.
        """
        try:
            # Type mapping for Gemini
            type_mapping = {
                list: content.Type.ARRAY,
                bool: content.Type.BOOLEAN,
                str: content.Type.STRING,
                float: content.Type.NUMBER,
                int: content.Type.INTEGER,
                dict: content.Type.OBJECT,
                Any: content.Type.TYPE_UNSPECIFIED,
            }

            properties = {}
            required_fields = schema.get_required_fields()

            # Build properties for each field
            for field in schema.fields:
                field_type = type_mapping.get(field.type, content.Type.TYPE_UNSPECIFIED)
                properties[field.name] = content.Schema(
                    type=field_type,
                    description=field.description
                )

            # Create the schema
            gemini_schema = content.Schema(
                type=content.Type.OBJECT,
                properties=properties,
                required=required_fields
            )

            return gemini_schema

        except Exception as e:
            logger.error(f"Error translating schema to Gemini format: {e}")
            return {}

    @staticmethod
    def to_ollama(schema: Type[Schema]) -> Dict[str, Any]:
        """
        Translate a standard schema to Ollama format.
        """
        try:
            properties = {}
            required_fields = schema.get_required_fields()

            # Build properties for each field
            for field in schema.fields:
                properties[field.name] = {
                    "type": "string" if field.type == str else "number" if field.type in [int, float] else "boolean" if field.type == bool else "array" if field.type == list else "object",
                    "description": field.description
                }

            # Create the schema
            ollama_schema = {
                "type": "object",
                "properties": properties,
                "required": required_fields
            }

            return ollama_schema

        except Exception as e:
            logger.error(f"Error translating schema to Ollama format: {e}")
            return {}

    @staticmethod
    def to_gpt(schema: Type[Schema]) -> Type:
        """
        Translate a standard schema to OpenAI GPT format (Pydantic model).
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
