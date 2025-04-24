from typing import Type, Optional, Any, List, Dict

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
            default: Optional[Any] = None,
            enum: Optional[List[Any]] = None,
            range_: Optional[tuple] = None,
            exclusive_range: Optional[tuple] = None,
            length_range: Optional[tuple] = None,
            items_range: Optional[tuple] = None,
            properties_range: Optional[tuple] = None,
            regex: Optional[str] = None,
            multiple_of: Optional[float] = None,
            format_: Optional[str] = None
        ) -> None:
        super().__init__(
            name=name,
            type_=dict,
            description=description,
            required=required,
            default=default,
            enum=enum,
            range_=range_,
            exclusive_range=exclusive_range,
            length_range=length_range,
            items_range=items_range,
            properties_range=properties_range,
            regex=regex,
            multiple_of=multiple_of,
            format_=format_
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
            default: Optional[Any] = None,
            enum: Optional[List[Any]] = None,
            range_: Optional[tuple] = None,
            exclusive_range: Optional[tuple] = None,
            length_range: Optional[tuple] = None,
            items_range: Optional[tuple] = None,
            properties_range: Optional[tuple] = None,
            regex: Optional[str] = None,
            multiple_of: Optional[float] = None,
            format_: Optional[str] = None,
            not_: Optional[Dict] = None
        ) -> None:
        super().__init__(
            name=name,
            type_=list,
            description=description,
            required=required,
            default=default,
            enum=enum,
            range_=range_,
            exclusive_range=exclusive_range,
            length_range=length_range,
            items_range=items_range,
            properties_range=properties_range,
            regex=regex,
            multiple_of=multiple_of,
            format_=format_
        )
        self.items_type = items_type
