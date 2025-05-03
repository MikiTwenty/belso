from typing import List

import json
import ollama

from belso.utils import FORMATS
from belso import Schema, Field
from belso.core.processor import SchemaProcessor

# Define a simple schema for items in the array
class ItemSchema(Schema):
    fields = [
        Field(
            name="id",
            type=int,
            description="Unique identifier for the item",
            required=True
        ),
        Field(
            name="name",
            type=str,
            description="Name of the item",
            required=True
        ),
        Field(
            name="active",
            type=bool,
            description="Whether the item is active",
            required=False,
            default=True
        )
    ]

# Define a schema with different types of array fields
class ArrayFieldsTestSchema(Schema):
    fields = [
        # Simple array of primitive types
        Field(
            name="tags",
            type=List[str],
            description="List of string tags",
            required=True
        ),

        # Array with range constraints
        Field(
            name="scores",
            type=List[int],
            description="List of integer scores",
            required=True,
            items_range=(1, 5)  # Min 1, max 5 items
        ),

        # Array of complex objects (nested schema)
        Field(
            name="items",
            type=List[ItemSchema],
            description="List of item objects",
            required=True
        ),

        # Optional array
        Field(
            name="optional_data",
            type=List[float],
            description="Optional list of float values",
            required=False,
            default=[]
        )
    ]

def main():
    # Display the schema
    SchemaProcessor.display(ArrayFieldsTestSchema)

    # Convert to Ollama format
    ollama_schema = SchemaProcessor.translate(ArrayFieldsTestSchema, to=FORMATS.OLLAMA)

    print("\nConverted schema to Ollama format:")
    print(json.dumps(ollama_schema, indent=4))

    try:
        # Define the prompt for array data generation
        default_prompt = "Generate an array of 3 items with tags, scores, and item details"
        print(f"\nDefault prompt:\n\"{default_prompt}\"")

        user_prompt = input(f"\n>> Type a prompt (press Enter to use default prompt): ")
        prompt = user_prompt or default_prompt

        # Make the request to Ollama with our schema
        response = ollama.chat(
            model="llama3.2:1b-instruct-fp16",  # You may need to change this to a model you have installed
            messages=[{"role": "user", "content": prompt}],
            format=ollama_schema  # Our converted schema
        )

        # Process the structured response
        result = response['message']['content']
        print("\nReceived response from Ollama:")
        print(json.dumps(json.loads(result), indent=4))

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

