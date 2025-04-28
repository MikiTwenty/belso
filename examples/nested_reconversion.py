from belso.utils import FORMATS
from belso import Schema, Field, SchemaProcessor

class LightSchema(Schema):
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
            type_=LightSchema,
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
SchemaProcessor.to_json(schema, "./examples/nested_schema.json")
schema = SchemaProcessor.from_json("./examples/nested_schema.json")
SchemaProcessor.to_xml(schema, "./examples/nested_schema.xml")
schema = SchemaProcessor.from_xml("./examples/nested_schema.xml")
schema = SchemaProcessor.standardize(schema)

SchemaProcessor.display(schema)
