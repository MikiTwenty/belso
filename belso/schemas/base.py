# belso.schemas.base

from typing import Any, List, Optional, Type, ClassVar

class BaseField:
    def __init__(
            self,
            name: str,
            type: Type,
            description: str,
            required: bool = True,
            default: Optional[Any] = None
        ) -> None:
        """
        Initialize a new BaseField instance.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        - `type` (`Type`): the type of the field.
        - `description` (`str`): a description of the field.
        - `required` (`bool`): whether the field is required. Defaults to `True`.
        - `default` (`Optional[Any]`): the default value of the field. Defaults to `None`.
        """
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.default = default

class Schema:
    """
    A base class for defining schemas.
    """
    name: ClassVar[str] = ''
    fields: ClassVar[List[BaseField]] = []

    @classmethod
    def get_required_fields(cls) -> List[str]:
        """
        Get the names of all required fields in the schema.\n
        ---
        ### Returns
        - `List[str]`: a list of required field names.
        """
        return [field.name for field in cls.fields if field.required]

    @classmethod
    def get_field_by_name(
            cls,
            name: str
        ) -> Optional[BaseField]:
        """
        Get a field by its name.\n
        ---
        ### Args
        - `name` (`str`): the name of the field.
        ---
        ### Returns
        - `Optional[BaseField]`: the field with the given name, or `None` if not found.
        """
        for field in cls.fields:
            if field.name == name:
                return field
        return None
