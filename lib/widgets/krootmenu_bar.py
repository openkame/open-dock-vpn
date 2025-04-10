from PySide6.QtWidgets import QWidgetAction, QSizePolicy
from widgets.kwidgets import KWidget, KMenuBar, KMenu, KLabel
from core.actions import (
    KAction, KOpenLogConsoleAction, KOpenAddClientAction,
    KOpenProfilesManagerAction, KToggleTooltipsAction,
    KLangsAction, KThemeModeAction, KThemeAction,
    KQuitAppAction, KSwitchViewAction
)
from core.manager import locales, themer

from core.labels import Label

class KRootMenuBar(KMenuBar):
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self.setThemeStyle("menu_bar")

        self.title_label = KLabel(Label.UI_MAIN_APP_TITLE)

        # ───── Clients menu
        self.addclient_open = KOpenAddClientAction(self)
        self.manageprofiles_open = KOpenProfilesManagerAction(self)
        self.consolelogs_open = KOpenLogConsoleAction(self)
        self.app_quit = KQuitAppAction(self)

        menu_clients = KMenu(self, Label.UI_MAIN_LABEL_CLIENTS_NAME)
        menu_clients.setThemeStyle("menu_bar")
        
        menu_clients.addAction(self.addclient_open)
        menu_clients.addAction(self.manageprofiles_open)
        menu_clients.addAction(self.consolelogs_open)
        menu_clients.addSeparator()
        menu_clients.addAction(self.app_quit)
        self.addMenu(menu_clients)

        # ───── Settings menu
        menu_settings = KMenu(self, Label.UI_MAIN_LABEL_SETTINGS_NAME)
        menu_settings.setThemeStyle("menu_bar")

        # Theme Mode dynamique (remplace le bouton par un menu 🌗)
        self.theme_mode_menu = KMenu(self, Label.UI_MAIN_LABEL_THEME_MODE)  # 🔁 Clé existante conservée 
        self.theme_mode_menu.setThemeStyle("menu_bar") 
        self.add_theme_mode_items()
        menu_settings.addMenu(self.theme_mode_menu)

        # Thèmes dynamiques
        self.theme_menu = KMenu(self, Label.UI_MAIN_LABEL_THEME_SELECTOR)
        self.theme_menu.setThemeStyle("menu_bar") 
        self.add_theme_items()
        menu_settings.addMenu(self.theme_menu)

        # Langues dynamiques
        self.lang_menu = KMenu(self, Label.UI_MAIN_LABEL_LANG_SELECTOR)
        self.lang_menu.setThemeStyle("menu_bar") 
        self.add_language_items()
        menu_settings.addMenu(self.lang_menu)

        # Toggle Tooltips
        self.tooltips_toggle_action = KToggleTooltipsAction(self)
        menu_settings.addAction(self.tooltips_toggle_action)

        self.addMenu(menu_settings)

        # ajouter un spacer ici
        self.add_spacer_to_menubar()

        # Boutons de contrôles (switch/hide)
        # 🔁 Switch view button (compact/full)
        self.switchview = KSwitchViewAction(self)
        self.addAction(self.switchview)
        self.hideview = KAction(self, "➖")
        self.hideview.triggered.connect(self._parent.hide)
        self.addAction(self.hideview)

    def add_spacer_to_menubar(self):
        spacer_action = QWidgetAction(self)

        spacer = KWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        spacer_action.setDefaultWidget(spacer)
        
        self.addAction(spacer_action)  # self est la QMenuBar ici

    def add_theme_mode_items(self):
        self.theme_mode_menu.clear()
        modes = ["system", "light", "dark"]
        for mode in modes:
            action = KThemeModeAction(self, mode)
            self.theme_mode_menu.addAction(action)

    def add_theme_items(self):
        self.theme_menu.clear()
        for theme in themer.themes:
            action = KThemeAction(self, theme)
            self.theme_menu.addAction(action)

    def add_language_items(self):
        self.lang_menu.clear()

        for code, label in locales.languages.items():
            action = KLangsAction(self, code, label)
            self.lang_menu.addAction(action)

