# belso.gui.app

"""
Belso GUI Application Entrypoint
---
Initializes the Gradio app, connects UI layout to logic handlers.
"""

import gradio as gr

from belso.gui.logic import handlers
from belso.gui.layout import build_layout
from belso.gui.components.schema_toolbar import refresh_breadcrumb

def run():
    """
    Launches the Belso Schema Builder UI.
    """
    with gr.Blocks(title="Belso Schema Builder") as app:
        app_instance, el = build_layout()

        # Event bindings (tutti qui dentro)
        el["create_schema_btn"].click(
            fn=handlers.on_create_schema,
            inputs=[el["new_schema_input"]],
            outputs=[el["schema_dropdown"], el["breadcrumb"]]
        )
        el["schema_dropdown"].change(
            fn=handlers.on_schema_change,
            inputs=[el["schema_dropdown"]],
            outputs=[el["field_table"]]
        )
        el["add_field_btn"].click(
            fn=handlers.on_add_field,
            inputs=[
                el["field_name"], el["field_type"], el["field_desc"], el["field_required"],
                el["field_enum"], el["field_regex"], el["field_range_min"], el["field_range_max"],
                el["field_multiple_of"], el["field_length_min"], el["field_length_max"],
                el["items_min"], el["items_max"], el["nested_schema_dropdown"], el["array_type_dropdown"]
            ],
            outputs=[el["field_status"], el["field_table"]]
        )
        el["export_btn"].click(
            fn=handlers.on_export_schema,
            inputs=[el["schema_dropdown"], el["format_dropdown"]],
            outputs=[el["schema_output"]]
        )
        el["import_btn"].click(
            fn=handlers.on_import_schema,
            inputs=[el["schema_import"]],
            outputs=[el["import_status"]]
        ).then(
            fn=refresh_breadcrumb,
            inputs=[],
            outputs=[el["breadcrumb"]]
        )

    app.launch()
