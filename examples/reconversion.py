from belso.utils import FORMATS
from belso import Schema, Field, SchemaProcessor

class CustomSchema(Schema):
    fields = [Field("value", type=bool, description="Random boolean value")]

def main():
    # Display the schema
    SchemaProcessor.display(CustomSchema)

    # Convert the schema to multiple formats
    schema = SchemaProcessor.convert(CustomSchema, to=FORMATS.OLLAMA)
    schema = SchemaProcessor.convert(schema, to=FORMATS.OPENAI)
    schema = SchemaProcessor.convert(schema, to=FORMATS.GOOGLE)
    schema = SchemaProcessor.convert(schema, to=FORMATS.ANTHROPIC)
    schema = SchemaProcessor.convert(schema, to=FORMATS.HUGGINGFACE)
    schema = SchemaProcessor.convert(schema, to=FORMATS.LANGCHAIN)
    schema = SchemaProcessor.convert(schema, to=FORMATS.MISTRAL)

    # Save and load the schema using different formats
    SchemaProcessor.save(schema, "./examples/schemas/simple_schema.json")
    schema = SchemaProcessor.load("./examples/schemas/simple_schema.json")
    SchemaProcessor.save(schema, "./examples/schemas/simple_schema.xml")
    schema = SchemaProcessor.load("./examples/schemas/simple_schema.xml")
    SchemaProcessor.save(schema, "./examples/schemas/simple_schema.yaml")
    schema = SchemaProcessor.load("./examples/schemas/simple_schema.yaml")

    # Standardize the schema
    schema = SchemaProcessor.standardize(schema)

    # Display the standardized schema to check the consistency with the original schema
    SchemaProcessor.display(schema)

if __name__ == "__main__":
    main()
