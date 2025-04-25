import json

from belso.utils import PROVIDERS
from belso import Schema, Field, SchemaProcessor

class CustomSchema(Schema):
    fields = [
        Field(
            name="value",
            type_=bool,
            description="Random boolean value",
            required=True
        )
    ]

ollama_schema = SchemaProcessor.translate(CustomSchema, to=PROVIDERS.OLLAMA)
SchemaProcessor.display(ollama_schema)
