# belso.gui.logic.schema_manager

"""
Schema management logic.
---
Handles creation, build, retrieval, export, and import of schemas.
"""

import json

from belso.core.schema import Schema
from belso.gui.logic.state import state
from belso.utils.formats import FORMATS
from belso.utils.logging import get_logger
from belso.core.processor import SchemaProcessor

logger = get_logger(__name__)

def create_schema(name: str):
    """
    Initializes a new schema in the state.\n
    ---
    ### Args
    - `name` (`str`): schema name.
    """
    logger.debug(f"Creating schema: {name}")
    state.set_current_schema(name)
    state.set_fields([])
    state.set_schema(name, type(name, (Schema,), {"fields": []}))

def get_schema_fields(name: str) -> list:
    """
    Returns the fields of the specified schema.\n
    ---
    ### Args
    - `name` (`str`): schema name.\n
    ---
    ### Returns
    - `list`: list of dicts for each field.
    """
    schema = state.get_schema(name)
    if not schema:
        return []

    rows = []
    for f in schema.fields:
        row = {
            "Nome": f.name,
            "Tipo": f.__class__.__name__.replace("Field", ""),
            "Obbligatorio": "✅" if f.required else "❌",
            "Descrizione": f.description,
            "Schema Ref": getattr(f, "schema", getattr(f, "items_type", ""))
        }
        rows.append(row)
    return rows

def build_schema() -> Schema:
    """
    Builds the schema class from current field buffer.\n
    ---
    ### Returns
    - `Schema`: compiled schema class.
    """
    name = state.get_current_schema_name()
    fields = state.get_fields()
    logger.debug(f"Building schema: {name} with {len(fields)} fields")

    built_fields = []
    for f in fields:
        built_fields.append(f)

    schema_cls = type(name, (Schema,), {"fields": built_fields})
    state.set_schema(name, schema_cls)
    return schema_cls

def export_schema(schema_name: str, format_type: str = FORMATS.JSON) -> str:
    """
    Renders a schema to a JSON string in the selected format.\n
    ---
    ### Args
    - `schema_name` (`str`): name of the schema.
    - `format_type` (`str`): output format.\n
    ---
    ### Returns
    - `str`: schema as JSON.
    """
    schema = build_schema()
    try:
        data = SchemaProcessor.convert(schema, to=format_type)
        return json.dumps(data, indent=2)
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return f"Errore durante esportazione: {str(e)}"

def import_schema_from_json(json_str: str) -> str:
    """
    Imports a schema from a JSON string.\n
    ---
    ### Args
    - `json_str` (`str`): input string.\n
    ---
    ### Returns
    - `str`: status message.
    """
    try:
        raw = json.loads(json_str)
        schema: Schema = SchemaProcessor.load(raw)

        name = schema.__name__
        state.set_current_schema(name)
        state.set_schema(name, schema)
        state.set_fields(schema.fields)

        return f"✅ Schema '{name}' importato con {len(schema.fields)} campi."
    except Exception as e:
        logger.error(f"Import failed: {e}")
        return f"❌ Errore importazione: {str(e)}"
