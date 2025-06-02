import os
import json
from core.env import APP_DEFAULT_LOCALE, LOCALES_DIR, COUNTRY_FLAGS, LANG_NAMES

from core.labels import Label
from core.configs import GlobalConfig

class LocalesManager:
    """ 📜 Gestionnaire des traductions """

    def __init__(self, manager):
        self.manager = manager
        self.states = manager.states
        self.current_locale = None
        self.languages = None
        self.translations = {}

    def initialize(self):
        self.languages = self.get_available_languages()
        self.current_locale = self.load_saved_language()
        self.load_locale(self.current_locale)
        self.states.lang_updated.connect(self.update_locale)

    def update_locale(self):
        self.load_locale(self.current_locale)


    def load_locale(self, lang_code):
        """ 💾 Charge la langue spécifiée depuis le fichier JSON """
        file_path = os.path.join(LOCALES_DIR, f"{lang_code}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            self.current_locale = lang_code
            self.save_selected_language(lang_code)
        else:
            print(f"⚠️ Langue non trouvée : {lang_code}, fallback en {APP_DEFAULT_LOCALE}")
            self.load_locale(APP_DEFAULT_LOCALE)

    def get_available_languages(self):
        """🌍 Récupère dynamiquement les langues disponibles à partir des fichiers de traduction"""
        languages = {}

        for file in os.listdir(LOCALES_DIR):
            if file.endswith(".json"):
                lang_code = file[:-5]  # remove .json
                file_path = os.path.join(LOCALES_DIR, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = json.load(f)
                        if lang_code in content:
                            languages[lang_code] = content[lang_code]
                        else:
                            languages[lang_code] = f"🌍 {lang_code}"
                except Exception as e:
                    print(f"⚠️ Impossible de lire {file}: {e}")
        
        return languages

    # 💾 **Gestion de la langue enregistrée**
    def load_saved_language(self):
        """ 💾 Charge la langue enregistrée dans `config.json` """
        return self.manager.config.getValue(GlobalConfig.LANGUAGE)

    def save_selected_language(self, lang_code):
        """ 💾 Sauvegarde la langue sélectionnée dans `config.json` """
        if lang_code != self.manager.config.getValue(GlobalConfig.LANGUAGE):
            self.manager.config.setValue(GlobalConfig.LANGUAGE, lang_code)
    
    def tr(self, text: str | Label | dict):
        r"""
        🔄 Return a translated string or the raw string itself for widgets
            If text=str
             - Return the string as it
            If text=core.labels.Label
             - Convert it to a translated string
            If text=dict
             - apply formatting
             - 'key' key is a core.labels.Label
             - All other keys are formatting keys for string.format() function
        """
        self._text = text # raw argument given named text for user friendly-reading purposes
        self._label = None # label enum name
        self._key = None # Key retrieved from a label
        self._format_args = None # args to format string inside a Label

        if isinstance(self._text, Label):
            self._label = self._text
        elif isinstance(self._text, str):
            return str(self._text)
        elif isinstance(self._text, dict):
            self._label, self._format_args = self._extract_tr_args(self._text)
            if(not isinstance(self._label, Label)):
                return "❌ INVALID DICT ROOT KEY (must be a core.labels.Label)"
        else:
            return "❌ INVALID KEY TYPE (must be str, dict or core.labels.Label)"
        # Assign label value as key to self._key (we are now sure we're working on a label )
        self._key = self._label.value

        # Retrieve translation from key (e.g. "log.ui_main_message")
        translation = self._get_translation(self._key)
        try:
            return translation.format(**self._format_args) if self._format_args else translation
        except Exception as e:
            return f"❌ FORMAT ERROR in '{self._key}': {e}"

    
    def _extract_tr_args(self, data: dict | None) -> tuple[str, dict]:
        """Retourne une clé de traduction + kwargs pour tr() si c'est un dict qui est passé en arg à tr."""
        if not data or not isinstance(data, dict):
            return "", {}
        key = data.get("key", "")
        args = {k: v for k, v in data.items() if k != "key"}
        return key, args
    
    def _get_translation(self, full_key: str) -> str:
        try:
            root_key, leaf_key = full_key.split(".", 1)
            return self.translations[root_key][leaf_key]
        except (KeyError, TypeError, ValueError):
            return full_key
    
    def reload_ui(self):
        print("to dev")
