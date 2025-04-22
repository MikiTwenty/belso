.. belso documentation master file, created by
   sphinx-quickstart on Tue Apr 22 16:22:34 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to belso's documentation!
=================================

**belso** (Better LLMs Structured Outputs) is a Python library designed to simplify working with structured outputs from various LLM providers.

Features
--------

* Convert between different LLM provider schema formats
* Support for nested schemas
* Validation of structured outputs
* Support for multiple providers including OpenAI, Google, Anthropic, Mistral, and more

Installation
------------

.. code-block:: bash

   pip install belso

Quick Start
-----------

.. code-block:: python

   from belso.schemas import Schema, Field
   from belso.translator import SchemaTranslator
   from belso.validator import SchemaValidator

   # Define your schema
   class UserSchema(Schema):
       name = "UserSchema"
       fields = [
           Field(name="name", type=str, description="User's name", required=True),
           Field(name="age", type=int, description="User's age", required=True)
       ]

   # Translate to OpenAI format
   openai_schema = SchemaTranslator.to_provider(UserSchema, "openai")

   # Validate data against schema
   data = {"name": "John", "age": 30}
   validated_data = SchemaValidator.validate(data, UserSchema)

API Documentation
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   belso

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

