Welcome to belso's documentation!
=================================

**belso** (Better LLMs Structured Outputs) is a Python library for managing structured schema definitions across multiple LLM providers.
It simplifies the translation, validation, and visualization of complex nested data models used in tools like OpenAI function calling, Google PAI, Anthropic tools, LangChain, and others.

Features
--------

- ✅ Unified schema interface using Python classes
- 🔁 Bi-directional conversion between provider formats (OpenAI, Google, Ollama, Anthropic, Mistral, HuggingFace, LangChain)
- 📦 Support for nested fields and array types
- 📋 Validation and visualization tools for human-readable schema inspection
- ⚡ Minimal dependencies and fast runtime

Installation
------------

Install `belso` from PyPI:

.. code-block:: bash

   pip install belso

Quick Start
-----------

Define your schema and convert it to a target provider format:

.. code-block:: python

   from belso.utils import FORMATS
   from belso import Schema, Field, SchemaProcessor

   class UserSchema(Schema):
       fields = [
           Field(name="name", type=str, description="User's name"),
           Field(name="age", type=int, description="User's age")
       ]

   openai_schema = SchemaProcessor.convert(UserSchema, to=FORMATS.OPENAI)

Documentation Structure
------------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   introduction
   installation
   quickstart
   examples
   changelog

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: API DOCUMENTATION

   user_api/index
   dev_api/index

Search & Index
--------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
