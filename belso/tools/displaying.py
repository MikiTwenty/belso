# belso.tools.displaying

import logging
from typing import Type, Optional, Dict

from rich import box
from rich.table import Table
from rich.console import Console

from belso.core.schema import Schema
from belso.core.field import NestedField, ArrayField

_logger = logging.getLogger(__name__)

_console = Console()

def _display_schema(
        schema_cls: Type[Schema],
        parent_path: str = "",
        seen_counter: Optional[Dict[str, int]] = None,
        visited_ids: Optional[Dict[int, str]] = None
    ) -> None:
    """
    Recursive function to display a schema with nested fields.\n
    ---
    ### Args
    - `schema_cls` (Type[Schema]): The schema class to display.
    - `parent_path` (str): The parent path of the schema. Defaults to "".
    - `seen_counter` (Optional[Dict[str, int]], optional): Counter for duplicate contexts. Defaults to None.
    - `visited_ids` (Optional[Dict[int, str]], optional): Dictionary of visited schema IDs. Defaults to None.\n
    """
    if seen_counter is None:
        seen_counter = {}
    if visited_ids is None:
        visited_ids = {}

    schema_id = id(schema_cls)

    # Usa il path intero per identificare contesti duplicati
    path_key = parent_path or schema_cls.__name__
    count = seen_counter.get(path_key, 0)
    seen_counter[path_key] = count + 1

    # Aggiungi l'indice solo se il path è ricorrente
    display_name = f"{path_key}[{count}]" if count > 1 else path_key

    # Salta stampa duplicata se già visitato con stesso path
    if visited_ids.get(schema_id) == path_key:
        return
    visited_ids[schema_id] = path_key

    table = Table(
        title=f"\n[bold blue]{display_name}",
        box=box.ROUNDED,
        expand=False,
        show_lines=True
    )
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Required", style="green")
    table.add_column("Default", style="yellow")
    table.add_column("Description", style="white")

    for field in schema_cls.fields:
        required = "✅" if field.required else "❌"
        default = str(field.default) if field.default is not None else "-"
        description = field.description or "-"

        if isinstance(field, NestedField):
            type_name = f"object ({field.schema.__name__})"
        elif isinstance(field, ArrayField) and isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
            type_name = f"array[{field.items_type.__name__}]"
        else:
            type_name = field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_)

        table.add_row(field.name, type_name, required, default, description)

    _console.print(table)

    # Visita ricorsiva per Nested e ArrayField
    for field in schema_cls.fields:
        field_path = f"{path_key}.{field.name}"
        if isinstance(field, NestedField):
            _display_schema(field.schema, field_path, seen_counter, visited_ids)
        elif isinstance(field, ArrayField) and isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
            _display_schema(field.items_type, field_path, seen_counter, visited_ids)

def display_schema(schema: Type[Schema]) -> None:
    """
    Display a schema with nested fields.\n
    ---
    ### Args
    - `schema` (Type[Schema]): The schema to display.\n
    """
    try:
        _display_schema(schema, seen_counter={}, visited_ids={})
    except Exception as e:
        _logger.error(f"Error printing schema: {e}")
        _logger.debug("Schema printing error details", exc_info=True)
        _console.print(f"[bold red]Error printing schema: {e}")
