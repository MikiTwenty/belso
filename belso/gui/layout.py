# belso.gui.layout

import logging

import gradio as gr

from belso.gui.state import GUIState
from belso.gui.components.schema_tree import render_schema_tree
from belso.gui.handlers import handle_add_schema, handle_add_field
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

        current_state = gr.State(value=initial_state)

        gr.Button("➕ Nuovo Schema", scale=1).click(
            fn=handle_add_schema,
            inputs=[current_state],
            outputs=[current_state],
        )

        @gr.render(inputs=[current_state])
        def render(gui_state: GUIState):
            """
            Render the schema tree for the current state.
            ---
            ### Args
            - `gui_state` (`GUIState`): the current state of the application.
            ---
            ### Returns
            - `None`: no return value.
            """
            if not gui_state.schemas:
                logger.warning("No schemas found in state.")
                gr.Markdown("⚠️ Nessuno schema ancora creato.")
                return

            with gr.Tabs():
                for name, schema in gui_state.schemas.items():
                    with gr.Tab(label=name):
                        with gr.Row():
                            name_edit = gr.Textbox(label="Nome schema", value=name, scale=3)
                            gr.Button("🗑️", size="sm").click(
                                fn=lambda s, n=name: s.delete_schema(n) or s.clone(),
                                inputs=[current_state],
                                outputs=[current_state]
                            )

                        render_schema_tree(schema, current_state, gui_state)

                        label = "✏️ Modifica Campo" if gui_state.selected_field else "➕ Aggiungi Campo"
                        open_by_default = gui_state.selected_field is not None

                        with gr.Accordion(label, open=open_by_default):
                            field_data = open_field_editor_data(gui_state.selected_field)
                            name = gr.Textbox(label="Nome", value=field_data["name"])
                            type_ = gr.Dropdown(choices=["str", "int", "float", "bool"], label="Tipo", value=field_data["type"])
                            desc = gr.Textbox(label="Descrizione", value=field_data["description"])
                            req = gr.Checkbox(label="Obbligatorio", value=field_data["required"])
                            default = gr.Textbox(label="Default", value=field_data["default"])

                            gr.Button("💾 Salva campo", scale=1).click(
                                fn=handle_add_field,
                                inputs=[name, type_, desc, req, default, current_state],
                                outputs=[current_state]
                            )

    logger.info("GUI interface built.")
    return app
