# belso.gui.handlers.field_handlers

import logging
from typing import Optional, List, Any, Tuple

import gradio as gr

from belso.core.field import Field
from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP

logger = logging.getLogger(__name__)

def _merge_range(
        min_val: str,
        max_val: str
    ) -> Optional[tuple]:
    """
    Merge min and max values into a range tuple.\n
    ---
    ### Args
    - `min_val` (`str`): minimum value as string.
    - `max_val` (`str`): maximum value as string.\n
    ---
    ### Returns
    - `Optional[tuple]`: tuple (min, max) or None if both values are empty.
    """
    if not min_val.strip() and not max_val.strip():
        return None

    try:
        # Parse min value
        if min_val.strip():
            min_parsed = int(min_val.strip()) if min_val.strip().isdigit() else float(min_val.strip())
        else:
            min_parsed = 0  # Default minimum value

        # Parse max value
        if max_val.strip():
            max_parsed = int(max_val.strip()) if max_val.strip().isdigit() else float(max_val.strip())
        else:
            max_parsed = float('inf')  # Default to infinity if not specified

        return (min_parsed, max_parsed)
    except (ValueError, IndexError):
        logger.warning(f"Invalid range values: min={min_val}, max={max_val}")
        return None

def _parse_enum(enum_str: str) -> Optional[List[Any]]:
    """
    Convert an enum string into a list of values.\n
    ---
    ### Args
    - `enum_str` (`str`): enum string with comma-separated values.\n
    ---
    ### Returns
    - `Optional[List[Any]]`: list of values or None if the string is empty.
    """
    if not enum_str or enum_str.strip() == "":
        return None

    return [item.strip() for item in enum_str.split(",")]

def handle_add_field(
        name: str,
        type_: str,
        desc: str,
        req: bool,
        default: str,
        state: GUIState,
        schema_name: str = "",
        length_min: str = "",
        length_max: str = "",
        regex: str = "",
        format_: str = "",
        range_min: str = "",
        range_max: str = "",
        exclusive_min: str = "",
        exclusive_max: str = "",
        multiple_of: Optional[float] = None,
        items_min: str = "",
        items_max: str = "",
        properties_min: str = "",
        properties_max: str = "",
        enum: str = ""
    ) -> Tuple[GUIState, str]:
    """
    Open the field editor to add a new field.\n
    ---
    ### Args
    - `name` (`str`): The name of the field.
    - `type_` (`str`): The type of the field.
    - `desc` (`str`): The description of the field.
    - `req` (`bool`): Whether the field is required.
    - `default` (`str`): The default value of the field.
    - `state` (`GUIState`): The current GUI state.
    - `schema_name` (`str`): The name of the schema.
    - `length_min` (`str`): Minimum length for strings.
    - `length_max` (`str`): Maximum length for strings.
    - `regex` (`str`): Regular expression for validating strings.
    - `format_` (`str`): Format for validating strings.
    - `range_min` (`str`): Minimum value for numbers.
    - `range_max` (`str`): Maximum value for numbers.
    - `exclusive_min` (`str`): Exclusive minimum value for numbers.
    - `exclusive_max` (`str`): Exclusive maximum value for numbers.
    - `multiple_of` (`Optional[float]`): Multiple of valid numeric values.
    - `items_min` (`str`): Minimum number of items in a list.
    - `items_max` (`str`): Maximum number of items in a list.
    - `properties_min` (`str`): Minimum number of properties in an object.
    - `properties_max` (`str`): Maximum number of properties in an object.
    - `enum` (`str`): List of valid values.\n
    ---
    ### Returns
    - `Tuple[GUIState, str]`: The updated GUI state and the name of the schema.
    """
    schema = state.schemas.get(schema_name)
    if not schema:
        logger.warning(f"No schema found with name: {schema_name}")
        return state.clone(), ""  # Return empty string as second value

    py_type = _FILE_TYPE_MAP.get(type_, str)

    kwargs = {
        "name": name,
        "type": py_type,
        "description": desc,
        "required": req,
        "default": default or None,
    }

    # String
    if length_min.strip() or length_max.strip():
        length_range = _merge_range(length_min, length_max)
        if length_range:
            kwargs["length_range"] = length_range

    if regex.strip():
        kwargs["regex"] = regex.strip()

    if format_.strip():
        kwargs["format"] = format_.strip()

    # Number
    if range_min.strip() or range_max.strip():
        range_ = _merge_range(range_min, range_max)
        if range_:
            kwargs["range"] = range_

    if exclusive_min.strip() or exclusive_max.strip():
        exclusive_range = _merge_range(exclusive_min, exclusive_max)
        if exclusive_range:
            kwargs["exclusive_range"] = exclusive_range

    if isinstance(multiple_of, (int, float)) and multiple_of != 0:
        kwargs["multiple_of"] = float(multiple_of)

    # List
    if items_min.strip() or items_max.strip():
        items_range = _merge_range(items_min, items_max)
        if items_range:
            kwargs["items_range"] = items_range

    # Dict
    if properties_min.strip() or properties_max.strip():
        properties_range = _merge_range(properties_min, properties_max)
        if properties_range:
            kwargs["properties_range"] = properties_range

    # Enum (comune)
    parsed_enum = _parse_enum(enum)
    if parsed_enum:
        kwargs["enum"] = parsed_enum

    # Creazione campo
    new_field = Field(**kwargs)

    if state.selected_field:
        logger.info("Editing existing field...")
        schema.fields = [
            new_field if f.name == state.selected_field.name else f
            for f in schema.fields
        ]
    else:
        logger.info("Adding new field...")
        schema.fields.append(new_field)

    state.set_selected_field(None)

    # Ensure we stay on the current schema by setting it as active
    state.active_schema_name = schema_name

    return state.clone(), schema_name

def handle_edit_field(
        state: GUIState,
        field: Field
    ) -> GUIState:
    """
    Open the field editor to edit an existing field.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `field` (`Field`): The field to edit.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    state.set_selected_field(field)
    return state.clone()

def handle_remove_field(
        state: GUIState,
        schema: Schema,
        field: Field
    ) -> GUIState:
    """
    Remove a field from a schema.\n
    ---
    ### Args
    - `state` (`GUIState`): The current GUI state.
    - `schema` (`Schema`): The schema containing the field.
    - `field` (`Field`): The field to remove.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    logger.info(f"Removing field \"{field.name}\" from schema \"{schema.__name__}\".")
    try:
        schema.fields = [f for f in schema.fields if f.name != field.name]
        logger.info("Field removed successfully.")
        return state.clone()
    except Exception as e:
        logger.error(f"Error removing field: {e}")
        return state.clone()

def handle_type_change(type_: str) -> tuple:
    """
    Handle type change in the field editor.\n
    ---
    ### Args
    - `type_` (`str`): the new type.\n
    ---
    ### Returns
    - `tuple`: visibility and values for all field options.
    """
    # Determine visibility based on type
    is_str = type_ == "str"
    is_num = type_ in ["int", "float"]
    is_list = type_ == "list"
    is_dict = type_ == "dict"

    return (
        # Prima aggiorna visibilità dei gruppi
        gr.update(visible=is_str),   # str_options
        gr.update(visible=is_num),   # num_options
        gr.update(visible=is_list),  # list_options
        gr.update(visible=is_dict),  # dict_options

        # Poi i valori/visibilità dei singoli componenti
        gr.update(visible=is_str, value=""), gr.update(visible=is_str, value=""),
        gr.update(visible=is_str, value=""), gr.update(visible=is_str, value=""),

        gr.update(visible=is_num, value=""), gr.update(visible=is_num, value=""),
        gr.update(visible=is_num, value=""), gr.update(visible=is_num, value=""),
        gr.update(visible=is_num, value=None),

        gr.update(visible=is_list, value=""), gr.update(visible=is_list, value=""),
        gr.update(visible=is_dict, value=""), gr.update(visible=is_dict, value=""),
    )
