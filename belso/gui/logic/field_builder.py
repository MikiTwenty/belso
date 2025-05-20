# belso.gui.logic.field_builder

"""
Field Builder.
---
Parses UI inputs and builds appropriate field instances for schema.
"""

from typing import Optional, Tuple

from belso.gui.utils import DynamicField
from belso.utils.logging import get_logger

logger = get_logger(__name__)

def build_field_from_inputs(
        name: str,
        type_: str,
        description: str,
        required: bool,
        enum: str,
        regex: str,
        range_min: float,
        range_max: float,
        multiple_of: float,
        length_min: int,
        length_max: int,
        items_min: int,
        items_max: int,
        nested_schema: str,
        items_type: str
    ) -> Tuple[Optional[DynamicField], str]:
    """
    Builds a DynamicField instance from UI input values.
    ---
    ### Returns
    - `Tuple[Optional[DynamicField], str]`: result and message.
    """
    if not name:
        return None, "❌ Il nome del campo è obbligatorio."
    if not type_:
        return None, "❌ Specificare il tipo di campo."

    kwargs = {
        "name": name,
        "type_": type_,
        "description": description,
        "required": required,
    }

    # Validate optional fields
    if enum:
        kwargs["enum"] = [x.strip() for x in enum.split(",") if x.strip()]
    if regex:
        kwargs["regex"] = regex
    if range_min is not None and range_max is not None:
        kwargs["range_"] = (range_min, range_max)
    if multiple_of:
        kwargs["multiple_of"] = multiple_of
    if length_min is not None and length_max is not None:
        kwargs["length_range"] = (length_min, length_max)
    if items_min is not None and items_max is not None:
        kwargs["items_range"] = (items_min, items_max)
    if type_ == "nested" and nested_schema:
        kwargs["nested_schema"] = nested_schema
    if type_ == "array" and items_type:
        kwargs["items_type"] = items_type

    try:
        field = DynamicField(**kwargs)
        logger.debug(f"✅ Campo costruito: {field.name} ({field.type_})")
        return field, f"✅ Campo '{field.name}' aggiunto."
    except Exception as e:
        logger.error(f"Errore creazione campo: {e}")
        return None, f"❌ Errore nella creazione del campo: {str(e)}"
