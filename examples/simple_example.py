import json
import ollama

from belso.utils import FORMATS
from belso import Schema, Field, SchemaProcessor

# Define a simple schema for light control
class Lights(Schema):
    fields = [Field("lights_on", type=bool, description="Whether the lights should be on or off")]

def main():
    # Display the schema
    SchemaProcessor.display(Lights)

    # Convert the schema to Ollama format
    ollama_schema = SchemaProcessor.convert(Lights, to=FORMATS.OLLAMA)

    # Display the converted schema
    print("\nConverted schema to Ollama format:")
    print(json.dumps(ollama_schema, indent=4))

    try:
        # Define the prompt that asks to turn off the lights
        default_prompt = "Turn off the lights"
        print(f"\nDefault prompt:\n\"{default_prompt}\"")

        # Ask the user for a prompt
        user_prompt = input(f"\n>> Type a prompt (press Enter to use default prompt): ")
        prompt = user_prompt or default_prompt

        # Make the actual request to Ollama with our schema
        response = ollama.chat(
            model="llama3.2:1b-instruct-fp16",  # You may need to change this to a model you have installed
            messages=[{"role": "user", "content": prompt}],
            format=ollama_schema  # Our converted schema
        )
        result: dict = response['message']['content']

        # Display the response
        print("\nReceived response from Ollama:")
        print(json.dumps(json.loads(result), indent=4))

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
