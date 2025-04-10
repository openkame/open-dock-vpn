from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt

class KClientFullCard(QWidget):
    def __init__(self, client_name, status_icon="🟢", autostart=True, is_favorite=False):
        super().__init__()
        self.setFixedHeight(80)

        # On encadre chaque carte
        #self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        layout = QVBoxLayout(self)

        # Ligne du haut (Nom + étoile si favori)
        top_row = QHBoxLayout()
        name_label = QLabel(f"Client Name : {client_name}")
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        top_row.addWidget(name_label)

        if is_favorite:
            fav_label = QLabel("⭐")
            top_row.addWidget(fav_label, alignment=Qt.AlignRight)

        layout.addLayout(top_row)

        # Ligne du bas (Statut + Autostart)
        bottom_row = QHBoxLayout()

        status_label = QLabel("Status : " + status_icon)
        bottom_row.addWidget(status_label)

        startup_label = QLabel("Autostart : 🚀" if autostart else "Autostart : ⛔️")
        bottom_row.addWidget(startup_label)

        layout.addLayout(bottom_row)

    # 🔘 Rend la carte cliquable (Mock)
    def mousePressEvent(self, event):
        print("🖱️ Client selected (mock click)")
