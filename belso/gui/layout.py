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
    Build the Belso Schema Editor interface.
    ---
    ### Args
    - `initial_state` (`GUIState`): the initial state of the application.
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
                                inputs=[current_state, name_edit_textbox], # Pass current_state and the textbox component's value
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
                                # Opzioni per stringhe
                                with gr.Group(visible=field_data["type"] == "str") as str_options:
                                    length_range = gr.Textbox(
                                        label="Lenght Range (min,max)",
                                        value=str(field_data.get("length_range", ""))
                                    )
                                    regex = gr.Textbox(label="Regex", value=field_data.get("regex", ""))
                                    format_ = gr.Textbox(label="Format", value=field_data.get("format_", ""))

                                # Opzioni per numeri (int e float)
                                with gr.Group(visible=field_data["type"] in ["int", "float"]) as num_options:
                                    range_ = gr.Textbox(
                                        label="Range (min,max)",
                                        value=str(field_data.get("range_", ""))
                                    )
                                    exclusive_range = gr.Textbox(
                                        label="Exclusive Range (min,max)",
                                        value=str(field_data.get("exclusive_range", ""))
                                    )
                                    multiple_of = gr.Number(
                                        label="Multiple of",
                                        value=field_data.get("multiple_of", None)
                                    )

                                # Opzioni per liste
                                with gr.Group(visible=field_data["type"] == "list") as list_options:
                                    items_range = gr.Textbox(
                                        label="Items Range (min,max)",
                                        value=str(field_data.get("items_range", ""))
                                    )

                                # Opzioni per oggetti/dizionari
                                with gr.Group(visible=field_data["type"] == "dict") as dict_options:
                                    properties_range = gr.Textbox(
                                        label="Properties Range (min,max)",
                                        value=str(field_data.get("properties_range", ""))
                                    )

                                # Opzione enum comune a tutti i tipi
                                enum = gr.Textbox(
                                    label="Enum (comma separated)",
                                    value=str(field_data.get("enum", ""))
                                )

                            # Aggiorna la visibilità e i valori delle opzioni quando cambia il tipo
                            type_.change(
                                fn=handle_type_change,
                                inputs=[
                                    type_,
                                    length_range, regex, format_,
                                    range_, exclusive_range, multiple_of,
                                    items_range, properties_range
                                ],
                                outputs=[
                                    str_options, num_options, list_options, dict_options,
                                    length_range, regex, format_,
                                    range_, exclusive_range, multiple_of,
                                    items_range, properties_range
                                ]
                            )

                            # Raccogli tutti i campi di input per passarli alla funzione di salvataggio
                            all_inputs = [
                                name, type_, desc, req, default, current_state,
                                length_range, regex, format_,
                                range_, exclusive_range, multiple_of,
                                items_range, properties_range, enum
                            ]

                            gr.Button("💾 Save Field", scale=1).click(
                                fn=handle_add_field,
                                inputs=all_inputs,
                                outputs=[current_state]
                            )

    logger.info("GUI interface built.")
    return app
