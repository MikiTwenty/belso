Quick Start Guide
=================

This guide will help you get started with belso quickly.

Basic Usage
-----------

1. Define a Schema
~~~~~~~~~~~~~~~~~~

First, define your schema using belso's Schema and Field classes:

.. code-block:: python

   from belso import Schema, Field

   class UserSchema(Schema):
       name = "UserSchema"
       fields = [
           Field(name="name", type_=str, description="User's name", required=True),
           Field(name="age", type_=int, description="User's age", required=True)
       ]

2. Translate to Provider Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert your schema to a specific provider format:

.. code-block:: python

    from belso import SchemaProcessor
    from belso.utils import PROVIDERS

    # Convert to OpenAI format
    openai_schema = SchemaProcessor.translate(UserSchema, to=PROVIDERS.OPENAI)

    # Convert to Anthropic format
    anthropic_schema = SchemaProcessor.translate(UserSchema, to=PROVIDERS.ANTHROPIC)
