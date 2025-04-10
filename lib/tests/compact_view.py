from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt

from state_manager import state_manager


class CompactView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compact View (Mock)")
        self.setFixedSize(300, 250)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self._drag_position = None  # 📦 Stocke la position de départ du drag

        # ───────────── Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self._build_header()
        self.client_zone = QVBoxLayout()
        self.main_layout.addLayout(self.client_zone)

        self.label_empty = QLabel("📭 No VPN clients yet")
        self.label_empty.setAlignment(Qt.AlignCenter)
        self.label_empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.client_zone.addWidget(self.label_empty)

    def _build_header(self):
        """ 🔧 En-tête avec boutons """
        header_layout = QHBoxLayout()

        switch_button = QPushButton("🟰")
        switch_button.setFixedSize(30, 30)
        switch_button.clicked.connect(state_manager.emit_switch_view_request)
        header_layout.addWidget(switch_button)

        title = QLabel("VPN Compact View")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title, 1)

        btn_hide = QPushButton("❌")
        btn_hide.setFixedSize(30, 30)
        btn_hide.clicked.connect(self.hide)
        header_layout.addWidget(btn_hide)

        self.main_layout.addLayout(header_layout)

    def populate_clients(self, clients: list[dict]):
        """ 🔄 Met à jour dynamiquement la liste des clients favoris """
        # Nettoyage précédent
        while self.client_zone.count():
            item = self.client_zone.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Filtrer favoris
        favorites = [c for c in clients if c.get("favorite", False)]

        if not favorites:
            self.client_zone.addWidget(self.label_empty)
            return

        self.label_empty.hide()

        for client in favorites[:3]:  # Affiche max 3
            layout = QHBoxLayout()
            name = QLabel(client.get("name", "Unknown"))
            layout.addWidget(name)

            btn_toggle = QPushButton("⏹" if client.get("autostart") else "▶️")
            btn_toggle.setFixedSize(30, 30)
            layout.addWidget(btn_toggle)

            status_icon = QLabel(client.get("status", "🟢"))
            layout.addWidget(status_icon)

            self.client_zone.addLayout(layout)

    # ───────────── Mouse Events pour déplacement
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_position:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_position = None

        