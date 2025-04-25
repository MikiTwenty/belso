# belso.formats.xml_format

from os import PathLike
from pathlib import Path
from typing import Optional
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from typing import Any, Type, Union

from belso.utils import get_logger
from belso.core import Schema, BaseField
from belso.utils.helpers import create_fallback_schema

# Get a module-specific logger
logger = get_logger(__name__)

def schema_to_xml(
        schema: Type[Schema],
        file_path: Optional[Union[str, Path, PathLike]] = None
    ) -> str:
    """
    Convert a belso Schema to XML format and optionally save to a file.\n
    ---
    ### Args
    - `schema` (`Type[belso.Schema]`): the schema to convert.\n
    - `file_path` (`Optional[Union[str, Path, PathLike]]`): path to save the XML to a file.\n
    ---
    ### Returns
    - `str`: the converted schema.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting conversion of schema '{schema_name}' to XML format...")

        # Create root element
        root = ET.Element("schema")
        root.set("name", schema.__name__)
        logger.debug(f"Created root element with name: {schema.__name__}.")

        # Add fields
        fields_elem = ET.SubElement(root, "fields")
        logger.debug(f"Processing {len(schema.fields)} fields...")

        for field in schema.fields:
            logger.debug(f"Processing field '{field.name}'...")
            field_elem = ET.SubElement(fields_elem, "field")
            field_elem.set("name", field.name)

            # Convert Python type to string representation
            type_str = field.type_.__name__ if hasattr(field.type_, "__name__") else str(field.type_)
            field_elem.set("type", type_str)
            logger.debug(f"BaseField '{field.name}' has type: {type_str}.")

            field_elem.set("required", str(field.required).lower())
            required_status = "required" if field.required else "optional"
            logger.debug(f"BaseField '{field.name}' is {required_status}")

            # Add description as a child element
            if field.description:
                desc_elem = ET.SubElement(field_elem, "description")
                desc_elem.text = field.description
                logger.debug(f"BaseField '{field.name}' has description: '{field.description}'.")

            # Add default value if it exists
            if field.default is not None:
                default_elem = ET.SubElement(field_elem, "default")
                default_elem.text = str(field.default)
                logger.debug(f"BaseField '{field.name}' has default value: {field.default}.")

        # Convert to string with pretty formatting
        logger.debug("Converting XML to string with pretty formatting...")
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        xml_str = reparsed.toprettyxml(indent="  ")

        # Save to file if path is provided
        if file_path:
            logger.debug(f"Saving XML schema to file: {file_path}.")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(xml_str)
                logger.debug(f"Successfully saved XML schema to {file_path}.")
            except Exception as e:
                logger.error(f"Failed to save XML schema to file: {e}")
                logger.debug("File saving error details", exc_info=True)

        logger.debug("Successfully converted schema to XML format.")
        return xml_str

    except Exception as e:
        logger.error(f"Error converting schema to XML format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        return "<schema><fields></fields></schema>"

def xml_to_schema(xml_input: Union[str, ET.Element]) -> Type[Schema]:
    """
    Convert XML data or an XML file to a belso Schema.\n
    ---
    ### Args
    - `xml_input` (`Union[str, ET.Element]`): either an XML string, Element, or a file path to an XML file.\n
    ---
    ### Returns
    - `Type[belso.Schema]`: the converted belso schema.
    """
    try:
        logger.debug("Starting conversion from XML to belso Schema...")

        # Parse input
        if isinstance(xml_input, str):
            # Check if it's a file path
            if "<" not in xml_input:  # Simple heuristic to check if it's XML content
                logger.debug(f"Attempting to load XML from file: {xml_input}.")
                try:
                    tree = ET.parse(xml_input)
                    root = tree.getroot()
                    logger.debug(f"Successfully loaded XML from file: {xml_input}.")
                except (FileNotFoundError, ET.ParseError) as e:
                    logger.error(f"Failed to load XML from file: {e}")
                    logger.debug("File loading error details", exc_info=True)
                    raise ValueError(f"Failed to load XML from file: {e}")
            else:
                # It's an XML string
                logger.debug("Parsing XML from string...")
                try:
                    root = ET.fromstring(xml_input)
                    logger.debug("Successfully parsed XML string.")
                except ET.ParseError as e:
                    logger.error(f"Failed to parse XML string: {e}")
                    logger.debug("XML parsing error details", exc_info=True)
                    raise ValueError(f"Failed to parse XML string: {e}")
        else:
            # Assume it's an ElementTree Element
            logger.debug("Using provided ElementTree Element...")
            root = xml_input

        # Create a new Schema class
        schema_name = root.get("name", "LoadedSchema")
        logger.debug(f"Creating new Schema class with name: {schema_name}.")

        class LoadedSchema(Schema):
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
            fields_count = len(fields_elem.findall("field"))
            logger.debug(f"Found {fields_count} fields in XML...")

            for field_elem in fields_elem.findall("field"):
                name = field_elem.get("name", "")
                field_type_str = field_elem.get("type", "str")
                field_type = type_mapping.get(field_type_str.lower(), str)

                logger.debug(f"Processing field '{name}' with type '{field_type_str}'...")

                # Get required attribute (default to True)
                required_str = field_elem.get("required", "true")
                required = required_str.lower() == "true"
                required_status = "required" if required else "optional"
                logger.debug(f"BaseField '{name}' is {required_status}.")

                # Get description
                desc_elem = field_elem.find("description")
                description = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                if description:
                    logger.debug(f"BaseField '{name}' has description: '{description}'.")

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
                    logger.debug(f"BaseField '{name}' has default value: {default}.")

                field = BaseField(
                    name=name,
                    type_=field_type,
                    description=description,
                    required=required,
                    default=default
                )

                LoadedSchema.fields.append(field)

        logger.debug(f"Successfully created Schema with {len(LoadedSchema.fields)} fields.")
        return LoadedSchema

    except Exception as e:
        logger.error(f"Error converting XML to schema: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        logger.warning("Returning fallback schema due to conversion error.")
        return create_fallback_schema()
