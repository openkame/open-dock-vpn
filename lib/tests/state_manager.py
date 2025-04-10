from PySide6.QtCore import QObject, Signal

class StateManager(QObject):
    """ 🎛️ Gestionnaire de l'état global de l'application """
    switch_view_requested = Signal()
    def __init__(self):
        super().__init__()

    def emit_switch_view_request(self):
        self.switch_view_requested.emit()
    
# 🌍 Instance unique du StateManager
state_manager = StateManager()
        