from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtGui import QIcon

from core.env import APP_ICON_PATH
from widgets.kwidgets import KMenu, KSystemTray
from core.actions import KLangsAction, KThemeModeAction, KThemeAction, KQuitAppAction
from core.manager import locales, themer

from core.labels import Label

class KRootSystemTray(KSystemTray):
    def __init__(self, parent):
        KSystemTray.__init__(self, parent)
        self._parent=parent

        # 🖼️ Icône personnalisée (à placer à la racine du projet mock)
        self.setIcon(QIcon(APP_ICON_PATH))
        self.setToolTip("VPN Manager running\nNbClients: 2")

        # 📋 Menu principal
        tray_menu = KMenu(self._parent)

        # 📁 Clients
        menu_clients = KMenu(self._parent, Label.UI_MAIN_LABEL_CLIENTS_NAME)
        tray_menu.addMenu(menu_clients)

        # TODO create client list and add actions for it with a loop on them
        menu_clients.addAction("Start Client 1")
        menu_clients.addAction("Stop Client 1")
        menu_clients.addSeparator()
        menu_clients.addAction("Start Client 2")
        menu_clients.addAction("Stop Client 2")

        tray_menu.addSeparator()

        # 🌍 Languages
        langs_menu = KMenu(self._parent, Label.UI_MAIN_LABEL_LANG_SELECTOR)
        tray_menu.addMenu(langs_menu)       
        for code, lang in locales.languages.items():
            action = KLangsAction(self, code, lang)
            langs_menu.addAction(action)

        # 🎨 Themes
        themes_menu = KMenu(self._parent, Label.UI_MAIN_LABEL_THEME_SELECTOR)
        tray_menu.addMenu(themes_menu)
        for theme in themer.themes:
            action = KThemeAction(self, theme)
            themes_menu.addAction(action)

        # 🌗 Theme Mode
        mode_menu = KMenu(self._parent, Label.UI_MAIN_LABEL_THEME_MODE)
        tray_menu.addMenu(mode_menu)
        modes = ["system", "light", "dark"]
        for mode in modes:
            action = KThemeModeAction(self, mode)
            mode_menu.addAction(action)

        tray_menu.addSeparator()
        quit_action = KQuitAppAction(self)
        tray_menu.addAction(quit_action)

        self.setContextMenu(tray_menu)
        self.show()

        # 📌 Affiche la fenêtre sur clic gauche
        self.activated.connect(self.on_tray_icon_click)

        # 🪄 Infobulle de dernière action mockée
        self.showMessage("VPN Manager", "✅ Last action: Client 1 started", QSystemTrayIcon.Information, 3000)
    
    def on_tray_icon_click(self, reason):
        """ 📌 Réaffiche la fenêtre si elle est cachée """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Clic gauche
            if self._parent.isHidden():
                self._parent.showNormal()
                self._parent.activateWindow()
