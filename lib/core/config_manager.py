import os
import json
from core.env import CONFIG_FILENAME, CLIENTS_DIR, TEMPLATES_DIR, GLOBAL_CONFIG_FILE
from core.configs import GlobalConfig, ClientConfig, ConfigPath
from core.labels import Label

class ConfigManager:
    def __init__(self, manager):
        self.manager = manager
        self._global_config = None
        self._clients_configs = {}
        self._active_client = None

    def initialize(self):
        self._load_configs()
        
    def _load_configs(self):
        self._global_config = self._load_json_file(GLOBAL_CONFIG_FILE)
        if os.path.exists(CLIENTS_DIR):
            for client_name in os.listdir(CLIENTS_DIR):
                config_path = self._get_client_config_path(client_name)
                if os.path.exists(config_path):
                    self._clients_configs[client_name] = self._load_json_file(config_path)
    
    # 🔗 Configuration spécifique à un client
    def _get_client_config_path(self, client_name):
        """ 📍 Retourne le chemin du `config.json` local d'un client """
        return os.path.join(CLIENTS_DIR, client_name, CONFIG_FILENAME)
    
    def _save_global_config(self):
        """ 💾 Sauvegarde `config.json` global """
        self._save_json_file(GLOBAL_CONFIG_FILE, self._global_config)

    def _save_client_config(self, client_name):
        """ 💾 Sauvegarde `config.json` d'un client VPN """
        self._save_json_file(self._get_client_config_path(client_name), self._clients_configs[client_name])

    # set les informations clients quand un est activé
    def setActiveClient(self, client_name):
        self._active_client = client_name
        # states.emit_active_client_updated(client_name)  # tu peux connecter ça dans FullView

    def getActiveClient(self): 
        return self._active_client
    
    def unsetActiveClient(self):
        self._active_client = None
        # faire un emit à None ça permettra de réafficher le widget de remplacement quand rien n'est sélectionné
        # states.emit_active_client_updated(None)  # tu peux connecter ça dans FullView
    
    def isActiveClientSet(self):
        if self._active_client:
            return True
        else:
            return False
    
    def getValue(self, path_enum: GlobalConfig | ClientConfig | ConfigPath, client_name: str | None = None):
        if isinstance(path_enum, ConfigPath):
            is_global = path_enum.enum is GlobalConfig
            target_config = self._global_config if is_global else self._clients_configs.get(client_name)
            path = path_enum.path
        elif isinstance(path_enum, (GlobalConfig, ClientConfig)):
            is_global = isinstance(path_enum, GlobalConfig)
            target_config = self._global_config if is_global else self._clients_configs.get(client_name)
            path = path_enum.value
        else:
            raise TypeError("Invalid path type for getValue()")

        if target_config is None:
            return None

        data = target_config
        for key in path:
            data = data.get(key)
            if data is None:
                return None
        return data
    
    def hasValue(self, path_enum: GlobalConfig | ClientConfig | ConfigPath, client_name: str | None = None) -> bool:
        value = self.getValue(path_enum, client_name=client_name)
        return value is not None
    
    def addValue(self, path_enum: GlobalConfig | ClientConfig | ConfigPath, client_name: str | None = None):
        """➕ Ajoute une valeur vide (dict) seulement si elle n'existe pas encore"""
        if not self.hasValue(path_enum, client_name):
            self.setValue(path_enum, value={}, client_name=client_name)

    def setValue(self, path_enum: GlobalConfig | ClientConfig | ConfigPath, value, client_name: str | None = None):
        # 🔍 Détermine la config cible
        if isinstance(path_enum, ConfigPath):
            is_global = path_enum.enum is GlobalConfig
            target_config = self._global_config if is_global else self._clients_configs.get(client_name)
            path = path_enum.path
        elif isinstance(path_enum, (GlobalConfig, ClientConfig)):
            is_global = isinstance(path_enum, GlobalConfig)
            target_config = self._global_config if is_global else self._clients_configs.get(client_name)
            path = path_enum.value
        else:
            raise TypeError("Invalid path type for setValue()")

        # ⚠️ Vérif si on a bien une config valide
        if target_config is None:
            raise ValueError("No configuration available for this path. Maybe missing client_name?")

        # 🛠 Traverse & update la config
        data = target_config
        path = tuple(path)  # ✅ force la conversion (même si c'était déjà un tuple, pas de souci)
        for key in path[:-1]:
            data = data.setdefault(key, {})
        data[path[-1]] = value

        # 💾 Sauvegarde automatique
        if is_global:
            self._save_global_config()
        elif client_name:
            self._save_client_config(client_name)

    def deleteValue(self, path_enum: GlobalConfig | ClientConfig | ConfigPath, client_name: str | None = None):
        # Détermination de la config et du chemin
        if isinstance(path_enum, ConfigPath):
            is_global = path_enum.enum is GlobalConfig
            target_config = self._global_config if is_global else self._clients_configs.get(client_name)
            path = path_enum.path
        elif isinstance(path_enum, (GlobalConfig, ClientConfig)):
            is_global = isinstance(path_enum, GlobalConfig)
            target_config = self._global_config if is_global else self._clients_configs.get(client_name)
            path = path_enum.value
        else:
            raise TypeError("Invalid path type for deleteValue()")

        if target_config is None:
            raise ValueError("No configuration available for this path. Maybe missing client_name?")

        # Suppression de la clé
        data = target_config
        path = tuple(path)  # ✅ force la conversion (même si c'était déjà un tuple, pas de souci)
        for key in path[:-1]:
            data = data.get(key)
            if not isinstance(data, dict):
                return  # Clé intermédiaire manquante, rien à supprimer
        data.pop(path[-1], None)  # Ne lève pas d'erreur si la clé finale n'existe pas

        # Sauvegarde après suppression
        if is_global:
            self._save_global_config()
        elif client_name:
            self._save_client_config(client_name)

    def createClientConfig(self, client_name: str, initial_config: dict):
        """🆕 Crée un nouveau client VPN avec sa configuration initiale"""
        if client_name in self._clients_configs:
            raise ValueError(f"Client '{client_name}' already exists.")

        if "@" not in client_name or "." not in client_name.split("@")[1]:
            raise ValueError(f"Invalid client_name format: '{client_name}' (expected user@vpn.domain)")

        # 1. Ajoute à la mémoire le client et sauvegarde le fichier
        self._clients_configs[client_name] = initial_config
        self._save_client_config(client_name)

        # 2. Ajoute au global config
        self.addValue(GlobalConfig.CLIENTS, client_name)
        self.setValue(GlobalConfig.CLIENT_USER(client_id=client_name), client_name.split("@")[0])
        self.setValue(GlobalConfig.CLIENT_VPN(client_id=client_name), client_name.split("@")[1].split(".")[0])
        self.setValue(GlobalConfig.CLIENT_DOMAIN(client_id=client_name), client_name.split("@")[1].split(".")[1])
        self.setValue(GlobalConfig.CLIENT_FAVORITE(client_id=client_name), False)
        self.setValue(GlobalConfig.CLIENT_ERROR(client_id=client_name), False)

    def deleteClientConfig(self, client_name: str):
        """🗑 Supprime un client VPN et sa configuration"""
        # 1. Retire de la mémoire
        self._clients_configs.pop(client_name, None)
        # 2. Supprime le fichier sur le disque
        config_path = self._get_client_config_path(client_name)
        if os.path.exists(config_path):
            os.remove(config_path)

        # 2. Retire du global config
        if self.hasValue(GlobalConfig.CLIENT(client_id=client_name)):
            self.deleteValue(GlobalConfig.CLIENT(client_id=client_name))
        
        if self._active_client == client_name:
            self.unsetActiveClient()

    ## JSON Files operations
    def _load_json_file(self, path):
        """ 📂 Charge un fichier JSON si disponible, sinon retourne un objet vide """
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                self.manager.logger.write(Label.LOG_JSON_READ_ERROR(path=path))
        return {}  # Fichier inexistant ou invalide
    
    def _save_json_file(self, path, data):
        """ 💾 Sauvegarde des données dans un fichier JSON """
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    
    # 🔍 Vérification et mise à jour des clients
    def verify_clients(self):
        """ 🔍 Vérifie la cohérence entre les clients présents sur le disque et `config.json` global """

        if self.getValue(GlobalConfig.CLIENTS) == None:
            self.setValue(GlobalConfig.CLIENTS, {})

        existing_clients = set(os.listdir(CLIENTS_DIR))  # 📌 Liste des dossiers clients

        # ✅ Vérification des clients connus
        for client_name in list(self._global_config["clients"]):
            client_path = self._get_client_config_path(client_name)
            if not os.path.exists(client_path):  # ❌ Dossier client supprimé ?
                self.manager.logger.write(Label.LOG_CLIENT_NOT_FOUND(client_name=client_name))
                self.deleteValue(GlobalConfig.CLIENT(client_id=client_name))
            else:
                if not self._clients_configs[client_name]:
                    self.manager.logger.write(Label.LOG_CONFIG_MISSING(client_name=client_name))
                    self.setValue(GlobalConfig.CLIENT_ERROR(client_id=client_name), True)

                else:
                    self.setValue(GlobalConfig.CLIENT_ERROR(client_id=client_name), False)


        # 🆕 Ajout des clients non répertoriés
        for client_name in existing_clients:
            if client_name and not self.hasValue(GlobalConfig.CLIENT(client_id=client_name)):
                if self._clients_configs[client_name]:  # ✅ Un `config.json` valide existe ?
                    self.manager.logger.write(Label.LOG_CLIENT_ADDING(client_name=client_name))
                    self.addValue(GlobalConfig.CLIENTS,client_name)
                    self.setValue(GlobalConfig.CLIENT_USER(client_id=client_name), client_name.split("@")[0])
                    self.setValue(GlobalConfig.CLIENT_VPN(client_id=client_name), client_name.split("@")[1].split(".")[0])
                    self.setValue(GlobalConfig.CLIENT_DOMAIN(client_id=client_name), client_name.split("@")[1].split(".")[1])
                    self.setValue(GlobalConfig.CLIENT_FAVORITE(client_id=client_name), False)
                    self.setValue(GlobalConfig.CLIENT_ERROR(client_id=client_name), False)

                else:
                    self.manager.logger.write(Label.LOG_CONFIG_IGNORED(client_name=client_name))

    def verify_profiles(self):
        """ 🔍 Vérifie que les profils VPN dans `config.json` sont valides et corrige si besoin """
        if self.getValue(GlobalConfig.PROFILES) == None:
            self.setValue(GlobalConfig.PROFILES, {})
        for profile_name in self._global_config["profiles"]:
            profile_path = os.path.join(TEMPLATES_DIR, profile_name)

            # 📌 Vérifier si le dossier du profil existe
            if not os.path.exists(profile_path):
                self.manager.logger.write(Label.LOG_PROFILE_MISSING(profile_name=profile_name))
                self.setValue(GlobalConfig.PROFILE_ERROR(profile_id=profile_name), True)
            else:
                self.setValue(GlobalConfig.PROFILE_ERROR(profile_id=profile_name), False)

