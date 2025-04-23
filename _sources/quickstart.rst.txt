Quick Start Guide
=================

This guide will help you get started with belso quickly.

Basic Usage
-----------

1. Define a Schema
~~~~~~~~~~~~~~~~~~

First, define your schema using belso's Schema and Field classes:

.. code-block:: python

   from belso.schemas import Schema, Field

   class UserSchema(Schema):
       name = "UserSchema"
       fields = [
           Field(name="name", type=str, description="User's name", required=True),
           Field(name="age", type=int, description="User's age", required=True)
       ]

2. Translate to Provider Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert your schema to a specific provider format:

.. code-block:: python

    from belso.utils import PROVIDERS
    from belso.translator import SchemaTranslator

    # Convert to OpenAI format
    openai_schema = SchemaTranslator.translate(UserSchema, to=PROVIDERS.OPENAI)

    # Convert to Anthropic format
    anthropic_schema = SchemaTranslator.translate(UserSchema, to=PROVIDERS.ANTHROPIC)

3. Validate Data
~~~~~~~~~~~~~~~~

Validate data against your schema:

.. code-block:: python

   from belso.validator import SchemaValidator

   data = {"name": "John", "age": 30}
   validated_data = SchemaValidator.validate(data, UserSchema)
