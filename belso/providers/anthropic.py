# belso.providers.anthropic

from belso.providers.base import json_provider

to_anthropic, from_anthropic = json_provider(
    extra_metadata={
        "$schema": "http://json-schema.org/draft-07/schema#"
    }
)(lambda: None)
