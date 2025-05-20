# belso.gui.components.field_editor

import logging
from typing import Optional

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
    return {
        "name": existing_field.name if existing_field else "",
        "type": existing_field.type_.__name__ if existing_field else "str",
        "description": existing_field.description if existing_field else "",
        "required": existing_field.required if existing_field else True,
        "default": existing_field.default if existing_field else "",
    }
