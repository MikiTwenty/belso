from belso.utils import FORMATS
from belso import Schema, Field, SchemaProcessor

class CustomSchema(Schema):
    fields = [
        Field(
            name="value",
            type=bool,
            description="Random boolean value",
            required=True
        )
    ]
SchemaProcessor.display(CustomSchema)

schema = SchemaProcessor.translate(CustomSchema, to=FORMATS.OLLAMA)
schema = SchemaProcessor.translate(schema, to=FORMATS.OPENAI)
schema = SchemaProcessor.translate(schema, to=FORMATS.GOOGLE)
schema = SchemaProcessor.translate(schema, to=FORMATS.ANTHROPIC)
schema = SchemaProcessor.translate(schema, to=FORMATS.HUGGINGFACE)
schema = SchemaProcessor.translate(schema, to=FORMATS.LANGCHAIN)
schema = SchemaProcessor.translate(schema, to=FORMATS.MISTRAL)
SchemaProcessor.save(schema, "./examples/schemas/simple_schema.json")
schema = SchemaProcessor.load("./examples/schemas/simple_schema.json")
SchemaProcessor.save(schema, "./examples/schemas/simple_schema.xml")
schema = SchemaProcessor.load("./examples/schemas/simple_schema.xml")
SchemaProcessor.save(schema, "./examples/schemas/simple_schema.yaml")
schema = SchemaProcessor.load("./examples/schemas/simple_schema.yaml")
schema = SchemaProcessor.standardize(schema)

SchemaProcessor.display(schema)
