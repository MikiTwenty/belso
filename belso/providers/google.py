# belso.providers.google

from typing import Type

from google.ai.generativelanguage_v1beta.types import content

from belso.utils.logging import get_logger
from belso.core.schema import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils.helpers import create_fallback_schema
from belso.utils.mappings.type_mappings import _GOOGLE_TYPE_MAP, _REVERSE_GOOGLE_TYPE_MAP

_logger = get_logger(__name__)

def _convert_field_to_schema(field: BaseField) -> content.Schema:
    """
    Converts a base field into a Google content.Schema object.\n
    ---
    ### Args
    - `field` (`BaseField`): the field to convert.\n
    ---
    ### Returns
    - `content.Schema`: the corresponding Google schema.
    """
    _logger.debug(f"Converting base field '{field.name}' to Google Schema...")

    schema = content.Schema(
        type=_GOOGLE_TYPE_MAP.get(field.type_, content.Type.TYPE_UNSPECIFIED),
        description=field.description or "",
        nullable=not field.required
    )

    if field.enum:
        schema.enum.extend([str(e) for e in field.enum])
    if field.format_:
        schema.format = field.format_

    return schema


def _convert_nested_field(field: NestedField) -> content.Schema:
    """
    Converts a NestedField to a Google content.Schema object.\n
    ---
    ### Args
    - `field` (`NestedField`): the nested field.\n
    ---
    ### Returns
    - `content.Schema`: the nested schema.
    """
    _logger.debug(f"Converting nested field '{field.name}' to Google Schema...")

    nested_schema = to_google(field.schema)

    return content.Schema(
        type=content.Type.OBJECT,
        description=field.description or "",
        nullable=not field.required,
        properties=nested_schema.properties,
        required=nested_schema.required
    )

def _convert_array_field(field: ArrayField) -> content.Schema:
    """
    Converts an ArrayField to a Google content.Schema object.\n
    ---
    ### Args
    - `field` (`ArrayField`): the array field.\n
    ---
    ### Returns
    - `content.Schema`: the array schema.
    """
    _logger.debug(f"Converting array field '{field.name}' to Google Schema...")

    if isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
        items_schema = to_google(field.items_type)
    else:
        items_schema = content.Schema(
            type=_GOOGLE_TYPE_MAP.get(field.items_type, content.Type.TYPE_UNSPECIFIED)
        )

    schema = content.Schema(
        type=content.Type.ARRAY,
        description=field.description or "",
        nullable=not field.required,
        items=items_schema
    )

    if field.items_range:
        schema.min_items = field.items_range[0]
        schema.max_items = field.items_range[1]

    return schema


def to_google(schema: Type[Schema]) -> content.Schema:
    """
    Convert a belso schema to Google Gemini format.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`) : the belso schema to convert.\n
    ---
    ### Returns
    - `content.Schema`: the converted schema.
    """
    try:
        schema_name = getattr(schema, "__name__", "UnnamedSchema")
        _logger.debug(f"Translating schema '{schema_name}' to Google format...")

        properties = {}
        for field in schema.fields:
            if isinstance(field, NestedField):
                properties[field.name] = _convert_nested_field(field)
            elif isinstance(field, ArrayField):
                properties[field.name] = _convert_array_field(field)
            else:
                properties[field.name] = _convert_field_to_schema(field)

        return content.Schema(
            type=content.Type.OBJECT,
            properties=properties,
            required=schema.get_required_fields()
        )

    except Exception as e:
        _logger.error(f"Error translating schema to Google format: {e}")
        _logger.debug("Translation error details", exc_info=True)
        return content.Schema()

def from_google(
        schema: content.Schema,
        schema_name: str = "Schema"
    ) -> Type[Schema]:
    """
    Convert a Google Gemini schema to belso format.\n
    ---
    ### Args
    - `schema` (`content.Schema`): the Google schema.
    - `schema_name` (`str`, optional): the prefix to add to the schema name. Defaults to "Schema".\n
    ---
    ### Returns
    - `Type[Schema]`: the converted belso schema.
    """
    try:
        _logger.debug("Starting conversion from Google schema to belso format...")

        schema_class_name = f"{schema_name}Schema"
        ConvertedSchema = type(schema_class_name, (Schema,), {"fields": []})

        required_fields = set(schema.required)
        properties = schema.properties

        for name, prop in properties.items():
            field_type = _REVERSE_GOOGLE_TYPE_MAP.get(prop.type, str)
            description = prop.description or ""
            required = name in required_fields
            default = None

            # Nested object
            if prop.type == content.Type.OBJECT and prop.properties:
                nested_schema = content.Schema(
                    type=content.Type.OBJECT,
                    properties=prop.properties,
                    required=prop.required
                )
                ConvertedSchema.fields.append(
                    NestedField(
                        name=name,
                        schema=from_google(nested_schema, schema_name=f"{name}"),
                        description=description,
                        required=required
                    )
                )
            # Array
            elif prop.type == content.Type.ARRAY and prop.items:
                items_type = _REVERSE_GOOGLE_TYPE_MAP.get(prop.items.type, str)
                ConvertedSchema.fields.append(
                    ArrayField(
                        name=name,
                        items_type=items_type,
                        description=description,
                        required=required
                    )
                )
            # Primitive
            else:
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
        _logger.error(f"Error converting Google schema to belso format: {e}")
        _logger.debug("Conversion error details", exc_info=True)
        return create_fallback_schema()
