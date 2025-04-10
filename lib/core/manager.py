from core.locales_manager import LocalesManager
from core.config_manager import ConfigManager
from core.log_manager import LogManager
from core.file_manager import FileManager
from core.state_manager import StateManager
from core.theme_manager import ThemeManager

class KManager:
    """🧠 Point central d’accès à tous les managers"""
    def __init__(self):
        # 📌 Singleton pour toute l’application
        self.states = StateManager(self)
        self.locales = LocalesManager(self)
        self.logger = LogManager(self)
        self.config = ConfigManager(self)
        self.files = FileManager(self)
        # 🌍 Instance unique du ThemeManager
        self.themes = ThemeManager(self)

    def initialize(self):
        self.config.initialize()
        self.locales.initialize()
        
        self.files.verify_structure()
        self.themes.initialize()


# Singletons Globaux d'accès aux managers
manager = KManager()
states = manager.states
logger = manager.logger
locales = manager.locales
config = manager.config
themer = manager.themes
tr = locales.tr