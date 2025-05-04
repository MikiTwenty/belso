Quick Start Guide
=================

This guide will help you get started with Belso quickly.

Basic Usage
-----------

1. Define a Schema
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from belso import Schema, Field

   class UserSchema(Schema):
       fields = [
           Field(name="name", type_=str, description="User's name"),
           Field(name="age", type_=int, description="User's age")
       ]

2. Convert to Provider Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from belso import SchemaProcessor
   from belso.utils import FORMATS

   # Convert to OpenAI format
   openai_schema = SchemaProcessor.convert(UserSchema, to=FORMATS.OPENAI)

   # Convert to Anthropic format
   anthropic_schema = SchemaProcessor.convert(UserSchema, to=FORMATS.ANTHROPIC)
