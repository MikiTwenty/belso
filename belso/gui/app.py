# belso.gui.app

import logging

from belso.gui.state import GUIState
from belso.gui.layout import build_interface

logger = logging.getLogger(__name__)

def run() -> None:
    """
    Run the Belso Schema Editor GUI.
    """
    logger.info("Starting Belso GUI...")
    state = GUIState()
    interface = build_interface(state)
    interface.launch()
