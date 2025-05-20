# belso.gui.components.schema_toolbar

"""
Schema Toolbar component.
---
Renders the breadcrumb bar and includes related dynamic updates.
"""

from belso.gui.logic.state import state
from belso.utils.logging import get_logger

logger = get_logger(__name__)

def get_breadcrumb_text() -> str:
    """
    Returns the current breadcrumb as a Markdown string.\n
    ---
    ### Returns
    - `str`: breadcrumb markdown.
    """
    stack = state.get_breadcrumb()
    if not stack:
        return "📂 Root"
    return "📂 " + " > ".join(stack)

def refresh_breadcrumb() -> str:
    """
    Callback to refresh the breadcrumb bar.\n
    ---
    ### Returns
    - `str`: updated breadcrumb.
    """
    new_breadcrumb = get_breadcrumb_text()
    logger.debug(f"Breadcrumb updated: {new_breadcrumb}")
    return new_breadcrumb
