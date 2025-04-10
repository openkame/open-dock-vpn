from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QMenuBar, QMenu, QStatusBar, 
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt

from kclients_list import KClientsFullList
from kclient_panel import KClientPanelMock
from lib.tests.ksystray import SystemTrayMock

from state_manager import state_manager


class FullView(QMainWindow):
    def __init__(self, parent=None):
        if parent:
            super().__init__(parent=parent)
        else:
            super().__init__()
        self.setWindowTitle("Full View (Mock)")

        # ❌ Désactive le redimensionnement
        self.setFixedSize(900, 600)

        

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ───────────── MenuBar
        menu_bar = QMenuBar()

        menu_clients = QMenu("Clients", self)
        menu_clients.addAction("➕ Add VPN")
        menu_clients.addAction("🧩 Manage Profiles")
        menu_clients.addAction("📄 Open Logs")
        menu_clients.addSeparator()
        menu_clients.addAction("❌ Quit")

        menu_settings = QMenu("Settings", self)
        menu_settings.addAction("🌗 Theme Mode")
        menu_settings.addAction("🎨 Change Theme")
        menu_settings.addAction("🌍 Change Language")
        menu_settings.addAction("📝 Toggle Tooltips")

        menu_bar.addMenu(menu_clients)
        menu_bar.addMenu(menu_settings)
        self.setMenuBar(menu_bar)

        # ───────────── Main layout
        clients_layout = QHBoxLayout()
        main_layout.addLayout(clients_layout)

        # Left section – client list + logs button
        clients_list_layout = QVBoxLayout()
        clients_layout.addLayout(clients_list_layout)

        self.clients_list = KClientsFullList()
        clients_list_layout.addWidget(self.clients_list)
        


        btn_logs = QPushButton("📄 Logs")
        clients_list_layout.addWidget(btn_logs)

        # Right section – toggles + client panel
        client_panel_layout = QVBoxLayout()
        clients_layout.addLayout(client_panel_layout)

        toggles_layout = QHBoxLayout()

        # ➖ Spacer pour décaler les boutons à droite
        toggles_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 🌗 Theme mode toggler (3 boutons emoji)
        btn_theme_system = QPushButton("🌓")
        btn_theme_light = QPushButton("☀️")
        btn_theme_dark = QPushButton("🌙")
        for btn in [btn_theme_system, btn_theme_light, btn_theme_dark]:
            btn.setFixedWidth(32)
            toggles_layout.addWidget(btn)

        # 🔁 Switch view button (compact/full)
        btn_switch_view = QPushButton("🔄")
        btn_switch_view.setFixedWidth(32)
        toggles_layout.addWidget(btn_switch_view)

        client_panel_layout.addLayout(toggles_layout)

        # 🧱 Placeholder client panel
        client_panel = KClientPanelMock()
        #client_panel.setAlignment(Qt.AlignCenter)
        client_panel_layout.addWidget(client_panel)

        # ───────────── StatusBar
        status_bar = QStatusBar()
        status_bar.showMessage("✔️ VPN Manager ready")
        self.setStatusBar(status_bar)

        btn_switch_view.clicked.connect(state_manager.emit_switch_view_request)  # 🔥 Trigger switch from full view

        self.systray = SystemTrayMock(self)


# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     win = FullView()
#     win.show()
#     sys.exit(app.exec())
