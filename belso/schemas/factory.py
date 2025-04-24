# belso.schemas.factory

from typing import Any, Optional, Union, List, get_origin, get_args
from belso.utils.logging import get_logger

logger = get_logger(__name__)

class Field:
    """
    Factory class that returns BaseField, NestedField, or ArrayField instances,
    depending on the type provided by the user.
    """
    def __new__(
            cls,
            name: str,
            type_hint: Any,
            description: str = "",
            required: bool = True,
            default: Optional[Any] = None
        ) -> Union['belso.schemas.BaseField', 'belso.schemas.NestedField', 'belso.schemas.ArrayField']:
        """
        Create a new Field instance based on the provided type hint.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `type_hint` (`Any`): the type hint for the field.
        - `description` (`str`): the description of the field. Defaults to an empty string.
        - `required` (`bool`): whether the field is required. Defaults to `True`.
        - `default` (`Optional[Any]`): the default value of the field. Defaults to `None`.
        ---
        ### Returns
        - `belso.schemas.BaseField` | `belso.schemas.NestedField` | `belso.schemas.ArrayField`: the created field instance.
        """
        from belso.schemas.base import BaseField, Schema
        from belso.schemas.nested import NestedField, ArrayField

        origin = get_origin(type_hint)
        args = get_args(type_hint)

        # Handle list types (e.g., List[str], List[MySchema])
        if origin is list or origin is List:
            item_type = args[0] if args else str
            if isinstance(item_type, type) and issubclass(item_type, Schema):
                logger.debug(f"[Field] -> ArrayField<{item_type.__name__}> (schema)")
                return ArrayField(
                    name=name,
                    items_type=dict,
                    items_schema=item_type,
                    description=description,
                    required=required
                )
            else:
                logger.debug(f"[Field] -> ArrayField<{item_type}>")
                return ArrayField(
                    name=name,
                    items_type=item_type,
                    description=description,
                    required=required
                )

        # Handle nested schemas
        if isinstance(type_hint, type) and issubclass(type_hint, Schema):
            logger.debug(f"[Field] -> NestedField<{type_hint.__name__}>")
            return NestedField(
                name=name,
                schema=type_hint,
                description=description,
                required=required
            )

        # Default: primitive type field
        logger.debug(f"[Field] -> BaseField<{type_hint}>")
        return BaseField(
            name=name,
            type=type_hint,
            description=description,
            required=required,
            default=default
        )
