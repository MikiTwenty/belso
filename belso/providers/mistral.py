# belso.providers.mistral

from belso.providers.base import json_provider

to_mistral, from_mistral = json_provider()(lambda: None)
