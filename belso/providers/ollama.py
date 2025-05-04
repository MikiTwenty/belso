# belso.providers.ollama

from belso.providers.base import json_provider

to_ollama, from_ollama = json_provider()(lambda: None)
