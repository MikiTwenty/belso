from belso.utils import FORMATS
from belso import Schema, Field, SchemaProcessor

class Light(Schema):
    fields = [
        Field("is_on", type=bool, description="Whether the light should be on or off"),
        Field("brightness", type=int, description="Brightness of the light, from 0 to 100 - 0 if light is off"),
        Field(
            "temperature",
            type=str,
            enum=['warm', 'neutral', 'cold'],  # Predefined output values
            description="The temperature of the light, from warm to cold"
        ),
    ]

class Room(Schema):
    fields = [Field("Light", type=Light, description="The light in the room")]

class House(Schema):
    fields = [
        Field("Kitchen", type=Room, description="The kitchen in the house"),
        Field("Bedroom", type=Room, description="The bedroom in the house"),
        Field("Bathroom", type=Light, description="The bathroom in the house"),
    ]

def main():
    # Display the schema
    SchemaProcessor.display(House)

    # Convert the schema to multiple formats
    schema = SchemaProcessor.convert(House, to=FORMATS.OLLAMA)
    schema = SchemaProcessor.convert(schema, to=FORMATS.OPENAI)
    schema = SchemaProcessor.convert(schema, to=FORMATS.GOOGLE)
    schema = SchemaProcessor.convert(schema, to=FORMATS.ANTHROPIC)
    schema = SchemaProcessor.convert(schema, to=FORMATS.HUGGINGFACE)
    schema = SchemaProcessor.convert(schema, to=FORMATS.LANGCHAIN)
    schema = SchemaProcessor.convert(schema, to=FORMATS.MISTRAL)
    schema = SchemaProcessor.convert(schema, to=FORMATS.JSON)

    # Save and load the schema using different formats
    SchemaProcessor.save(schema, path="./examples/schemas/nested_schema.json")
    schema = SchemaProcessor.load(path="./examples/schemas/nested_schema.json")
    schema = SchemaProcessor.convert(schema, to=FORMATS.XML)
    SchemaProcessor.save(schema, path="./examples/schemas/nested_schema.xml")
    schema = SchemaProcessor.load(path="./examples/schemas/nested_schema.xml")
    schema = SchemaProcessor.convert(schema, to=FORMATS.YAML)
    SchemaProcessor.save(schema, path="./examples/schemas/nested_schema.yaml")
    schema = SchemaProcessor.load(path="./examples/schemas/nested_schema.yaml")

    # Standardize the schema
    schema = SchemaProcessor.standardize(schema)

    # Display the standardized schema to check the consistency with the original schema
    SchemaProcessor.display(schema)

if __name__ == "__main__":
    main()
