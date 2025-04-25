import json
import ollama

from belso.utils import PROVIDERS
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

def main():
    # Convert to Ollama format
    ollama_schema = SchemaProcessor.translate(House, to=PROVIDERS.OLLAMA)

    print("\nConverted schema to Ollama format:")
    print(json.dumps(ollama_schema, indent=4))

    try:
        # Define the prompt that asks to turn off the lights
        default_prompt = (
            "Turn on all the lights in all the room of the house,"
            " set the brightness at 50% and the temperature to warm."
        )
        print(f"\nDefault prompt:\n\"{default_prompt}\"")
        user_prompt = input(f"\n>> Type a prompt (press Enter to use default prompt): ")
        prompt = user_prompt or default_prompt

        # Make the actual request to Ollama with our schema
        response = ollama.chat(
            model="llama3.2:1b-instruct-fp16",  # You may need to change this to a model you have installed
            messages=[{"role": "user", "content": prompt}],
            format=ollama_schema  # Our converted schema
        )

        # Process the structured response
        result: dict = response['message']['content']
        print("\nReceived response from Ollama:")
        print(json.dumps(json.loads(result), indent=4))

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
