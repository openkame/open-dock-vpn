import json
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from core.env import THEMES_DIR, APP_DEFAULT_THEME

from core.configs import GlobalConfig


class ThemeManager:
    """ 🎨 Gestionnaire des thèmes """
    def __init__(self, manager):
        self.manager = manager
        self.config = self.manager.config
        self.states = self.manager.states
        self.current_theme = None
        self.current_mode = None
        self.modes = None
        self.themes = None
        self.theme_data = None
    
    def initialize(self):
        if not self.config.hasValue(GlobalConfig.THEME_NAME):
            self.config.setValue(GlobalConfig.THEME_NAME, "default")
        self.current_theme = self.config.getValue(GlobalConfig.THEME_NAME)

        if not self.config.hasValue(GlobalConfig.THEME_MODE):
            self.config.setValue(GlobalConfig.THEME_MODE, "light")
        self.current_mode = self.config.getValue(GlobalConfig.THEME_MODE)
        
        self.themes = self.load_available_themes()
        self.theme_data = self.load_theme()
        # 📡 Écoute des signaux
        self.states.theme_mode_updated.connect(self.change_mode)
        self.states.theme_updated.connect(self.change_theme)

    def load_available_themes(self):
        """ 📂 Charge la liste des thèmes disponibles """
        return [f.replace(".json", "") for f in os.listdir(THEMES_DIR) if f.endswith(".json")]

    def change_mode(self, mode):
        """ 🔄 Change uniquement le mode (System/Light/Dark) """
        self.current_mode = mode
        self.load_theme()
    
    def change_theme(self, theme):
        self.current_theme = theme
        self.load_theme()

    def load_theme(self, mode=None, theme_name=None):
        """ 📖 Charge un thème et applique le mode clair/sombre """
        if theme_name:
            self.current_theme = theme_name
        else:
            theme_name = self.current_theme

        theme_path = os.path.join(THEMES_DIR, f"{theme_name}.json")

        if not os.path.exists(theme_path):
            theme_name = APP_DEFAULT_THEME
            theme_path = os.path.join(THEMES_DIR, f"{theme_name}.json")

        # 🔄 Vérifie le mode du système
        if mode is None:
            mode = self.current_mode
        if mode == "system":
            mode = "dark" if self.is_system_dark() else "light"

        with open(theme_path, "r", encoding="utf-8") as f:
            theme_data = json.load(f)

        self.current_mode = mode
        self.theme_data = theme_data.get(mode, theme_data)

        # 💾 Sauvegarde dans la config globale
        if theme_name != self.config.getValue(GlobalConfig.THEME_NAME): self.config.setValue(GlobalConfig.THEME_NAME, theme_name)
        if mode != self.config.getValue(GlobalConfig.THEME_MODE): self.config.setValue(GlobalConfig.THEME_MODE, mode)
    
    def is_system_dark(self):
        """ 🌍 Vérifie si le système est en mode sombre via QPalette """
        app = QApplication.instance()
        if not app:
            return False  # ⚠️ Si pas d'instance QApplication, retourne False par défaut

        palette = app.palette()
        text_color = palette.color(QPalette.WindowText).lightness()
        return text_color > 128  # 🌙 Si la couleur du texte est plus claire que la moyenne, on est en dark mode

    def get_style(self, style_name: str, widget_name: str) -> str:
        """ 🎨 Génère la feuille de style complète pour un widget donné """
        qss_blocks = []
        base_props = []
        extra_blocks = []   

        if not self.theme_data:
            self.load_theme()        

        # 🧱 Partie principale (clé exacte = style_name)
        style_data = self.theme_data.get(style_name, {})
        for key, value in style_data.items():
            # 1️⃣ Propriétés directes (background-color, font-size, etc)
            if not isinstance(value, dict):
                base_props.append(f"{key}: {value};")
            else:
                # 2️⃣ Sous-composants internes (QTabBar, QScrollBar::handle, etc)
                selector = key
                props = [f"{prop}: {val};" for prop, val in value.items()]
                block = f"{selector} {'{'}\n{'\n'.join(props)}\n{'}'}"
                extra_blocks.append(block)

        # ➕ Partie 2 : pseudo-classes (à la racine, ex: "tabber:hover", "tabber::handle:pressed")
        for key, value in self.theme_data.items():
            if key.startswith(f"{style_name}:") or key.startswith(f"{style_name}::"):
                suffix = key[len(style_name):]  # Extrait ":hover", "::handle:pressed", etc
                selector = f"{widget_name}{suffix}"
                props = [f"{prop}: {val};" for prop, val in value.items()]
                block = f"{selector} {'{'}\n{'\n'.join(props)}\n{'}'}"
                extra_blocks.append(block)

        # 🧱 Bloc principal
        if base_props:
            qss_blocks.append(f"{widget_name} {'{'}\n{'\n'.join(base_props)}\n{'}'}")

        # ➕ Ajout des blocs supplémentaires
        qss_blocks.extend(extra_blocks)
        return "\n\n".join(qss_blocks)

