# belso.gui.layout

"""
Layout builder for Belso GUI.
---
Defines the structural layout of the app using Gradio Blocks,
and provides handles to the main component sections.
"""

import gradio as gr

def build_layout() -> dict:
    """
    Builds the UI layout using Gradio components.\n
    ---
    ### Returns
    - `dict`: dictionary containing references to major layout sections.
    """
    with gr.Blocks(title="Belso Schema Builder") as app:
        gr.Markdown("# 🧠 Belso Schema Builder")

        # BREADCRUMB + SCHEMA ACTION BAR
        with gr.Row():
            breadcrumb = gr.Markdown("📂 Root", elem_id="breadcrumb_bar")
            refresh_button = gr.Button("🔄 Refresh", size="sm")

        # SCHEMA & FIELD SELECTION ZONE
        with gr.Row():
            with gr.Column(scale=1):
                schema_dropdown = gr.Dropdown(
                    label="Schema corrente",
                    choices=[],
                    interactive=True
                )
                new_schema_name = gr.Textbox(label="Nuovo schema")
                create_schema_btn = gr.Button("➕ Crea schema")

            with gr.Column(scale=2):
                field_table = gr.Dataframe(
                    headers=["Nome", "Tipo", "Obbligatorio", "Descrizione", "Schema Ref"],
                    datatype=["str"] * 5,
                    label="Campi dello schema",
                    interactive=False,
                    row_count=(5, "dynamic"),
                    col_count=(5, "fixed")
                )

        # FIELD EDITOR (accordion dinamico)
        with gr.Accordion("➕ Aggiungi campo", open=False):
            field_name = gr.Textbox(label="Nome campo")
            field_type = gr.Dropdown(
                label="Tipo",
                choices=["str", "int", "float", "bool", "nested", "array"],
                value="str"
            )
            field_desc = gr.Textbox(label="Descrizione")
            field_required = gr.Checkbox(label="Obbligatorio", value=True)

            # VALIDATION
            with gr.Accordion("Opzioni di validazione", open=False):
                field_enum = gr.Textbox(label="Valori ammessi (enum, separati da virgola)")
                field_regex = gr.Textbox(label="Espressione regolare")
                field_range_min = gr.Number(label="Minimo")
                field_range_max = gr.Number(label="Massimo")
                field_multiple_of = gr.Number(label="Multiplo di")
                field_length_min = gr.Number(label="Lunghezza minima", precision=0)
                field_length_max = gr.Number(label="Lunghezza massima", precision=0)

            # ARRAY/NESTED OPTIONS
            with gr.Accordion("Array/Nested", open=False, visible=False) as array_nested_options:
                nested_schema_dropdown = gr.Dropdown(label="Schema annidato", choices=[])
                array_type_dropdown = gr.Dropdown(label="Tipo elementi", choices=[])
                items_min = gr.Number(label="Min elementi", precision=0)
                items_max = gr.Number(label="Max elementi", precision=0)

            add_field_btn = gr.Button("✅ Aggiungi campo")
            field_status = gr.Textbox(label="Esito", interactive=False)

        # EXPORT / IMPORT
        with gr.Row():
            export_btn = gr.Button("⬇️ Esporta schema")
            import_btn = gr.Button("⬆️ Importa schema")
            format_dropdown = gr.Dropdown(
                label="Formato",
                choices=["json", "openai", "google", "ollama", "anthropic", "mistral", "langchain", "huggingface"],
                value="json"
            )

        schema_output = gr.Code(label="Schema generato", language="json")
        schema_import = gr.Code(label="Schema da importare", language="json")
        import_status = gr.Textbox(label="Esito import", interactive=False)

        return app, {
            # Layout handles
            "breadcrumb": breadcrumb,
            "refresh_btn": refresh_button,
            "schema_dropdown": schema_dropdown,
            "new_schema_input": new_schema_name,
            "create_schema_btn": create_schema_btn,
            "field_table": field_table,
            "field_name": field_name,
            "field_type": field_type,
            "field_desc": field_desc,
            "field_required": field_required,
            "field_enum": field_enum,
            "field_regex": field_regex,
            "field_range_min": field_range_min,
            "field_range_max": field_range_max,
            "field_multiple_of": field_multiple_of,
            "field_length_min": field_length_min,
            "field_length_max": field_length_max,
            "array_nested_options": array_nested_options,
            "nested_schema_dropdown": nested_schema_dropdown,
            "array_type_dropdown": array_type_dropdown,
            "items_min": items_min,
            "items_max": items_max,
            "add_field_btn": add_field_btn,
            "field_status": field_status,
            "export_btn": export_btn,
            "import_btn": import_btn,
            "format_dropdown": format_dropdown,
            "schema_output": schema_output,
            "schema_import": schema_import,
            "import_status": import_status,
        }
