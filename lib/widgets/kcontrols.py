from PySide6.QtWidgets import QHBoxLayout
from widgets.kwidgets import KWidget, KButton
from core.actions import KThemeModeAction
from core.manager import themer

class KThemeModeToggler(KWidget):
    """ 🎨 Boutons pour basculer entre les thèmes (System / Light / Dark) """
    def __init__(self):
        super().__init__()

        # 📌 Layout horizontal pour aligner les boutons
        self._layout = QHBoxLayout()
        
        self.setLayout(self._layout)

        # 📌 Modes de thème disponibles
        self.modes = ["system", "light", "dark"]
        self.buttons = {}

        # 📌 Chargement du mode actuel depuis la config
        self.current_mode = themer.current_mode

        # 📌 Création des boutons de sélection
        for mode in self.modes:
            btn = KButton()
            btn.setDefaultAction(KThemeModeAction(btn, mode))
            btn.setFixedWidth(96)
            self.buttons[mode] = btn
            self._layout.addWidget(btn)