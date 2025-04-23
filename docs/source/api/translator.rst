Translator
==========

.. autoclass:: belso.translator.SchemaTranslator
   :members:
   :show-inheritance:
   :undoc-members:

Providers
---------

OpenAI Provider
~~~~~~~~~~~~~~~

.. autofunction:: belso.translator.providers.to_openai
.. autofunction:: belso.translator.providers.from_openai

Anthropic Provider
~~~~~~~~~~~~~~~~~~

.. autofunction:: belso.translator.providers.to_anthropic
.. autofunction:: belso.translator.providers.from_anthropic

Google Provider
~~~~~~~~~~~~~~~

.. autofunction:: belso.translator.providers.to_google
.. autofunction:: belso.translator.providers.from_google

Mistral Provider
~~~~~~~~~~~~~~~~

.. autofunction:: belso.translator.providers.to_mistral
.. autofunction:: belso.translator.providers.from_mistral

Ollama Provider
~~~~~~~~~~~~~~~

.. autofunction:: belso.translator.providers.to_ollama
.. autofunction:: belso.translator.providers.from_ollama

HuggingFace Provider
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: belso.translator.providers.to_huggingface
.. autofunction:: belso.translator.providers.from_huggingface

LangChain Provider
~~~~~~~~~~~~~~~~~~

.. autofunction:: belso.translator.providers.to_langchain
.. autofunction:: belso.translator.providers.from_langchain

Serialization
-------------

JSON Format
~~~~~~~~~~~

.. autofunction:: belso.translator.serialization.schema_to_json
.. autofunction:: belso.translator.serialization.json_to_schema

XML Format
~~~~~~~~~~

.. autofunction:: belso.translator.serialization.schema_to_xml
.. autofunction:: belso.translator.serialization.xml_to_schema

Utils
-----

.. autofunction:: belso.translator.utils.detect_schema_format
