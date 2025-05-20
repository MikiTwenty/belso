# belso.gui.components.field_editor

from typing import Optional

from belso.core.field import Field

def open_field_editor_data(
        existing_field: Optional[Field] = None
    ) -> dict:
    return {
        "name": existing_field.name if existing_field else "",
        "type": existing_field.type.__name__ if existing_field else "str",
        "description": existing_field.description if existing_field else "",
        "required": existing_field.required if existing_field else True,
        "default": existing_field.default if existing_field else "",
    }
