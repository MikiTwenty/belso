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

schema = SchemaProcessor.translate(CustomSchema, to=PROVIDERS.OLLAMA)
schema = SchemaProcessor.translate(schema, to=PROVIDERS.OPENAI)
schema = SchemaProcessor.translate(schema, to=PROVIDERS.GOOGLE)
schema = SchemaProcessor.translate(schema, to=PROVIDERS.ANTHROPIC)
schema = SchemaProcessor.translate(schema, to=PROVIDERS.HUGGINGFACE)
schema = SchemaProcessor.translate(schema, to=PROVIDERS.LANGCHAIN)
schema = SchemaProcessor.translate(schema, to=PROVIDERS.MISTRAL)
schema = SchemaProcessor.standardize(schema)

SchemaProcessor.display(schema)
