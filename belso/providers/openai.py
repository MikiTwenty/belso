# belso.providers.openai

from belso.providers.base import pydantic_provider

to_openai, from_openai = pydantic_provider()(lambda: None)
