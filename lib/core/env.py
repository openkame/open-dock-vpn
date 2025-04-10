import os

# 🌍 Langue dans laquelle l'application est développée
APP_DEFAULT_LOCALE="fr"
# Theme par défaut de l'application
APP_DEFAULT_THEME="default"
# Style par défaut 
APP_DEFAULT_STYLE="default"
LAYOUT_DEFAULT_STYLE="default_layout"

# Drapeau et langues disponibles (pas forcément de traduction juste en menu, ensuite faut faire les fichier <lang_code>.json)
COUNTRY_FLAGS = {
    "fr": "🇫🇷", "en": "🇬🇧", "de": "🇩🇪", "es": "🇪🇸", "it": "🇮🇹",
    "pt": "🇵🇹", "ru": "🇷🇺", "cn": "🇨🇳", "jp": "🇯🇵"
}
LANG_NAMES = {
    "fr": "Français", "en": "English", "de": "Deutsch", "es": "Español",
    "it": "Italiano", "pt": "Português", "ru": "Русский", "cn": "中文", "jp": "日本語"
}

# 📌 Trouver automatiquement le répertoire racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 📂 Chemins des dossiers principaux
LIB_DIR = os.path.join(BASE_DIR, "lib")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONFIG_FILENAME = "config.json"
LOCALES_DIR = os.path.join(CONFIG_DIR, "locales")
THEMES_DIR = os.path.join(CONFIG_DIR, "themes")
TEMPLATES_DIR = os.path.join(CONFIG_DIR, "templates")
ICONS_DIR = os.path.join(CONFIG_DIR, "icons")

LOGS_DIR = os.path.join(BASE_DIR, "logs")

SHARED_DIR = os.path.join(BASE_DIR, "shared")
CLIENTS_DIR = os.path.join(SHARED_DIR, "clients")
HOMES_DIR = os.path.join(SHARED_DIR, "home")
SKEL_NAME = "skel"
SKEL_DIR = os.path.join(SHARED_DIR, SKEL_NAME)

GLOBAL_CONFIG_FILE= os.path.join(CONFIG_DIR, "config.json")
GLOBAL_CONFIG_INITCONTENT = "{}"

APP_ICON_PATH = os.path.join(ICONS_DIR, "vpn-manager.png")
FAVORITE_ICON_PATH = os.path.join(ICONS_DIR, "star-filled.png")
NO_FAVORITE_ICON_PATH = os.path.join(ICONS_DIR, "star-outline.png")

# 🔥 Export des constantes pour usage global
__all__ = [
    "BASE_DIR", "LIB_DIR", "TEMPLATES_DIR", "ICONS_DIR", "LOGS_DIR",
    "SHARED_DIR", "CLIENTS_DIR", "HOMES_DIR", "SKEL_NAME", "SKEL_DIR",
    "GLOBAL_CONFIG_FILE" "TRAY_ICON_PATH"
]
