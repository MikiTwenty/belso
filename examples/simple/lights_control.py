import json
import ollama

from belso.utils import PROVIDERS
from belso import Schema, Field, Translator

# Define a simple schema for light control
class LightsControlSchema(Schema):
    fields = [
        Field(
            name="lights_on",
            type_hint=bool,
            description="Whether the lights should be on or off",
            required=True
        )
    ]

def main():
    # Convert to Ollama format
    ollama_schema = Translator.translate(LightsControlSchema, to=PROVIDERS.OLLAMA)

    print("\nConverted schema to Ollama format:")
    print(json.dumps(ollama_schema, indent=4))

    try:
        # Define the prompt that asks to turn off the lights
        default_prompt = "Turn off the lights"
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
