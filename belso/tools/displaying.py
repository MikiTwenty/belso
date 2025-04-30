# belso.tools.displaying

import logging
from typing import Any, Type,  Optional

from rich import box
from rich.table import Table
from rich.console import Console

from belso.core.schema import Schema
from belso.core.field import NestedField, ArrayField

_logger = logging.getLogger(__name__)

_console = Console()

def display_schema(
        schema: [Type[Schema]]
    ) -> None:
    """
    Pretty-print a schema using colors and better layout, including nested fields.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the belso schema to print.
    """
    try:
        def _display_schema(schema_cls: Type[Schema], indent: int = 0, parent_path: str = ""):
            # Get clean schema name without parent prefixes
            schema_name = schema_cls.__name__
            if "." in schema_name:
                # Extract the last part of the name after the last underscore
                parts = schema_name.split(".")
                if len(parts) > 1 and parts[-1] == "Schema":
                    clean_name = parts[-1]
                else:
                    clean_name = parts[-1]
            else:
                clean_name = schema_name

            # Create _display name with parent.child notation if there's a parent path
            # Only include schema names, not field names
            display_name = f"{parent_path}.{clean_name}" if parent_path else clean_name

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

                # Nested field
                if isinstance(field, NestedField):
                    # Get clean nested schema name
                    nested_name = field.schema.__name__
                    if nested_name.endswith("Schema"):
                        nested_clean_name = nested_name[:-6]  # Remove "Schema" suffix
                    elif "." in nested_name:
                        parts = nested_name.split(".")
                        if len(parts) > 1 and parts[-1] == "Schema":
                            nested_clean_name = parts[-2]  # Use the part before "Schema"
                        else:
                            nested_clean_name = parts[-1]
                    else:
                        nested_clean_name = nested_name

                    nested_type = f"object ({nested_clean_name})"
                    table.add_row(field.name, nested_type, required, default, description)
                # Array of objects
                elif isinstance(field, ArrayField) and hasattr(field, "items_type") and isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
                    # Get clean array item schema name
                    items_name = field.items_type.__name__
                    if items_name.endswith("Schema"):
                        items_clean_name = items_name[:-6]  # Remove "Schema" suffix
                    elif "." in items_name:
                        parts = items_name.split(".")
                        if len(parts) > 1 and parts[-1] == "Schema":
                            items_clean_name = parts[-2]  # Use the part before "Schema"
                        else:
                            items_clean_name = parts[-1]
                    else:
                        items_clean_name = items_name

                    array_type = f"array[{items_clean_name}]"
                    table.add_row(field.name, array_type, required, default, description)
                # Primitive
                else:
                    field_type = field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_)
                    table.add_row(field.name, field_type, required, default, description)

            _console.print(table)

            # Recursive printing of nested fields
            for field in schema_cls.fields:
                if isinstance(field, NestedField):
                    # Pass only the schema name to the parent path, not the field name
                    new_parent_path = display_name
                    _display_schema(field.schema, indent + 1, new_parent_path)
                elif isinstance(field, ArrayField) and hasattr(field, "items_type") and isinstance(field.items_type, type) and issubclass(field.items_type, Schema):
                    # Pass only the schema name to the parent path, not the field name
                    new_parent_path = display_name
                    _display_schema(field.items_type, indent + 1, new_parent_path)

        _display_schema(schema)

    except Exception as e:
        _logger.error(f"Error printing schema: {e}")
        _logger.debug("Schema printing error details", exc_info=True)
        _console.print(f"[bold red]Error printing schema: {e}")
