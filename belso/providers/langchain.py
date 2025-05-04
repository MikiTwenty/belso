# langchain.py

from belso.providers.base import pydantic_provider

to_langchain, from_langchain = pydantic_provider()(lambda: None)
