import os
import datetime
from core.env import LOGS_DIR

from core.labels import Label

class LogManager:
    def __init__(self, manager):
        self.manager = manager
        self.tr = self.manager.locales.tr
        pass

    def get_global_log_path(self):
        """ 🔗 Retourne le chemin du fichier log global """
        return os.path.join(LOGS_DIR, "vpn-manager.log")

    def get_log_path(self, client_name):
        """ 🔗 Retourne le chemin du fichier log pour un VPN spécifique """
        return os.path.join(LOGS_DIR, f"{client_name}.log")

    def write(self, global_message:str|Label|None=None, client_name:str|None=None, client_message:str|Label|None=None):
        """ 📌 Ajoute une entrée dans les logs (globale + client si applicable) """
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        
        # 🔥 Log globale
        if global_message:
            global_log_entry = f"{timestamp} {self.tr(global_message)}\n"
            global_log_path = self.get_global_log_path()
            with open(global_log_path, "a") as global_log:
                global_log.write(global_log_entry)
            # Affiche aussi sur stdout pour les exécutions depuis le terminal
            print(f"{global_log_entry}".strip())

            self.manager.states.emit_global_log_update(global_log_entry)  # 🛰️ Signal global
        
        # 🔥 Log spécifique au client
        if client_name and client_message:
            client_log_entry = f"{timestamp} {self.tr(client_message)}\n"
            client_log_path = self.get_log_path(client_name)
            with open(client_log_path, "a") as client_log:
                client_log.write(client_log_entry)
            # Affiche aussi sur stdout pour les exécutions depuis le terminal
            print(f"{client_log_entry}".strip())

            self.manager.states.emit_client_log_update(client_log_entry, client_name)  # 🛰️ Signal client

    def read(self, client_name=None):
        if not client_name:
            """ 📖 Lit les logs du manager et retourne les dernières lignes """
            log_path = self.get_global_log_path()
        else:
            """ 📖 Lit les logs du VPN et retourne les dernières lignes """
            log_path = self.get_log_path(client_name)
        if os.path.exists(log_path):
            with open(log_path, "r") as log_file:
                return log_file.readlines()
        return []

    def delete_logs(self, client_name=None):
        if not client_name:
            """ 🗑 Supprime le contenu des logs du manager """
            log_path = self.get_global_log_path()
        else:
            """ 🗑 Supprime le contenu des logs d’un VPN """
            log_path = self.get_log_path(client_name)
        if os.path.exists(log_path):
            open(log_path, "w").close()
