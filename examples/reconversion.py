from belso.utils import FORMATS
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

schema = SchemaProcessor.translate(CustomSchema, to=FORMATS.OLLAMA)
schema = SchemaProcessor.translate(schema, to=FORMATS.OPENAI)
schema = SchemaProcessor.translate(schema, to=FORMATS.GOOGLE)
schema = SchemaProcessor.translate(schema, to=FORMATS.ANTHROPIC)
schema = SchemaProcessor.translate(schema, to=FORMATS.HUGGINGFACE)
schema = SchemaProcessor.translate(schema, to=FORMATS.LANGCHAIN)
schema = SchemaProcessor.translate(schema, to=FORMATS.MISTRAL)
SchemaProcessor.to_json(schema, "./examples/schema.json")
schema = SchemaProcessor.from_json("./examples/schema.json")
SchemaProcessor.to_xml(schema, "./examples/schema.xml")
schema = SchemaProcessor.from_xml("./examples/schema.xml")
SchemaProcessor.to_yaml(schema, "./examples/schema.yaml")
schema = SchemaProcessor.from_yaml("./examples/schema.yaml")
schema = SchemaProcessor.standardize(schema)

SchemaProcessor.display(schema)
