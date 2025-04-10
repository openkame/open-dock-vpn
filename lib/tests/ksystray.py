from PySide6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QWidget
)
from PySide6.QtGui import QIcon, QAction


class SystemTrayMock(QSystemTrayIcon):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        # 🖼️ Icône personnalisée (à placer à la racine du projet mock)
        self.setIcon(QIcon("vpn-manager.png"))
        self.setToolTip("VPN Manager running\nNbClients: 2")

        # 📋 Menu principal
        tray_menu = QMenu(parent)

        # 📁 Clients
        clients_menu = tray_menu.addMenu("Clients")
        clients_menu.addAction("Start Client 1")
        clients_menu.addAction("Stop Client 1")
        clients_menu.addSeparator()
        clients_menu.addAction("Start Client 2")
        clients_menu.addAction("Stop Client 2")

        # 🎨 Themes
        themes_menu = tray_menu.addMenu("Themes")
        for theme in ["default", "blue", "dark"]:
            action = QAction(theme, self)
            themes_menu.addAction(action)

        # 🌗 Theme Mode
        mode_menu = tray_menu.addMenu("Theme Mode")
        mode_system = QAction("🖥️ System", self)
        mode_light = QAction("🌞 Light", self)
        mode_dark = QAction("🌙 Dark", self)
        mode_system.setDisabled(True)  # Exemple : mode actuel grisé

        mode_menu.addAction(mode_system)
        mode_menu.addAction(mode_light)
        mode_menu.addAction(mode_dark)

        tray_menu.addSeparator()
        quit_action = QAction("❌ Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.setContextMenu(tray_menu)
        self.show()

        # 🪄 Infobulle de dernière action mockée
        self.showMessage("VPN Manager", "✅ Last action: Client 1 started", QSystemTrayIcon.Information, 3000)
