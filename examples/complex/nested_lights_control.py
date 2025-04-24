import json
import ollama

from belso.utils import PROVIDERS
from belso import Schema, Field, Translator

class Room(Schema):
    fields = [
        Field(
            name="lights_on",
            type_hint=bool,
            description="Whether the lights should be on or off",
            required=True
        )
    ]

class House(Schema):
    fields = [
        Field(
            name="Kitchen",
            type_hint=Room,
            description="The kitchen in the house",
            required=True
        ),
        Field(
            name="Bedroom",
            type_hint=Room,
            description="The bedroom in the house",
            required=True
        ),
        Field(
            name="Bathroom",
            type_hint=Room,
            description="The bathroom in the house",
            required=True
        ),
    ]

def main():
    # Convert to Ollama format
    ollama_schema = Translator.translate(House, to=PROVIDERS.OLLAMA)

    print("\nConverted schema to Ollama format:")
    print(json.dumps(ollama_schema, indent=4))

    try:
        # Define the prompt that asks to turn off the lights
        default_prompt = "Turn off all the lights in all the rooms in the house"
        user_prompt = input(f"\n>> Type a prompt (press Enter for default: \"{default_prompt}\"): ")
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
        print(result)

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
