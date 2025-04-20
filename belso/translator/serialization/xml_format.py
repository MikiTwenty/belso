import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from typing import Dict, Any, Type, Union

from belso.translator.schemas import Schema, Field

def schema_to_xml(
        schema: Type[Schema],
        file_path: str = None
    ) -> str:
    """
    Convert a Belso Schema to XML format and optionally save to a file.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    - `file_path`: optional path to save the XML to a file.\n
    ---
    ### Returns
    - `str`: the schema in XML format.
    """
    # Create root element
    root = ET.Element("schema")
    root.set("name", schema.name)

    # Add fields
    fields_elem = ET.SubElement(root, "fields")

    for field in schema.fields:
        field_elem = ET.SubElement(fields_elem, "field")
        field_elem.set("name", field.name)

        # Convert Python type to string representation
        type_str = field.type.__name__ if hasattr(field.type, "__name__") else str(field.type)
        field_elem.set("type", type_str)

        field_elem.set("required", str(field.required).lower())

        # Add description as a child element
        if field.description:
            desc_elem = ET.SubElement(field_elem, "description")
            desc_elem.text = field.description

        # Add default value if it exists
        if field.default is not None:
            default_elem = ET.SubElement(field_elem, "default")
            default_elem.text = str(field.default)

    # Convert to string with pretty formatting
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    xml_str = reparsed.toprettyxml(indent="  ")

    # Save to file if path is provided
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)

    return xml_str

def xml_to_schema(xml_input: Union[str, ET.Element]) -> Type[Schema]:
    """
    Convert XML data or an XML file to a Belso Schema.\n
    ---
    ### Args
    - `xml_input`: either an XML string, Element, or a file path to an XML file.\n
    ---
    ### Returns
    - `Type[Schema]`: the Belso Schema.
    """
    # Parse input
    if isinstance(xml_input, str):
        # Check if it's a file path
        if "<" not in xml_input:  # Simple heuristic to check if it's XML content
            try:
                tree = ET.parse(xml_input)
                root = tree.getroot()
            except (FileNotFoundError, ET.ParseError) as e:
                raise ValueError(f"Failed to load XML from file: {e}")
        else:
            # It's an XML string
            try:
                root = ET.fromstring(xml_input)
            except ET.ParseError as e:
                raise ValueError(f"Failed to parse XML string: {e}")
    else:
        # Assume it's an ElementTree Element
        root = xml_input

    # Create a new Schema class
    class LoadedSchema(Schema):
        name = root.get("name", "LoadedSchema")
        fields = []

    # Type mapping from string to Python types
    type_mapping = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "any": Any
    }

    # Process each field
    fields_elem = root.find("fields")
    if fields_elem is not None:
        for field_elem in fields_elem.findall("field"):
            name = field_elem.get("name", "")
            field_type_str = field_elem.get("type", "str")
            field_type = type_mapping.get(field_type_str.lower(), str)

            # Get required attribute (default to True)
            required_str = field_elem.get("required", "true")
            required = required_str.lower() == "true"

            # Get description
            desc_elem = field_elem.find("description")
            description = desc_elem.text if desc_elem is not None and desc_elem.text else ""

            # Get default value
            default = None
            default_elem = field_elem.find("default")
            if default_elem is not None and default_elem.text:
                # Convert default value to the appropriate type
                if field_type == bool:
                    default = default_elem.text.lower() == "true"
                elif field_type == int:
                    default = int(default_elem.text)
                elif field_type == float:
                    default = float(default_elem.text)
                else:
                    default = default_elem.text

            field = Field(
                name=name,
                type=field_type,
                description=description,
                required=required,
                default=default
            )

            LoadedSchema.fields.append(field)

    return LoadedSchema
