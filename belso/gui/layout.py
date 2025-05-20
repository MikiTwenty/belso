# belso.gui.layout

import gradio as gr

from belso.gui.state import GUIState
from belso.gui.components.schema_tree import render_schema_tree
from belso.gui.handlers import handle_add_schema, handle_add_field
from belso.gui.components.field_editor import open_field_editor_data

def build_interface(initial_state: GUIState) -> gr.Blocks:
    """
    Costruisce l'interfaccia utente per il Belso Schema Editor.
    """
    with gr.Blocks() as app:
        gr.Markdown("## 🧬 Belso Schema Editor")

        current_state = gr.State(value=initial_state)

        gr.Button("➕ Nuovo Schema").click(
            fn=handle_add_schema,
            inputs=[current_state],
            outputs=[current_state],
        )

        @gr.render(inputs=[current_state])
        def render(gui_state: GUIState):
            if not gui_state.schemas:
                gr.Markdown("⚠️ Nessuno schema ancora creato.")
                return

            with gr.Tabs():
                for name, schema in gui_state.schemas.items():
                    with gr.Tab(label=name):
                        gr.Markdown(f"### ✨ {name}")
                        render_schema_tree(schema, current_state, gui_state)

            with gr.Column(visible=True):
                field_data = open_field_editor_data()
                name = gr.Textbox(label="Nome", value=field_data["name"])
                type_ = gr.Dropdown(choices=["str", "int", "float", "bool"], label="Tipo", value=field_data["type"])
                desc = gr.Textbox(label="Descrizione", value=field_data["description"])
                req = gr.Checkbox(label="Obbligatorio", value=field_data["required"])
                default = gr.Textbox(label="Default", value=field_data["default"])

                gr.Button("💾 Salva campo").click(
                    fn=handle_add_field,
                    inputs=[name, type_, desc, req, default, current_state],
                    outputs=[current_state]
                )

    return app
