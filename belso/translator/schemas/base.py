from typing import Any, List, Optional, Type

class Field:
    def __init__(
            self,
            name: str,
            type: Type,
            description: str,
            required: bool = True,
            default: Optional[Any] = None
        ) -> None:
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.default = default

class Schema:
    name: str = ''
    fields: List[Field] = []

    @classmethod
    def get_required_fields(cls) -> List[str]:
        return [field.name for field in cls.fields if field.required]

    @classmethod
    def get_field_by_name(
            cls,
            name: str
        ) -> Optional[Field]:
        for field in cls.fields:
            if field.name == name:
                return field
        return None
