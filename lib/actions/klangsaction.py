from core.actions import KAction
from core.manager import locales, states

class KLangsAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent, code: str, lang: str):
        self.code = code 
        self.lang = lang
        super().__init__(parent, self.lang)
        
        self.triggered.connect(self._on_triggered)
        states.lang_updated.connect(self._on_lang_updated)
        self._on_lang_updated()  # état initial

    def _on_triggered(self):
        if self.isEnabled():
            locales.current_locale = self.code
            states.emit_lang_update()

    def _on_lang_updated(self):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        self.setDisabled(locales.current_locale == self.code)