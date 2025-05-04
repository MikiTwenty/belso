# belso.providers.huggingface

from belso.providers.base import json_provider

to_huggingface, from_huggingface = json_provider(
    extra_metadata={
        "format": "huggingface"
    }
)(lambda: None)
