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
        indent: int = 0,
        parent_path: str = "",
        seen_counter: Optional[Dict[int, int]] = None
    ) -> None:
    """
    Recursive function to display a schema with nested fields.
    ---
    ### Args
    - `schema_cls` (`Type[Schema]`): the belso schema to print.
    - `indent` (`int`, optional): the indentation level. Defaults to 0.
    - `parent_path` (`str`, optional): the parent path of the schema. Defaults to "".
    - `seen_counter` (`Dict[int, int]`, optional): keeps track of schema instances to detect duplication.
    """
    if seen_counter is None:
        seen_counter = {}

    # Count repeated schema usage
    schema_id = id(schema_cls)
    count = seen_counter.get(schema_id, 0)
    seen_counter[schema_id] = count + 1

    # Base schema name
    schema_name = schema_cls.__name__
    display_base = f"{parent_path}.{schema_name}" if parent_path else schema_name
    display_name = f"{display_base}[{count}]" if count > 0 else display_base

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

    # Recursively display nested schemas
    for field in schema_cls.fields:
        if isinstance(field, NestedField):
            _display_schema(field.schema, indent + 1, display_name, seen_counter)
        elif isinstance(field, ArrayField) and isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
            _display_schema(field.items_type, indent + 1, display_name, seen_counter)

def display_schema(schema: Type[Schema]) -> None:
    """
    Pretty-print a schema using colors and better layout, including nested fields.
    ---
    ### Args
    - `schema` (`Type[Schema]`): the belso schema to print.
    """
    try:
        _display_schema(schema, seen_counter={})
    except Exception as e:
        _logger.error(f"Error printing schema: {e}")
        _logger.debug("Schema printing error details", exc_info=True)
        _console.print(f"[bold red]Error printing schema: {e}")
