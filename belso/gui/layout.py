# belso.gui.layout

import logging

import gradio as gr

from belso.gui.state import GUIState
from belso.gui.events import handle_add_schema, handle_add_field
from belso.gui.components.schema_tree import render_schema_tree

logger = logging.getLogger(__name__)

def build_interface(state: GUIState) -> gr.Blocks:
    """
    Builds the GUI layout for Belso Schema Editor.
    """
    with gr.Blocks() as app:
        gr.Markdown("## 🧬 Belso Schema Editor")

        state_var = gr.State(value=state)
        schema_output = gr.Column()

        def render_schemas(gui_state: GUIState):
            """
            Internal helper to render tabs and fields.
            This must run inside a gradio context.
            """
            with schema_output:
                if not gui_state.schemas:
                    gr.Markdown("⚠️ Nessuno schema ancora creato.")
                    return

                with gr.Tabs():
                    for name, schema in gui_state.schemas.items():
                        with gr.Tab(label=name):
                            gr.Markdown(f"### ✨ {name}")
                            render_schema_tree(schema, gui_state)
                            with gr.Row():
                                add_btn = gr.Button("➕ Campo")
                                add_btn.click(
                                    fn=lambda s: (handle_add_field(s, name), s)[1],
                                    inputs=[state_var],
                                    outputs=[state_var],
                                )

        def on_add_schema(gui_state: GUIState):
            handle_add_schema(gui_state)
            return gui_state

        # Pulsante per aggiungere uno schema
        gr.Button("➕ Nuovo Schema").click(
            fn=on_add_schema,
            inputs=[state_var],
            outputs=[state_var],
        )

        # Rendering iniziale
        render_schemas(state)

    return app
