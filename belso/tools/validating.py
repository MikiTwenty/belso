# belso.tools.validating

from typing import Any, Dict, Type, Union

import json

from belso.utils import get_logger
from belso.core.schema import Schema

_logger = get_logger(__name__)

@staticmethod
def validate_schema(
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
        _logger.debug(f"Starting validation against schema '{schema_name}'...")

        # Convert string to dict if needed
        if isinstance(data, str):
            _logger.debug("Input data is a string, attempting to parse as JSON...")
            try:
                data = json.loads(data)
                _logger.debug("Successfully parsed JSON string.")
            except json.JSONDecodeError as e:
                _logger.error(f"Failed to parse JSON string: {e}")
                _logger.debug("JSON parsing error details", exc_info=True)
                raise ValueError("Invalid JSON string provided")

        # Get required fields
        required_fields = schema.get_required_fields()
        _logger.debug(f"Schema has {len(required_fields)} required fields: {', '.join(required_fields)}")

        # Check required fields
        _logger.debug("Checking for required fields...")
        for field_name in required_fields:
            if field_name not in data:
                _logger.error(f"Missing required field: '{field_name}'.")
                raise ValueError(f"Missing required field: {field_name}.")
        _logger.debug("All required fields are present.")

        # Validate field types
        _logger.debug("Validating field types...")
        for field in schema.fields:
            if field.name in data:
                value = data[field.name]
                field_type = field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_)

                # Skip None values for non-required fields
                if value is None and not field.required:
                    _logger.debug(f"Field '{field.name}' has None value, which is allowed for optional fields.")
                    continue

                # Log the field being validated
                _logger.debug(f"Validating field '{field.name}' with value '{value}' against type '{field_type}'...")

                # Handle array fields
                if hasattr(field, 'items_type') or (hasattr(field.type_, "__origin__") and field.type_.__origin__ is list):
                    if not isinstance(value, list):
                        value_type = type(value).__name__
                        _logger.error(f"Type mismatch for field '{field.name}': expected list, got '{value_type}'.")
                        raise TypeError(f"Field '{field.name}' expected type list, got {value_type}.")

                    # Check array length constraints if specified
                    if hasattr(field, 'items_range') and field.items_range:
                        min_items, max_items = field.items_range
                        if len(value) < min_items:
                            _logger.error(f"Array field '{field.name}' has too few items: {len(value)} < {min_items}")
                            raise ValueError(f"Array field '{field.name}' must have at least {min_items} items, got {len(value)}.")
                        if len(value) > max_items:
                            _logger.error(f"Array field '{field.name}' has too many items: {len(value)} > {max_items}")
                            raise ValueError(f"Array field '{field.name}' must have at most {max_items} items, got {len(value)}.")

                    # Get item type for validation
                    item_type = getattr(field, 'items_type', None)
                    if item_type is None and hasattr(field.type_, "__args__"):
                        item_type = field.type_.__args__[0]

                    # Validate each item in the array
                    if item_type:
                        for i, item in enumerate(value):
                            # For nested schemas, recursively validate
                            if isinstance(item_type, type) and issubclass(item_type, Schema):
                                try:
                                    # This is where the fix is needed - we need to ensure the validation
                                    # properly checks types and raises exceptions
                                    validate_schema(item, item_type)
                                except Exception as e:
                                    _logger.error(f"Validation failed for item {i} in array field '{field.name}': {e}")
                                    raise ValueError(f"Invalid item at index {i} in array field '{field.name}': {e}")
                            # For primitive types, check type
                            elif not isinstance(item, item_type):
                                item_value_type = type(item).__name__
                                item_type_name = item_type.__name__ if hasattr(item_type, "__name__") else str(item_type)
                                _logger.error(f"Type mismatch for item {i} in array field '{field.name}': expected '{item_type_name}', got '{item_value_type}'.")
                                raise TypeError(f"Item at index {i} in array field '{field.name}' expected type {item_type_name}, got {item_value_type}.")

                # Handle nested schema fields
                elif hasattr(field, 'schema') and isinstance(value, dict):
                    try:
                        validate_schema(value, field.schema)
                    except Exception as e:
                        _logger.error(f"Validation failed for nested field '{field.name}': {e}")
                        raise ValueError(f"Invalid data for nested field '{field.name}': {e}")

                # Type validation for primitive fields
                elif not isinstance(value, field.type_):
                    # Special case for int/float compatibility
                    if field.type_ == float and isinstance(value, int):
                        _logger.debug(f"Converting integer value {value} to float for field '{field.name}'...")
                        data[field.name] = float(value)
                    else:
                        value_type = type(value).__name__
                        _logger.error(f"Type mismatch for field '{field.name}': expected '{field_type}', got '{value_type}'.")
                        raise TypeError(f"Field '{field.name}' expected type {field_type}, got {value_type}.")
                else:
                    _logger.debug(f"Field '{field.name}' passed type validation.")

        _logger.debug("All fields passed validation.")
        return data

    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            # Only log unexpected errors, as ValueError and TypeError are already logged
            _logger.error(f"Unexpected error during validation: {e}")
            _logger.debug("Validation error details", exc_info=True)
