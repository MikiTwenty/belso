# belso.validator.validator

import json
from typing import Any, Dict, Type, Union

from belso.schemas import Schema
from belso.utils.logging import get_logger

# Get a module-specific logger
logger = get_logger(__name__)

class Validator:
    @staticmethod
    def validate(
            data: Union[Dict[str, Any], str],
            schema: Type[Schema]
        ) -> Dict[str, Any]:
        """
        Validate that the provided data conforms to the given schema.\n
        ---
        ### Args
        - `data` (`Union[Dict[str, Any], str]`): the data to validate (either a dict or JSON string).
        - `schema` (`Type[belso.Schema]`): the schema to validate against.\n
        ---
        ### Returns:
        - `Dict[str, Any]`: the validated data.
        """
        try:
            schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
            logger.debug(f"Starting validation against schema '{schema_name}'...")

            # Convert string to dict if needed
            if isinstance(data, str):
                logger.debug("Input data is a string, attempting to parse as JSON...")
                try:
                    data = json.loads(data)
                    logger.debug("Successfully parsed JSON string.")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON string: {e}")
                    logger.debug("JSON parsing error details", exc_info=True)
                    raise ValueError("Invalid JSON string provided")

            # Get required fields
            required_fields = schema.get_required_fields()
            logger.debug(f"Schema has {len(required_fields)} required fields: {', '.join(required_fields)}")

            # Check required fields
            logger.debug("Checking for required fields...")
            for field_name in required_fields:
                if field_name not in data:
                    logger.error(f"Missing required field: '{field_name}'.")
                    raise ValueError(f"Missing required field: {field_name}.")
            logger.debug("All required fields are present.")

            # Validate field types
            logger.debug("Validating field types...")
            for field in schema.fields:
                if field.name in data:
                    value = data[field.name]
                    field_type = field.type_hint.__name__ if hasattr(field.type_hint, "__name__") else str(field.type_hint)

                    # Skip None values for non-required fields
                    if value is None and not field.required:
                        logger.debug(f"BaseField '{field.name}' has None value, which is allowed for optional fields.")
                        continue

                    # Log the field being validated
                    logger.debug(f"Validating field '{field.name}' with value '{value}' against type '{field_type}'...")

                    # Type validation
                    if not isinstance(value, field.type_hint):
                        # Special case for int/float compatibility
                        if field.type_hint == float and isinstance(value, int):
                            logger.debug(f"Converting integer value {value} to float for field '{field.name}'...")
                            data[field.name] = float(value)
                        else:
                            value_type = type(value).__name__
                            logger.error(f"Type mismatch for field '{field.name}': expected '{field_type}', got '{value_type}'.")
                            raise TypeError(f"BaseField '{field.name}' expected type {field_type}, got {value_type}.")
                    else:
                        logger.debug(f"BaseField '{field.name}' passed type validation.")

            logger.debug("All fields passed validation.")
            return data

        except Exception as e:
            if not isinstance(e, (ValueError, TypeError)):
                # Only log unexpected errors, as ValueError and TypeError are already logged
                logger.error(f"Unexpected error during validation: {e}")
                logger.debug("Validation error details", exc_info=True)
            raise
