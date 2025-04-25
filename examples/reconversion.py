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
SchemaProcessor.display(CustomSchema)

ollama_schema = SchemaProcessor.translate(CustomSchema, to=PROVIDERS.OLLAMA)
openai_schema = SchemaProcessor.translate(ollama_schema, to=PROVIDERS.OPENAI)
belso_schema = SchemaProcessor.standardize(openai_schema)

SchemaProcessor.display(CustomSchema)

