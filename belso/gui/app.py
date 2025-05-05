# belso.gui.app

import json
from typing import List, Type

import gradio as gr

from belso.core.schema import Schema
from belso.utils.formats import FORMATS
from belso.gui.utils import DynamicField
from belso.utils.logging import get_logger
from belso.core.processor import SchemaProcessor
from belso.core.field import Field, NestedField, ArrayField
from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP

_logger = get_logger(__name__)

class SchemaGenerator:
    fields = []
    schemas = {}  # Store created schemas for reuse
    current_schema = None  # Track the schema being edited

    @classmethod
    def add_field(
            cls,
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
            items_min: int = None,
            items_max: int = None,
            nested_schema: str = None,
            items_type: str = None
        ) -> str:
        """
        Adds a field to the current schema.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `type_` (`str`): the type of the field.
        - `description` (`str`): the description of the field.
        - `required` (`bool`): whether the field is required.
        - `enum` (`str`): the enum of the field.
        - `regex` (`str`): the regex of the field.
        - `range_min` (`float`): the minimum value of the field.
        - `range_max` (`float`): the maximum value of the field.
        - `multiple_of` (`float`): the multiple of the field.
        - `length_min` (`int`): the minimum length of the field.
        - `length_max` (`int`): the maximum length of the field.
        - `items_min` (`int`, optional): the minimum items of the field. Defaults to `None`.
        - `items_max` (`int`, optional): the maximum items of the field. Defaults to `None`.
        - `nested_schema` (`str`, optional): the nested schema of the field. Defaults to `None`.
        - `items_type` (`str`, optional): the items type of the field. Defaults to `None`.
        ---
        ### Returns
        - `str`: the status of the operation.
        """
        _logger.debug(f"Adding field \"{name}\"...")
        if not name:
            _logger.warning("Field name is empty. Skipping...")
            return "Field name is required."

        if not type_:
            _logger.warning("Field type is empty. Skipping...")
            return "Field type is required."

        kwargs = {
            "name": name,
            "type_": type_,
            "description": description,
            "required": required
        }

        # Process validation parameters
        if enum:
            kwargs["enum"] = [item.strip() for item in enum.split(",")]
        if regex:
            kwargs["regex"] = regex
        if range_min is not None and range_max is not None:
            kwargs["range_"] = (range_min, range_max)
        if multiple_of is not None:
            kwargs["multiple_of"] = multiple_of
        if length_min is not None and length_max is not None:
            kwargs["length_range"] = (length_min, length_max)
        if items_min is not None and items_max is not None:
            kwargs["items_range"] = (items_min, items_max)

        # Handle nested schemas and array items
        if type_ == "nested" and nested_schema:
            kwargs["nested_schema"] = nested_schema
        if type_ == "array" and items_type:
            kwargs["items_type"] = items_type

        cls.fields.append(DynamicField(**kwargs))
        _logger.debug(f"Field \"{name}\" added.")
        return f"Field \"{name}\" added."

    @classmethod
    def build_schema(
            cls,
            schema_name: str
        ) -> Type[Schema]:
        """
        Builds a Belso schema class from the current set of fields.\n
        ---
        ### Args
        - `schema_name` (`str`): the name of the schema. Defaults to "UnnamedSchema".\n
        ---
        ### Returns
        - `Type[Schema]`: the Belso schema class.
        """
        _logger.debug(f"Building schema \"{schema_name}\"...")
        if not schema_name:
            _logger.warning("Schema name is empty. Using default name...")
            schema_name = "UnnamedSchema"

        field_objs = []
        for field in cls.fields:
            field: DynamicField = field
            # Handle different field types
            if field.type_ == "nested" and field.nested_schema in cls.schemas:
                # Create a nested field using an existing schema
                nested_schema = cls.schemas[field.nested_schema]
                field_obj = NestedField(
                    name=field.name,
                    schema=nested_schema,
                    description=field.description,
                    required=field.required
                )
            elif field.type_ == "array":
                # Create an array field
                items_type = _FILE_TYPE_MAP.get(field.items_type, str)

                # Check if items_type is a schema
                if field.items_type in cls.schemas:
                    items_type = cls.schemas[field.items_type]

                kwargs = {
                    "name": field.name,
                    "items_type": items_type,
                    "description": field.description,
                    "required": field.required
                }

                if field.items_range:
                    kwargs["items_range"] = field.items_range

                field_obj = ArrayField(**kwargs)
            else:
                # Create a regular field
                base_type = _FILE_TYPE_MAP.get(field.type_, str)
                kwargs = {
                    "name": field.name,
                    "type": base_type,
                    "description": field.description,
                    "required": field.required
                }

                # Add validation parameters
                if field.enum: kwargs["enum"] = field.enum
                if field.regex: kwargs["regex"] = field.regex
                if field.range_: kwargs["range"] = field.range_
                if field.multiple_of: kwargs["multiple_of"] = field.multiple_of
                if field.length_range: kwargs["length_range"] = field.length_range

                field_obj = Field(**kwargs)

            field_objs.append(field_obj)

        # Create the schema class
        schema_class = type(schema_name, (Schema,), {"fields": field_objs})

        # Store the schema for future reference
        cls.schemas[schema_name] = schema_class
        cls.current_schema = schema_name

        _logger.debug(f"Schema \"{schema_name}\" built.")
        return schema_class

    @classmethod
    def render_schema(
            cls,
            schema_name: str,
            format_type: str = FORMATS.JSON
        ) -> str:
        """
        Renders the current schema as a JSON string.\n
        ---
        ### Args
        - `schema_name` (`str`): the name of the schema.
        - `format_type` (`str`, optional): the format of the schema. Defaults to `FORMATS.JSON`.\n
        ---
        ### Returns
        - `str`: the JSON string of the schema.
        """
        _logger.debug(f"Rendering schema \"{schema_name}\" in format \"{format_type}\"...")
        if not cls.fields:
            _logger.warning("No fields defined. Skipping...")
            return "No fields defined. Add fields to create a schema."

        schema_class = cls.build_schema(schema_name)

        try:
            schema = SchemaProcessor.convert(schema_class, to=format_type)
            return json.dumps(schema, indent=2)
        except Exception as e:
            _logger.error(f"Error rendering schema: {str(e)}")
            return f"Error rendering schema: {str(e)}"

    @classmethod
    def save_schema(
            cls,
            schema_name: str
        ) -> str:
        """
        Saves the current schema.\n
        ---
        ### Args
        - `schema_name` (`str`): the name of the schema.\n
        ---
        ### Returns
        - `str`: the status of the operation.
        """
        _logger.debug(f"Saving schema \"{schema_name}\"...")
        if not cls.fields:
            _logger.warning("No fields defined. Skipping...")
            return "No fields defined. Add fields to create a schema."

        schema_class = cls.build_schema(schema_name)
        cls.schemas[schema_name] = schema_class
        cls.reset_fields()
        _logger.debug(f"Schema \"{schema_name}\" saved.")
        return f"Schema '{schema_name}' saved. You can now create a new schema or use this one as a nested type."

    @classmethod
    def reset_fields(cls) -> str:
        """
        Resets the fields.\n
        ---
        ### Returns
        - `str`: the status of the operation.
        """
        _logger.debug("Resetting fields...")
        cls.fields.clear()
        _logger.debug("Fields reset.")
        return "All fields cleared."

    @classmethod
    def import_schema_json(
            cls,
            json_data: str
        ) -> str:
        """
        Imports a schema from a JSON string.\n
        ---
        ### Args
        - `json_data` (`str`): the JSON string of the schema.\n
        ---
        ### Returns
        - `str`: the status of the operation.
        """
        _logger.debug("Importing schema from JSON...")
        try:
            data = json.loads(json_data)
            # Convert the JSON schema to a Belso schema
            schema: Schema = SchemaProcessor.load(data)

            # Extract fields from the schema
            cls.fields.clear()
            for field in schema.fields:
                field: DynamicField = field
                field_data = {
                    "name": field.name,
                    "description": field.description,
                    "required": field.required
                }

                # Handle different field types
                if isinstance(field, NestedField):
                    field_data["type_"] = "nested"
                    # We need to recursively import nested schemas
                    nested_name = field.schema.__name__
                    cls.schemas[nested_name] = field.schema
                    field_data["nested_schema"] = nested_name
                elif isinstance(field, ArrayField):
                    field_data["type_"] = "array"
                    if hasattr(field.items_type, "__name__"):
                        field_data["items_type"] = field.items_type.__name__
                    else:
                        field_data["items_type"] = "str"
                    if hasattr(field, "items_range") and field.items_range:
                        field_data["items_range"] = field.items_range
                else:
                    field_data["type_"] = field.type_.__name__ if hasattr(field.type_, "__name__") else "str"

                # Add validation parameters
                if hasattr(field, "enum") and field.enum:
                    field_data["enum"] = field.enum
                if hasattr(field, "regex") and field.regex:
                    field_data["regex"] = field.regex
                if hasattr(field, "range_") and field.range_:
                    field_data["range_"] = field.range_
                if hasattr(field, "multiple_of") and field.multiple_of:
                    field_data["multiple_of"] = field.multiple_of
                if hasattr(field, "length_range") and field.length_range:
                    field_data["length_range"] = field.length_range

                cls.fields.append(DynamicField(**field_data))

            _logger.debug("Schema imported.")
            return f"Schema imported with {len(cls.fields)} fields."
        except Exception as e:
            _logger.error(f"Error importing schema: {str(e)}")
            return f"Error importing schema: {str(e)}"

    @classmethod
    def get_available_schemas(cls) -> List[str]:
        """
        Gets the available schemas.\n
        ---
        ### Returns
        - `List[str]`: the list of available schemas.
        """
        _logger.debug("Getting available schemas...")
        return list(cls.schemas.keys())

    @classmethod
    def run(cls):
        """
        Runs the Belso Schema Generator.
        """
        _logger.debug("Running Belso Schema Generator...")
        with gr.Blocks(title="Belso Schema Generator") as demo:
            gr.Markdown("# 🏗️ Belso Schema Generator")

            with gr.Tabs() as tabs:
                with gr.TabItem("Schema Builder"):
                    with gr.Row():
                        schema_name = gr.Text(label="Schema Name", placeholder="MySchema")
                        schema_selector = gr.Dropdown(
                            choices=cls.get_available_schemas(),
                            label="Available Schemas",
                            interactive=True
                        )

                    with gr.Accordion("Field Definition", open=True):
                        with gr.Row():
                            name = gr.Text(label="Field Name")
                            type_selector = gr.Dropdown(
                                choices=list(_FILE_TYPE_MAP.keys()) + ["nested", "array"],
                                label="Field Type",
                                value="str"
                            )
                            required = gr.Checkbox(label="Required", value=True)

                        with gr.Row():
                            description = gr.Text(label="Description")

                        # Conditional UI elements for different field types
                        primitive_settings = gr.Column(visible=True)
                        nested_settings = gr.Column(visible=False)
                        array_settings = gr.Column(visible=False)

                        with primitive_settings:
                            with gr.Accordion("Validation Parameters", open=False):
                                with gr.Row():
                                    enum = gr.Text(label="Enum (comma-separated)")
                                    regex = gr.Text(label="Regex (only for str)")

                                with gr.Row():
                                    range_min = gr.Number(label="Min Value")
                                    range_max = gr.Number(label="Max Value")

                                with gr.Row():
                                    multiple_of = gr.Number(label="Multiple Of (float only)")

                                with gr.Row():
                                    length_min = gr.Number(label="Min Length (str only)")
                                    length_max = gr.Number(label="Max Length (str only)")

                        with nested_settings:
                            nested_schema_selector = gr.Dropdown(
                                choices=cls.get_available_schemas(),
                                label="Select Schema",
                                interactive=True
                            )

                        with array_settings:
                            with gr.Row():
                                items_type_selector = gr.Dropdown(
                                    choices=list(_FILE_TYPE_MAP.keys()) + cls.get_available_schemas(),
                                    label="Items Type",
                                    value="str"
                                )

                            with gr.Row():
                                items_min = gr.Number(label="Min Items")
                                items_max = gr.Number(label="Max Items")

                    with gr.Row():
                        add_button = gr.Button("Add Field")
                        reset_button = gr.Button("Reset Fields")

                    status = gr.Textbox(label="Status")

                    with gr.Row():
                        save_schema_button = gr.Button("Save Schema")
                        render_button = gr.Button("Preview Schema")

                    with gr.Accordion("Schema Preview", open=True):
                        format_selector = gr.Dropdown(
                            choices=[
                                FORMATS.JSON,
                                FORMATS.OPENAI,
                                FORMATS.GOOGLE,
                                FORMATS.OLLAMA,
                                FORMATS.ANTHROPIC,
                                FORMATS.MISTRAL,
                                FORMATS.LANGCHAIN
                            ],
                            label="Format",
                            value=FORMATS.JSON
                        )
                        preview = gr.Code(label="Preview", language="json")

                with gr.TabItem("Import/Export"):
                    with gr.Row():
                        import_json = gr.Textbox(label="Import JSON Schema", lines=10)
                        import_button = gr.Button("Import")

                    import_status = gr.Textbox(label="Import Status")

                    with gr.Row():
                        export_format = gr.Dropdown(
                            choices=[
                                FORMATS.JSON,
                                FORMATS.OPENAI,
                                FORMATS.GOOGLE,
                                FORMATS.OLLAMA,
                                FORMATS.ANTHROPIC,
                                FORMATS.MISTRAL,
                                FORMATS.LANGCHAIN
                            ],
                            label="Export Format",
                            value=FORMATS.JSON
                        )
                        export_schema_name = gr.Dropdown(
                            choices=cls.get_available_schemas(),
                            label="Schema to Export"
                        )
                        export_button = gr.Button("Export")

                    export_result = gr.Code(label="Export Result", language="json")

            # Define UI interactions
            def toggle_field_settings(field_type):
                return [
                    gr.update(visible=field_type not in ["nested", "array"]),  # primitive
                    gr.update(visible=field_type == "nested"),  # nested
                    gr.update(visible=field_type == "array")  # array
                ]

            type_selector.change(
                fn=toggle_field_settings,
                inputs=type_selector,
                outputs=[primitive_settings, nested_settings, array_settings]
            )

            # Update available schemas dropdown when a new schema is saved
            def update_schema_dropdowns():
                schemas = cls.get_available_schemas()
                return [
                    gr.update(choices=schemas),
                    gr.update(choices=schemas),
                    gr.update(choices=list(_FILE_TYPE_MAP.keys()) + schemas),
                    gr.update(choices=schemas)
                ]

            # Add field button
            add_button.click(
                fn=cls.add_field,
                inputs=[
                    name,
                    type_selector,
                    description,
                    required,
                    enum,
                    regex,
                    range_min,
                    range_max,
                    multiple_of,
                    length_min,
                    length_max,
                    items_min,
                    items_max,
                    nested_schema_selector,
                    items_type_selector
                ],
                outputs=status
            )

            # Reset fields button
            reset_button.click(fn=cls.reset_fields, outputs=status)

            # Save schema button
            save_schema_button.click(
                fn=cls.save_schema,
                inputs=schema_name,
                outputs=status
            ).then(
                fn=update_schema_dropdowns,
                outputs=[
                    schema_selector,
                    nested_schema_selector,
                    items_type_selector,
                    export_schema_name
                ]
            )

            # Render schema button
            render_button.click(
                fn=cls.render_schema,
                inputs=[schema_name, format_selector],
                outputs=preview
            )

            # Import schema button
            import_button.click(
                fn=cls.import_schema_json,
                inputs=import_json,
                outputs=import_status
            ).then(
                fn=update_schema_dropdowns,
                outputs=[
                    schema_selector,
                    nested_schema_selector,
                    items_type_selector,
                    export_schema_name
                ]
            )

            # Export schema button
            def export_schema(format_type, schema_name):
                _logger.debug(f"Exporting schema \"{schema_name}\" in format \"{format_type}\"...")
                if schema_name not in cls.schemas:
                    _logger.warning(f"Schema \"{schema_name}\" not found.")
                    return "Schema not found"

                schema = cls.schemas[schema_name]
                try:
                    result = SchemaProcessor.convert(schema, to=format_type)
                    _logger.debug(f"Schema \"{schema_name}\" exported.")
                    return json.dumps(result, indent=2)
                except Exception as e:
                    _logger.error(f"Error exporting schema: {str(e)}")
                    return f"Error exporting schema: {str(e)}"

            export_button.click(
                fn=export_schema,
                inputs=[export_format, export_schema_name],
                outputs=export_result
            )
        demo.launch()
