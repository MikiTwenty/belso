import re
from sphinx.application import Sphinx

class CustomDocstringProcessor:
    """
    Process custom docstring format to make it compatible with Sphinx.
    """
    def __init__(self):
        self.docstring = []

    def process(self, docstring) -> list:
        """
        Process the docstring to convert custom format to bullet-list reST with fallback logic.\n
        ---
        ### Args
        - `docstring` (`list[str]`): the docstring to process.\n
        ---
        ### Returns
        - `list[str]`: the processed docstring lines.
        """
        if not docstring:
            return []

        if len(docstring) == 1 and '\n' in docstring[0]:
            self.docstring = docstring[0].split('\n')
        else:
            self.docstring = docstring

        result = []
        in_args_section = False
        in_returns_section = False

        for line in self.docstring:
            stripped = line.strip()

            if stripped == '---':
                continue

            if stripped.startswith('###'):
                section = stripped[3:].strip().lower()
                in_args_section = section == 'args'
                in_returns_section = section == 'returns'
                result.append("")
                result.append(f".. rubric:: {section.capitalize()}")
                result.append("")
                continue

            # Fallback-safe parameter extraction
            if stripped.startswith('-'):
                # Match cases: - `param` (`type`): description
                match_full = re.match(r'^\s*-\s+`([^`]+)`\s+\(`([^`]+)`\):\s*(.*)', stripped)
                match_no_type = re.match(r'^\s*-\s+`([^`]+)`\s*:\s*(.*)', stripped)
                match_no_desc = re.match(r'^\s*-\s+`([^`]+)`\s+\(`([^`]+)`\)', stripped)

                # Args with param, type, and desc
                if in_args_section and match_full:
                    param, param_type, desc = match_full.groups()
                    desc = self._inline_code(desc)
                    highlighted_type = f":customtype:`{param_type}`"
                    result.append(f"- **{param}** ({highlighted_type}): {desc}")
                    continue

                # Args with param and description only
                if in_args_section and match_no_type:
                    param, desc = match_no_type.groups()
                    desc = self._inline_code(desc)
                    result.append(f"- **{param}**: {desc}")
                    continue

                # Args with param and type only (no desc)
                if in_args_section and match_no_desc:
                    param, param_type = match_no_desc.groups()
                    highlighted_type = f":customtype:`{param_type}`"
                    result.append(f"- **{param}** ({highlighted_type})")
                    continue

                # Return with type and description
                match_return = re.match(r'^\s*-\s+`([^`]+)`:\s*(.*)', stripped)
                match_return_notypedesc = re.match(r'^\s*-\s+`([^`]+)`\s*', stripped)
                if in_returns_section:
                    if match_return:
                        return_type, desc = match_return.groups()
                        desc = self._inline_code(desc)
                        highlighted_type = f":customtype:`{return_type}`"
                        result.append(f"- {highlighted_type}: {desc}")
                        continue
                    elif match_return_notypedesc:
                        return_type = match_return_notypedesc.groups()[0]
                        highlighted_type = f":customtype:`{return_type}`"
                        result.append(f"- {highlighted_type}")
                        continue

            # Skip unwanted formatting
            if ':' in stripped and not stripped.startswith('-'):
                continue
            if stripped.lower().startswith('return type') or stripped.lower().startswith('parameters'):
                continue

            result.append(self._inline_code(stripped))

        return result

    def _inline_code(self, text: str) -> str:
        """
        Replace markdown-style `inline code` with reST ``inline code``.\n
        ---
        ### Args
        - `text` (`str`): the text to process.\n
        ---
        ### Returns
        - `str`: text with inline code blocks rendered in reST.
        """
        return re.sub(r'`([^`]+)`', r'``\1``', text)


def process_docstring(app, what, name, obj, options, docstring):
    processor = CustomDocstringProcessor()
    processed = processor.process(docstring)
    docstring.clear()
    docstring.extend(processed)


def setup(app):
    from docutils import nodes
    from docutils.parsers.rst import roles

    def customtype_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        node = nodes.literal(text, text)
        node['classes'].append('customtype')
        return [node], []

    roles.register_local_role('customtype', customtype_role)

    app.connect('autodoc-process-docstring', process_docstring)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

