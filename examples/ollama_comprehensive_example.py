import json
import ollama
from typing import List

from belso.utils import FORMATS
from belso import Schema, Field, SchemaProcessor

# Define a schema for a person's contact information
class ContactInfo(Schema):
    fields = [
        Field(
            name="email",
            type=str,
            description="Email address",
            regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        ),
        Field(
            name="phone",
            type=str,
            description="Phone number",
            default="N/A"
        ),
        Field(
            name="preferred_contact",
            type=str,
            description="Preferred contact method",
            enum=["email", "phone", "mail"]
        )
    ]

# Define a schema for an address
class Address(Schema):
    fields = [
        Field(
            name="street",
            type=str,
            description="Street address",
            length_range=(5, 100)
        ),
        Field(
            name="city",
            type=str,
            description="City name"
        ),
        Field(
            name="postal_code",
            type=str,
            description="Postal code"
        ),
        Field(
            name="country",
            type=str,
            description="Country name"
        )
    ]

# Define a schema for a skill
class Skill(Schema):
    fields = [
        Field(
            name="name",
            type=str,
            description="Name of the skill"
        ),
        Field(
            name="level",
            type=int,
            description="Proficiency level from 1 to 5",
            range=(1, 5)
        ),
        Field(
            name="years_experience",
            type=float,
            description="Years of experience with this skill",
            range=(0, 50),
            multiple_of=0.5
        ),
        Field(
            name="certified",
            type=bool,
            description="Whether the person is certified in this skill",
            default=False
        )
    ]

# Define a comprehensive schema that uses all field types and validation options
class ComprehensiveProfile(Schema):
    fields = [
        # Basic primitive types
        Field(
            name="id",
            type=int,
            description="Unique identifier"
        ),
        Field(
            name="name",
            type=str,
            description="Full name",
            length_range=(2, 50)
        ),
        Field(
            name="age",
            type=int,
            description="Age in years",
            range=(18, 120)
        ),
        Field(
            name="height",
            type=float,
            description="Height in meters",
            range=(0.5, 2.5)
        ),
        Field(
            name="is_active",
            type=bool,
            description="Whether the profile is active"
        ),

        # Nested object fields
        Field(
            name="contact",
            type=ContactInfo,
            description="Contact information"
        ),
        Field(
            name="address",
            type=Address,
            description="Physical address"
        ),

        # Array fields with primitive types
        Field(
            name="interests",
            type=List[str],
            description="List of interests",
            default=[]
        ),
        Field(
            name="scores",
            type=List[int],
            description="List of test scores",
            items_range=(1, 10)  # Min 1, max 10 items
        ),
        Field(
            name="measurements",
            type=List[float],
            description="Various measurements"
        ),

        # Array of complex objects
        Field(
            name="skills",
            type=List[Skill],
            description="List of skills",
            items_range=(1, 5)  # Min 1, max 5 skills
        ),

        # Enum field
        Field(
            name="status",
            type=str,
            description="Current status",
            enum=["available", "busy", "away", "offline"]
        ),

        # Field with regex pattern
        Field(
            name="username",
            type=str,
            description="Username (alphanumeric, 3-15 chars)",
            regex=r"^[a-zA-Z0-9_]{3,15}$"
        ),

        # Field with exclusive range
        Field(
            name="rating",
            type=float,
            description="Rating score (exclusive range)",
            exclusive_range=(0, 10)  # Greater than 0, less than 10
        ),

        # Field with format
        Field(
            name="created_at",
            type=str,
            description="Creation date (ISO format)",
            format="date-time"
        )
    ]

def main():
    # Display the schema
    print("Displaying the comprehensive schema:")
    SchemaProcessor.display(ComprehensiveProfile)

    # Convert to Ollama format
    ollama_schema = SchemaProcessor.translate(ComprehensiveProfile, to=FORMATS.OLLAMA)

    print("\nConverted schema to Ollama format:")
    print(json.dumps(ollama_schema, indent=4))

    try:
        # Define the prompt for generating a profile
        default_prompt = (
            "Generate a comprehensive profile for a software developer named Alex Johnson "
            "who is 32 years old, 1.78m tall, and currently active. "
            "Include contact information, address, skills (at least 3), interests, and other required fields."
        )
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
