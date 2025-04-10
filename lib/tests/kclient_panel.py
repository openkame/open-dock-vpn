from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt


class KClientPanelMock(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # ──────────── Title + Status (Nom du client + emoji statut)
        title_layout = QHBoxLayout()
        title_label = QLabel("🧅 VPN - client-dev")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        title_layout.addWidget(title_label)

        status_label = QLabel("🟢")  # État actuel
        title_layout.addWidget(status_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # ──────────── Toggle Autostart + profil VPN utilisé
        toggles_layout = QHBoxLayout()
        autostart_toggle = QCheckBox("Autostart")
        toggles_layout.addWidget(autostart_toggle)

        vpn_profile_label = QLabel("🔧 Profile: dev-default")
        vpn_profile_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        toggles_layout.addWidget(vpn_profile_label)
        layout.addLayout(toggles_layout)

        # ──────────── Dernière action + Démarré le
        layout.addWidget(QLabel("📦 Last Action: Start VPN"))
        layout.addWidget(QLabel("📅 Started at: 2025-03-23 14:21"))

        # ──────────── Actions principales (Start / Stop / Refresh VPN)
        main_actions = QHBoxLayout()
        btn_start = QPushButton("▶️")
        btn_stop = QPushButton("⏹")
        btn_refresh = QPushButton("🔁")
        for btn in (btn_start, btn_stop, btn_refresh):
            btn.setFixedWidth(40)
            main_actions.addWidget(btn)
        layout.addLayout(main_actions)

        # ──────────── Quick actions (Terminal / Browser)
        quick_actions = QHBoxLayout()
        btn_terminal = QPushButton("🖥️ Terminal")
        btn_browser = QPushButton("🌍 Browser")
        quick_actions.addWidget(btn_terminal)
        quick_actions.addWidget(btn_browser)
        layout.addLayout(quick_actions)

        # ──────────── Delete button (Red, bottom-aligned)
        btn_delete = QPushButton("🗑️ Delete VPN")
        btn_delete.setStyleSheet("color: red; font-weight: bold;")
        btn_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addStretch()
        layout.addWidget(btn_delete)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = KClientPanelMock()
    win.setWindowTitle("Client Panel Mock")
    win.resize(350, 400)
    win.show()
    sys.exit(app.exec())
