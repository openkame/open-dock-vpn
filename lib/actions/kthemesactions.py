from core.actions import KAction
from core.manager import themer, states
from core.labels import Label

class KThemeModeAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent, mode: str):
        self.mode = mode
        enum_key = f"THEMES_{self.mode.upper()}"
        label = Label[enum_key]  # Enum lookup via string
        super().__init__(parent, label)
        
        self.triggered.connect(self._on_triggered)
        states.theme_mode_updated.connect(self._on_theme_updated)

        self._on_theme_updated(themer.current_mode)  # état initial
    def _on_triggered(self):
        if self.isEnabled():
            states.emit_theme_mode_update(self.mode)

    def _on_theme_updated(self, current_mode):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        self.setDisabled(current_mode == self.mode)

class KThemeAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent, theme: str):
        self.theme = theme
        super().__init__(parent, theme)
        
        self.triggered.connect(self._on_triggered)
        states.theme_updated.connect(self._on_theme_updated)

        self._on_theme_updated(themer.current_theme)  # état initial
    def _on_triggered(self):
        if self.isEnabled():
            states.emit_theme_update(self.theme)

    def _on_theme_updated(self, current_theme):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        self.setDisabled(current_theme == self.theme)

