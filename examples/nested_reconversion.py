from belso.utils import FORMATS
from belso import Schema, Field, SchemaProcessor

class Light(Schema):
    fields = [
        Field(
            name="is_on",
            type_=bool,
            description="Whether the light should be on or off",
            required=True
        ),
        Field(
            name="brightness",
            type_=int,
            description="Brightness of the light, from 0 to 100 - 0 if light is off",
            required=True
        ),
        Field(
            name="temperature",
            type_=str,
            enum=['warm', 'neutral', 'cold'],
            description="The temperature of the light, from warm to cold",
            required=True
        ),
    ]

class Room(Schema):
    fields = [
        Field(
            name="Light",
            type_=Light,
            description="The light in the room",
            required=True
        )
    ]

class House(Schema):
    fields = [
        Field(
            name="Kitchen",
            type_=Room,
            description="The kitchen in the house",
            required=True
        ),
        Field(
            name="Bedroom",
            type_=Room,
            description="The bedroom in the house",
            required=True
        ),
        Field(
            name="Bathroom",
            type_=Room,
            description="The bathroom in the house",
            required=True
        ),
    ]

SchemaProcessor.display(House)

schema = SchemaProcessor.translate(House, to=FORMATS.OLLAMA)
schema = SchemaProcessor.translate(schema, to=FORMATS.OPENAI)
schema = SchemaProcessor.translate(schema, to=FORMATS.GOOGLE)
schema = SchemaProcessor.translate(schema, to=FORMATS.ANTHROPIC)
schema = SchemaProcessor.translate(schema, to=FORMATS.HUGGINGFACE)
schema = SchemaProcessor.translate(schema, to=FORMATS.LANGCHAIN)
schema = SchemaProcessor.translate(schema, to=FORMATS.MISTRAL)
schema = SchemaProcessor.translate(schema, to=FORMATS.JSON)
SchemaProcessor.save(schema, path="./examples/nested_schema.json")
schema = SchemaProcessor.load(path="./examples/nested_schema.json")
schema = SchemaProcessor.translate(schema, to=FORMATS.XML)
SchemaProcessor.save(schema, path="./examples/nested_schema.xml")
schema = SchemaProcessor.load(path="./examples/nested_schema.xml")
schema = SchemaProcessor.translate(schema, to=FORMATS.YAML)
SchemaProcessor.save(schema, path="./examples/nested_schema.yaml")
schema = SchemaProcessor.load(path="./examples/nested_schema.yaml")
schema = SchemaProcessor.standardize(schema)

SchemaProcessor.display(schema)
