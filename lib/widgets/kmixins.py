from core.manager import states, themer, tr
from core.labels import Label

class KThemeMixin:
    """ 🎨 Mixin pour appliquer dynamiquement un thème QSS """
    def __init__(self, style_name="default"):
        self._theme_applied = False
        self._last_applied_theme = None
        self._last_applied_mode = None
        self._style_name = style_name

        # 📡 Écoute les changements de thème
        states.theme_updated.connect(self._on_theme_updated)
        states.theme_mode_updated.connect(self._on_theme_updated)
        states.widget_shown.connect(self._on_widget_shown)
    
    def setThemeStyle(self, style_name):
        """ ⚙️ Permet de customiser un widget après initialisation """
        self._style_name = style_name
        
    def _on_widget_shown(self, widget):
        if widget is self and not self._theme_applied:
            self._apply_theme()

    def _on_theme_updated(self):
        if self._theme_applied and hasattr(self, "setStyleSheet"):
            if self.isVisible():
                self._apply_theme()
            else:
                self._theme_applied = False  # flag pour appliquer plus tard
        else:
            self._theme_applied = False
    
    
    def _apply_theme(self):
        """ 🎨 Applique le style si nécessaire """
        if not self._style_name:
            print(f"⚠️ style_name manquant dans {self.__class__.__name__}")
            return
        
        # check ici si on a chngé de theme ou de mode
        if self._last_applied_mode == themer.current_mode and self._last_applied_theme == themer.current_theme:
            #print(f"🛑 Pas de changement de style pour {self.__class__.__name__}, skip")
            return
        
        new_qss = themer.get_style(self._style_name, self.metaObject().className())
        
        self.setStyleSheet(new_qss)
        self._last_applied_mode = themer.current_mode
        self._last_applied_theme = themer.current_theme
        self._theme_applied = True
        #print(f"🎨 Style appliqué à {self.__class__.__name__}")

class KDynamicTextMixin:
    """🏗️ Mixin dynamique pour traductions (setText, setTitle, etc.)"""
    def __init__(self, text: Label | str | None = None, setter=None):
        self._setter = setter or self.setText  # fallback si oublié
        self._connected = False
        self._updateSelves(text)

    def updateText(self, new_text: Label | str | None = None):
        if new_text and (new_text != self._key):
            self._updateSelves(new_text)
        elif isinstance(self._key, Label):
            self._text = tr(self._key)
        self._setter(self._text)

    def _updateSelves(self, text):
        self._key = text
        self._text = tr(self._key)
        if isinstance(self._key, Label) and not self._connected:
            states.lang_updated.connect(self.updateText)
            self._connected = True
        elif not isinstance(self._key, Label) and self._connected:
            states.lang_updated.disconnect(self.updateText)
            self._connected = False

class KTextMixin(KDynamicTextMixin):
    """🏗️ Mixin pour appliquer dynamiquement des traductions ou du texte brut"""
    def __init__(self, text: str | Label | None = None):
        super().__init__(text, setter=self.setText)

class KWindowTitleMixin(KDynamicTextMixin):
    """ 🏗️ Mixin pour appliquer dynamiquement les traductions """
    def __init__(self, text: str | Label | None = None):
        super().__init__(text, setter=self.setWindowTitle)

class KStatusMixin(KDynamicTextMixin):
    """ 🏗️ Mixin pour appliquer dynamiquement les traductions """
    def __init__(self, text: str | Label | None = None):
        super().__init__(text, setter=self.showMessage)

class KTitleMixin(KDynamicTextMixin):
    """ 🏗️ Mixin pour appliquer dynamiquement les traductions """
    def __init__(self, text: str | Label | None = None):
        super().__init__(text, setter=self.setTitle)