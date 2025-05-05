from typing import List

import json
import ollama

from belso.utils import FORMATS
from belso import Schema, Field
from belso.core.processor import SchemaProcessor

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
    fields = [Field("Lights", type=List[Light], description="The lights in the room", items_range=(1, 3))]

class House(Schema):
    fields = [Field("Rooms", type=List[Room], description="The rooms in the house", items_range=(1, 3))]

def main():
    # Display the schema
    SchemaProcessor.display(House)

    # Convert the schema to Ollama format
    ollama_schema = SchemaProcessor.convert(House, to=FORMATS.OLLAMA)

    # Display the converted schema
    print("\nConverted schema to Ollama format:")
    print(json.dumps(ollama_schema, indent=4))

    try:
        # Define the prompt for array data generation
        default_prompt = "Generate an house with multiple rooms and lights."
        print(f"\nDefault prompt:\n\"{default_prompt}\"")

        # Ask the user for a prompt
        user_prompt = input(f"\n>> Type a prompt (press Enter to use default prompt): ")
        prompt = user_prompt or default_prompt

        # Make the request to Ollama with our schema
        response = ollama.chat(
            model="llama3.2:1b-instruct-fp16",  # You may need to change this to a model you have installed
            messages=[{"role": "user", "content": prompt}],
            format=ollama_schema  # Our converted schema
        )
        result = response['message']['content']

        # Display the response
        print("\nReceived response from Ollama:")
        print(json.dumps(json.loads(result), indent=4))

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

