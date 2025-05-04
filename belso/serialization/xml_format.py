# belso.serialization.xml_format

from pathlib import Path
from typing import Optional, Type, Union

from belso.utils import get_logger
import xml.etree.ElementTree as ET
from belso.core import Schema, BaseField
from belso.core.field import NestedField, ArrayField
from belso.utils.helpers import create_fallback_schema
from belso.utils.mappings.type_mappings import _FILE_TYPE_MAP

_logger = get_logger(__name__)

def _add_prefix(
        base: str,
        prefix: str
    ) -> str:
    """
    Add `prefix` only if `base` does not already start with it.\n
    ---
    ### Args
    - `base` (`str`): string to which `prefix` is applied.
    - `prefix` (`str`): prefix to apply to `base`.\n
    ---
    ### Returns
    - `str`: `base` with `prefix` applied if needed.\n
    """
    return base if (not prefix or base.startswith(prefix)) else f"{prefix}{base}"

def _indent(
        elem: ET.Element,
        level: int = 0
    ) -> None:
    """
    Pretty-print helper.\n
    ---
    ### Args
    - `elem` (`ET.Element`): element to pretty-print.
    - `level` (`int`): current level of indentation.\n
    ---
    ### Returns
    - `None`: pretty-printing is done in-place.
    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            _indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i + "  "
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = i
    elif level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

def _to_xml(
        schema: Type[Schema], *,
        root_prefix: str = ""
    ) -> ET.Element:
    """
    Serialise `schema` to XML. `root_prefix` is applied once to the
    root schema only; children keep their own names untouched.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): schema to serialise.
    - `root_prefix` (`str`): prefix to apply to the root schema name.\n
    ---
    ### Returns
    - `ET.Element`: root element of the XML representation of `schema`.
    """
    root = ET.Element("schema", {"name": _add_prefix(schema.__name__, root_prefix)})
    fields_el = ET.SubElement(root, "fields")

    for fld in schema.fields:
        f_el = ET.SubElement(fields_el, "field", {
            "name": fld.name,
            "type": fld.type_.__name__ if hasattr(fld.type_, "__name__") else str(fld.type_),
            "required": str(fld.required).lower()
        })
        if fld.description:
            ET.SubElement(f_el, "description").text = fld.description
        if fld.default is not None:
            ET.SubElement(f_el, "default").text = str(fld.default)

        # nested object
        if isinstance(fld, NestedField):
            n_el = ET.SubElement(f_el, "nested_schema")
            n_el.append(_to_xml(fld.schema, root_prefix=""))  # no extra prefix
            continue

        # array
        if isinstance(fld, ArrayField):
            a_el = ET.SubElement(f_el, "array_info")
            ET.SubElement(a_el, "items_type").text = (
                fld.items_type.__name__ if hasattr(fld.items_type, "__name__") else str(fld.items_type)
            )
            if fld.items_schema:
                is_el = ET.SubElement(a_el, "items_schema")
                is_el.append(_to_xml(fld.items_schema, root_prefix=""))  # no extra prefix
            continue

    return root

def to_xml(
        schema: Type[Schema],
        file_path: Optional[Union[str, Path]] = None,
        schema_name: str = "") -> str:
    """
    Serialise `schema` to XML. `schema_name` is applied once to the
    root schema only; children keep their own names untouched.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): schema to serialise.
    - `file_path` (`Optional[Union[str, Path]]`): path to save the XML file.
    - `schema_name` (`str`): prefix to apply to the root schema name.\n
    ---
    ### Returns
    - `str`: XML representation of `schema`.
    """
    try:
        root = _to_xml(schema, root_prefix=schema_name)
        _indent(root)
        xml_text = ET.tostring(root, encoding="unicode")
        if file_path:
            _logger.debug(f"Saving XML schema to file \"{file_path}\"...")
            Path(file_path).write_text(xml_text, encoding="utf-8")
            _logger.info(f"XML schema saved to file \"{file_path}\".")
            return str(file_path)
        return xml_text
    except Exception as e:  # pragma: no cover
        _logger.error(f"Error converting schema to XML: {e}", exc_info=True)
        return "<schema><fields></fields></schema>"

def _from_xml(elem: ET.Element) -> Type[Schema]:
    """
    Deserialise XML into a belso Schema.\n
    ---
    ### Args
    - `elem` (`ET.Element`): root element of the XML representation of a schema.\n
    ---
    ### Returns
    - `Type[Schema]`: schema deserialised from `elem`.
    """
    class DynamicSchema(Schema):
        fields: list = []

    DynamicSchema.__name__ = elem.get("name", "LoadedSchema")

    for f_el in elem.find("fields").findall("field"):
        fname = f_el.get("name")
        ftype_str = f_el.get("type", "str")
        ftype = _FILE_TYPE_MAP.get(ftype_str.lower(), str)
        frequired = f_el.get("required", "true") == "true"
        fdesc = f_el.findtext("description", "")
        fdef_el = f_el.find("default")
        fdefault = fdef_el.text if fdef_el is not None else None

        # nested
        nested_root = f_el.find("nested_schema/schema")
        if nested_root is not None:
            nested_schema = _from_xml(nested_root)
            DynamicSchema.fields.append(
                NestedField(
                    name=fname,
                    schema=nested_schema,
                    description=fdesc,
                    required=frequired,
                    default=fdefault)
            )
            continue

        # array
        arr_info = f_el.find("array_info")
        if arr_info is not None:
            items_type_str = arr_info.findtext("items_type", "str")
            items_type = _FILE_TYPE_MAP.get(items_type_str.lower(), str)
            items_schema_root = arr_info.find("items_schema/schema")

            if items_schema_root is not None:
                items_schema = _from_xml(items_schema_root)
                DynamicSchema.fields.append(
                    ArrayField(
                        name=fname,
                        items_type=items_type,
                        items_schema=items_schema,
                        description=fdesc,
                        required=frequired,
                        default=fdefault)
                )
            else:
                DynamicSchema.fields.append(
                    ArrayField(
                        name=fname,
                        items_type=items_type,
                        description=fdesc,
                        required=frequired,
                        default=fdefault)
                )
            continue

        # primitive
        DynamicSchema.fields.append(
            BaseField(
                name=fname,
                type_=ftype,
                description=fdesc,
                required=frequired,
                default=fdefault)
        )

    return DynamicSchema

def from_xml(
        xml_input: Union[str, Path, ET.Element],
        schema_name: str = ""
    ) -> Type[Schema]:
    """
    Load XML (string / file / Element) into a belso Schema.
    `schema_name` is applied **only** to the root schema name.\n
    ---
    ### Args
    - `xml_input` (`Union[str, Path, ET.Element]`): XML input.
    - `schema_name` (`str`): prefix to apply to the root schema name.\n
    ---
    ### Returns
    - `Type[Schema]`: schema deserialised from `xml_input`.
    """
    try:
        _logger.debug(f"Loading XML schema...")
        if isinstance(xml_input, (str, Path)):
            _logger.debug(f"Loading XML schema from \"{xml_input}\"...")
            xml_text = Path(xml_input).read_text(encoding="utf-8") if Path(xml_input).exists() else xml_input
            root = ET.fromstring(xml_text)
            if isinstance(xml_input, Path) or (isinstance(xml_input, str) and Path(xml_input).exists()):
                _logger.info(f"XML schema loaded from file: \"{xml_input}\".")
            elif isinstance(xml_input, str):
                _logger.debug("XML schema loaded from string input.")
            else:
                _logger.debug("XML schema loaded from ElementTree memory object.")
        else:
            root = xml_input
            _logger.debug(f"XML schema loaded from memory.")

        schema_cls = _from_xml(root)
        schema_cls.__name__ = _add_prefix(schema_cls.__name__, schema_name)
        return schema_cls

    except Exception as e:  # pragma: no cover
        _logger.error(f"Error loading schema from XML: {e}", exc_info=True)
        return create_fallback_schema()
