# belso.gui.components.field_editor

import logging
from typing import Optional, List

from belso.core.field import Field

logger = logging.getLogger(__name__)

def open_field_editor_data(existing_field:Optional[Field]=None) -> dict:
    """
    Open the field editor with the given field data.
    If no field is given, open the editor with empty fields.\n
    ---
    ### Args
    - `existing_field` (`Optional[Field]`): field to edit.\n
    ---
    ### Returns
    - `dict`: field data for the editor.
    """
    logger.info("Opening field editor...")

    # Dati di base
    field_data = {
        "name": existing_field.name if existing_field else "",
        "type": existing_field.type_.__name__ if existing_field else "str",
        "description": existing_field.description if existing_field else "",
        "required": existing_field.required if existing_field else True,
        "default": existing_field.default if existing_field else "",
    }

    # Aggiungi opzioni specifiche per tipo se il campo esiste
    if existing_field:
        # Opzioni per stringhe
        if hasattr(existing_field, "length_range"):
            field_data["length_range"] = existing_field.length_range
        if hasattr(existing_field, "regex"):
            field_data["regex"] = existing_field.regex
        if hasattr(existing_field, "format_"):
            field_data["format_"] = existing_field.format_

        # Opzioni per numeri
        if hasattr(existing_field, "range_"):
            field_data["range_"] = existing_field.range_
        if hasattr(existing_field, "exclusive_range"):
            field_data["exclusive_range"] = existing_field.exclusive_range
        if hasattr(existing_field, "multiple_of"):
            field_data["multiple_of"] = existing_field.multiple_of

        # Opzioni per liste
        if hasattr(existing_field, "items_range"):
            field_data["items_range"] = existing_field.items_range

        # Opzioni per oggetti/dizionari
        if hasattr(existing_field, "properties_range"):
            field_data["properties_range"] = existing_field.properties_range

        # Opzione enum comune a tutti i tipi
        if hasattr(existing_field, "enum"):
            field_data["enum"] = existing_field.enum

    return field_data

def get_field_type_options(type_name: str) -> List[str]:
    """
    Restituisce le opzioni disponibili per un tipo di campo specifico.\n
    ---
    ### Args
    - `type_name` (`str`): nome del tipo di campo.\n
    ---
    ### Returns
    - `List[str]`: lista delle opzioni disponibili.
    """
    # Opzioni comuni a tutti i tipi
    common_options = ["enum"]

    # Opzioni specifiche per tipo
    type_options = {
        "str": ["length_range", "regex", "format_"],
        "int": ["range_", "exclusive_range", "multiple_of"],
        "float": ["range_", "exclusive_range", "multiple_of"],
        "bool": [],
        "list": ["items_range"],
        "dict": ["properties_range"],
    }

    return common_options + type_options.get(type_name, [])
