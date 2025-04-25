# Import Schema and Field directly
from belso.core.schema import Schema
from belso.core.field import BaseField, NestedField, ArrayField, Field

# Import processor after the schema classes
from belso.core.processor import SchemaProcessor

# Export all relevant classes
__all__ = [
    "Schema",
    "BaseField",
    "NestedField",
    "ArrayField",
    "Field",
    "SchemaProcessor"
]
