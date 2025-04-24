from typing import Type, Optional, Any

from belso.schemas import Schema, BaseField
from belso.utils.logging import get_logger

logger = get_logger(__name__)

class NestedField(BaseField):
    """
    BaseField class for nested schemas.
    Supports all advanced validation parameters passed via BaseField.\n
    Used by:
    - OpenAI
    - Google
    - Ollama
    - Anthropic
    - Mistral
    - LangChain
    - HuggingFace
    """
    def __init__(
            self,
            name: str,
            schema: Type[Schema],
            description: str = "",
            required: bool = True,
            **kwargs: Any
        ) -> None:
        super().__init__(
            name=name,
            type_=dict,
            description=description,
            required=required,
            **kwargs
        )
        self.schema = schema

class ArrayField(BaseField):
    """
    BaseField class for arrays of items.
    Supports all advanced validation parameters passed via BaseField.\n
    Used by:
    - OpenAI
    - Google
    - Ollama
    - Anthropic
    - Mistral
    - LangChain
    - HuggingFace
    """
    def __init__(
            self,
            name: str,
            items_type: Type = str,
            description: str = "",
            required: bool = True,
            **kwargs: Any
        ) -> None:
        super().__init__(
            name=name,
            type_=list,
            description=description,
            required=required,
            **kwargs
        )
        self.items_type = items_type
