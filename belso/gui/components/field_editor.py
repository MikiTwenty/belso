# belso.gui.components.field_editor

from typing import Optional

import gradio as gr

from belso.gui.state import GUIState
from belso.core.schema import Schema
from belso.core.field import Field, BaseField
from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP


def open_field_editor(
        state: GUIState,
        schema: Schema,
        existing_field: Optional[BaseField] = None
    ) -> None:
    """
    Opens a field editor form (in a modal-like view).\n
    ---
    ### Args
    - `state` (`GUIState`): GUI state object.
    - `schema` (`Schema`): The schema the field belongs to.
    - `existing_field` (`Optional[BaseField]`): If editing, the current field.
    """
    with gr.Column(visible=True):
        gr.Markdown("### ✏️ Modifica Campo" if existing_field else "### ➕ Nuovo Campo")

        name_input = gr.Textbox(label="Nome", value=existing_field.name if existing_field else "")
        type_input = gr.Dropdown(
            choices=list(_FILE_TYPE_MAP.keys()),
            label="Tipo",
            value=existing_field.type_.__name__ if existing_field else "str"
        )
        desc_input = gr.Textbox(label="Descrizione", value=existing_field.description if existing_field else "")
        required_input = gr.Checkbox(label="Obbligatorio", value=existing_field.required if existing_field else True)
        default_input = gr.Textbox(label="Default", value=existing_field.default if existing_field else "")

        submit_btn = gr.Button("💾 Salva campo")
        cancel_btn = gr.Button("❌ Annulla")

        def save_field(name, type_str, description, required, default):
            try:
                py_type = _FILE_TYPE_MAP.get(type_str, str)
                new_field = Field(
                    name=name,
                    type=py_type,
                    description=description,
                    required=required,
                    default=default or None,
                )
                if existing_field:
                    schema.fields = [
                        new_field if f.name == existing_field.name else f
                        for f in schema.fields
                    ]
                else:
                    schema.fields.append(new_field)
            except Exception as e:
                print(f"[FieldEditor] Errore durante il salvataggio: {e}")

        submit_btn.click(
            save_field,
            inputs=[name_input, type_input, desc_input, required_input, default_input],
            outputs=[]
        )

        cancel_btn.click(
            lambda: None,
            outputs=[]
        )
