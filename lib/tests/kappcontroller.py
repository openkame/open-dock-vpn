from PySide6.QtWidgets import QApplication, QWidget
from full_view import FullView
from compact_view import CompactView
import sys
from state_manager import state_manager

class KAppController(QWidget):
    def __init__(self):
        super().__init__()

        mock_clients = [
            {"name": "Alpha", "favorite": True, "autostart": True, "status": "🟢"},
            {"name": "Beta", "favorite": True, "autostart": False, "status": "🔴"},
            {"name": "Gamma", "favorite": False, "autostart": False, "status": "⚠️"},
            {"name": "Delta", "favorite": True, "autostart": True, "status": "🟢"},
        ]

        # On ne montre JAMAIS ce widget, mais il sert de parent logique
        self.full_view = FullView()
        self.full_view.clients_list.populate_clients(mock_clients)
        self.compact_view = CompactView()
        self.compact_view.populate_clients(mock_clients)

        # Un seul signal pour le switch
        state_manager.switch_view_requested.connect(self.toggle_view)

        # Démarrage sur la full view
        self.compact_view.hide()
        self.full_view.show()

    def toggle_view(self):
        if self.full_view.isVisible():
            self.full_view.showMinimized()
            self.compact_view.show()
            self.compact_view.raise_()
            self.compact_view.activateWindow()

            self.full_view.hide()
        else:
            self.compact_view.showMinimized()
            
            self.full_view.show()
            self.full_view.raise_()
            self.full_view.activateWindow()

            self.compact_view.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = KAppController()
    sys.exit(app.exec())
