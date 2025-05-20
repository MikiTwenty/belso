# belso.gui.handlers.field_handlers

import logging
from typing import Optional, List, Any

import gradio as gr

from belso.core.field import Field
from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP

logger = logging.getLogger(__name__)

def _parse_range(range_str: str) -> Optional[tuple]:
    """
    Converte una stringa di intervallo in una tupla.\n
    ---
    ### Args
    - `range_str` (`str`): stringa di intervallo nel formato "min,max".\n
    ---
    ### Returns
    - `Optional[tuple]`: tupla (min, max) o None se la stringa è vuota o invalida.
    """
    if not range_str or range_str.strip() == "":
        return None

    try:
        parts = range_str.split(",")
        if len(parts) != 2:
            return None

        min_val = int(parts[0].strip()) if parts[0].strip().isdigit() else float(parts[0].strip())
        max_val = int(parts[1].strip()) if parts[1].strip().isdigit() else float(parts[1].strip())

        return (min_val, max_val)
    except (ValueError, IndexError):
        logger.warning(f"Formato intervallo non valido: {range_str}")
        return None

def _parse_enum(enum_str: str) -> Optional[List[Any]]:
    """
    Converte una stringa di enum in una lista di valori.\n
    ---
    ### Args
    - `enum_str` (`str`): stringa di enum con valori separati da virgola.\n
    ---
    ### Returns
    - `Optional[List[Any]]`: lista di valori o None se la stringa è vuota.
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
        length_range: str = "",
        regex: str = "",
        format_: str = "",
        range_: str = "",
        exclusive_range: str = "",
        multiple_of: Optional[float] = None,
        items_range: str = "",
        properties_range: str = "",
        enum: str = ""
    ) -> GUIState:
    """
    Open the field editor to add a new field.\n
    ---
    ### Args
    - `name` (`str`): The name of the field.
    - `type_` (`str`): The type of the field.
    - `desc` (`str`): The description of the field.
    - `req` (`bool`): Whether the field is required.
    - `default` (`str`): The default value of the field.
    - `length_range` (`str`): Range of valid string lengths.
    - `regex` (`str`): Regular expression for validating strings.
    - `format_` (`str`): Format for validating strings.
    - `range_` (`str`): Range of valid numeric values.
    - `exclusive_range` (`str`): Exclusive range of valid numeric values.
    - `multiple_of` (`Optional[float]`): Multiple of valid numeric values.
    - `items_range` (`str`): Range of valid list items.
    - `properties_range` (`str`): Range of valid object properties.
    - `enum` (`str`): List of valid values.
    - `state` (`GUIState`): The current GUI state.\n
    ---
    ### Returns
    - `GUIState`: The updated GUI state.
    """
    schema = state.get_active_schema()
    if not schema:
        logger.warning("No active schema found.")
        return state.clone()

    py_type = _FILE_TYPE_MAP.get(type_, str)

    # Prepara i parametri avanzati
    kwargs = {
        "name": name,
        "type": py_type,
        "description": desc,
        "required": req,
        "default": default or None,
    }

    # Aggiungi parametri specifici per tipo
    if type_ == "str":
        if length_range:
            kwargs["length_range"] = _parse_range(length_range)
        if regex and regex.strip():
            kwargs["regex"] = regex.strip()
        if format_ and format_.strip():
            kwargs["format"] = format_.strip()

    if type_ in ["int", "float"]:
        if range_:
            kwargs["range"] = _parse_range(range_)
        if exclusive_range:
            kwargs["exclusive_range"] = _parse_range(exclusive_range)
        if multiple_of is not None:
            kwargs["multiple_of"] = multiple_of

    if type_ == "list" and items_range:
        kwargs["items_range"] = _parse_range(items_range)

    if type_ == "dict" and properties_range:
        kwargs["properties_range"] = _parse_range(properties_range)

    # Enum è comune a tutti i tipi
    if enum:
        kwargs["enum"] = _parse_enum(enum)

    # Crea il nuovo campo con tutti i parametri
    new_field = Field(**kwargs)

    if state.selected_field:
        logger.info("Editing existing field...")
        # Edit mode
        schema.fields = [
            new_field if f.name == state.selected_field.name else f
            for f in schema.fields
        ]
    else:
        logger.info("Adding new field...")
        schema.fields.append(new_field)

    state.set_selected_field(None)
    return state.clone()

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
    logger.info(f"Removing field \"{field.name}\" from schema \"{schema.name}\".")
    try:
        schema.fields = [f for f in schema.fields if f.name != field.name]
        logger.info("Field removed successfully.")
        return state.clone()
    except Exception as e:
        logger.error(f"Errore nella rimozione campo: {e}")

def handle_type_change(
        t: str,
        length_range: str,
        regex: str,
        format_: str,
        range_: str,
        exclusive_range: str,
        multiple_of: Optional[float],
        items_range: str,
        properties_range: str
    ) -> tuple:
    """
    Update visibility and reset values depending on field type.\n
    ---
    ### Args
    - `t` (`str`): The selected field type.
    - `length_range` (`str`): Range of valid string lengths.
    - `regex` (`str`): Regular expression for validating strings.
    - `format_` (`str`): Format for validating strings.
    - `range_` (`str`): Range of valid numeric values.
    - `exclusive_range` (`str`): Exclusive range of valid numeric values.
    - `multiple_of` (`Optional[float]`): Multiple of valid numeric values.
    - `items_range` (`str`): Range of valid list items.
    - `properties_range` (`str`): Range of valid object properties.\n
    ---
    ### Returns
    - `tuple`: Updated visibility and reset values for fields.
    """
    return (
        gr.update(visible=t == "str"),  # str_options
        gr.update(visible=t in ["int", "float"]),  # num_options
        gr.update(visible=t == "list"),  # list_options
        gr.update(visible=t == "dict"),  # dict_options

        "" if t != "str" else length_range,  # length_range
        "" if t != "str" else regex,  # regex
        "" if t != "str" else format_,  # format_

        "" if t not in ["int", "float"] else range_,  # range_
        "" if t not in ["int", "float"] else exclusive_range,  # exclusive_range
        None if t not in ["int", "float"] else multiple_of,  # multiple_of

        "" if t != "list" else items_range,  # items_range
        "" if t != "dict" else properties_range  # properties_range
    )
