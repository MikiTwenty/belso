# belso.gui.app

from belso.gui.state import GUIState
from belso.gui.layout import build_interface

def run() -> None:
    """
    Run the Belso Schema Editor GUI.
    """
    state = GUIState()
    interface = build_interface(state)
    interface.launch()
