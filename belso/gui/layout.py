# belso.gui.layout

import logging

import gradio as gr

from belso.gui.state import GUIState
from belso.gui.components.schema_tree import render_schema_tree
from belso.gui.handlers import (
    handle_add_schema,
    handle_add_field,
    handle_rename_schema,
    handle_type_change
)
from belso.gui.components.field_editor import open_field_editor_data

logger = logging.getLogger(__name__)

def build_interface(initial_state: GUIState) -> gr.Blocks:
    """
    Build the Belso Schema Editor interface.\n
    ---
    ### Args
    - `initial_state` (`GUIState`): the initial state of the application.\n
    ---
    ### Returns
    - `gr.Blocks`:  the Gradio application.
    """
    logger.info("Building GUI interface...")
    with gr.Blocks() as app:
        gr.Markdown("## 🧬 Belso Schema Editor")

        # Current state of the application
        current_state = gr.State(value=initial_state)

        # Buttons for schema operations
        gr.Button("➕ Nuovo Schema", size="sm").click(
            fn=handle_add_schema,
            inputs=[current_state],
            outputs=[current_state],
        )

        # Render the schema tree
        @gr.render(inputs=[current_state])
        def render(gui_state: GUIState) -> None:
            """
            Render the schema tree for the current state.\n
            ---
            ### Args
            - `gui_state` (`GUIState`): the current state of the application.
            """
            # If no schemas are found, display a warning message
            if not gui_state.schemas:
                logger.warning("No schemas found in state.")
                gr.Markdown("⚠️ Nessuno schema ancora creato.")
                return

            # Render the schema tree
            with gr.Tabs():
                for original_name, schema in gui_state.schemas.items(): # Use original_name for closure
                    with gr.Tab(label=original_name):
                        with gr.Row():
                            name_edit_textbox = gr.Textbox(label="Schame Name", value=original_name, scale=3, elem_id=f"schema-name-edit-{original_name}")
                            gr.Button("✏️ Rename Schema", size="sm", elem_id=f"save-schema-name-{original_name}").click(
                                fn=lambda state_val, new_name_val, captured_old_name=original_name: handle_rename_schema(state_val, captured_old_name, new_name_val),
                                inputs=[current_state, name_edit_textbox],
                                outputs=[current_state]
                            )
                            gr.Button("🗑️ Delete Schema", size="sm", elem_id=f"delete-schema-{original_name}").click(
                                fn=lambda s, n=original_name: s.delete_schema(n) or s.clone(),
                                inputs=[current_state],
                                outputs=[current_state]
                            )

                        render_schema_tree(schema, current_state, gui_state)

                        label = "✏️ Modify Field" if gui_state.selected_field else "➕ New Field"
                        open_by_default = gui_state.selected_field is not None

                        with gr.Accordion(label, open=open_by_default):
                            field_data = open_field_editor_data(gui_state.selected_field)

                            # Basic fields
                            name = gr.Textbox(label="Name", value=field_data["name"])
                            type_ = gr.Dropdown(
                                choices=["str", "int", "float", "bool", "list", "dict"],
                                label="Tipo",
                                value=field_data["type"]
                            )
                            desc = gr.Textbox(label="Description", value=field_data["description"])
                            req = gr.Checkbox(label="Required", value=field_data["required"])
                            default = gr.Textbox(label="Default", value=field_data["default"])

                            # Contenitore per opzioni dinamiche
                            with gr.Accordion("Advanced Setting", open=False):
                                # String options
                                with gr.Group(visible=field_data["type"] == "str") as str_options:
                                    with gr.Row():
                                        length_min = gr.Textbox(
                                            label="Min Length",
                                            value=str(field_data.get("length_min", ""))
                                        )
                                        length_max = gr.Textbox(
                                            label="Max Length",
                                            value=str(field_data.get("length_max", ""))
                                        )
                                    regex = gr.Textbox(label="Regex", value=field_data.get("regex", ""))
                                    format_ = gr.Textbox(label="Format", value=field_data.get("format_", ""))

                                # Number options (int and float)
                                with gr.Group(visible=field_data["type"] in ["int", "float"]) as num_options:
                                    with gr.Row():
                                        range_min = gr.Textbox(
                                            label="Min Value",
                                            value=str(field_data.get("range_min", ""))
                                        )
                                        range_max = gr.Textbox(
                                            label="Max Value",
                                            value=str(field_data.get("range_max", ""))
                                        )
                                    with gr.Row():
                                        exclusive_min = gr.Textbox(
                                            label="Exclusive Min",
                                            value=str(field_data.get("exclusive_min", ""))
                                        )
                                        exclusive_max = gr.Textbox(
                                            label="Exclusive Max",
                                            value=str(field_data.get("exclusive_max", ""))
                                        )
                                    multiple_of = gr.Number(
                                        label="Multiple of",
                                        value=field_data.get("multiple_of", None)
                                    )

                                # List options
                                with gr.Group(visible=field_data["type"] == "list") as list_options:
                                    with gr.Row():
                                        items_min = gr.Textbox(
                                            label="Min Items",
                                            value=str(field_data.get("items_min", ""))
                                        )
                                        items_max = gr.Textbox(
                                            label="Max Items",
                                            value=str(field_data.get("items_max", ""))
                                        )

                                # Dictionary/object options
                                with gr.Group(visible=field_data["type"] == "dict") as dict_options:
                                    with gr.Row():
                                        properties_min = gr.Textbox(
                                            label="Min Properties",
                                            value=str(field_data.get("properties_min", ""))
                                        )
                                        properties_max = gr.Textbox(
                                            label="Max Properties",
                                            value=str(field_data.get("properties_max", ""))
                                        )

                                # Common option for all types
                                enum = gr.Textbox(
                                    label="Enum (comma separated)",
                                    value=str(field_data.get("enum", ""))
                                )

                            # Aggiorna la visibilità e i valori delle opzioni quando cambia il tipo
                            type_.change(
                                fn=handle_type_change,
                                inputs=[type_],
                                outputs=[
                                    str_options, num_options, list_options, dict_options,  # ✅ GRUPPI
                                    length_min, length_max, regex, format_,
                                    range_min, range_max, exclusive_min, exclusive_max, multiple_of,
                                    items_min, items_max, properties_min, properties_max
                                ]
                            )

                            # Raccogli tutti i campi di input per passarli alla funzione di salvataggio
                            all_inputs = [
                                name, type_, desc, req, default, current_state,
                                length_min, length_max, regex, format_,
                                range_min, range_max, exclusive_min, exclusive_max, multiple_of,
                                items_min, items_max, properties_min, properties_max, enum
                            ]

                            gr.Button("💾 Save Field", scale=1).click(
                                fn=handle_add_field,
                                inputs=all_inputs,
                                outputs=[current_state]
                            )

    logger.info("GUI interface built.")
    return app
