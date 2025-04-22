from docutils import nodes
from sphinx.application import Sphinx
import re

class CustomDocstringProcessor:
    """Process custom docstring format to make it compatible with Sphinx."""

    def __init__(self):
        # Initialize with empty docstring
        self.docstring = []

    def process(self, docstring):
        """
        Process the docstring to convert custom format to Sphinx format.

        Args:
            docstring: The docstring to process

        Returns:
            The processed docstring
        """
        if not docstring:
            return []

        # Store the docstring for processing
        self.docstring = docstring

        # Process markdown-style section headers (---) and replace with proper RST format
        result = []
        in_section = False

        for line in self.docstring:
            # Handle section dividers (---)
            if line.strip() == '---':
                in_section = not in_section
                continue

            # Handle markdown headers (### Header)
            if line.strip().startswith('###'):
                header_text = line.strip()[3:].strip()
                result.append(header_text)
                result.append('-' * len(header_text))
                continue

            # Process bullet points with markdown-style formatting
            if re.match(r'^\s*-\s+`([^`]+)`\s+\(`([^`]+)`\):', line):
                # Convert "- `param` (`type`): description" to ":param param: description"
                match = re.match(r'^\s*-\s+`([^`]+)`\s+\(`([^`]+)`\):\s*(.*)', line)
                if match:
                    param, param_type, desc = match.groups()
                    result.append(f":param {param}: {desc}")
                    result.append(f":type {param}: {param_type}")
                    continue

            # Add other lines unchanged
            result.append(line)

        return result

def process_docstring(app, what, name, obj, options, docstring):
    """
    Process the docstring for autodoc.

    Args:
        app: The Sphinx application
        what: The type of the object
        name: The name of the object
        obj: The object itself
        options: The options given to the directive
        docstring: The docstring to process
    """
    processor = CustomDocstringProcessor()
    processed = processor.process(docstring)

    # Clear the original docstring and extend with processed content
    docstring.clear()
    docstring.extend(processed)

def setup(app):
    """
    Setup the extension.

    Args:
        app: The Sphinx application
    """
    app.connect('autodoc-process-docstring', process_docstring)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
