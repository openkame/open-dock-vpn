from core.env import \
    TEMPLATES_DIR, HOMES_DIR, \
    CLIENTS_DIR, SKEL_DIR, LOGS_DIR, \
    GLOBAL_CONFIG_FILE, GLOBAL_CONFIG_INITCONTENT
import os
import sys

from core.labels import Label

class FileManager:
    def __init__(self, manager):
        self.manager = manager
        self.logger = self.manager.logger
        self.config = self.manager.config

    def check_and_create_directory(self, path, must_exist=False):
        """ Vérifie et crée un dossier si nécessaire """
        if not os.path.exists(path):
            if must_exist:
                self.logger.write(Label.LOG_FOLDER_MUSTEXIST(path=path))
                sys.exit(1)
            os.makedirs(path)
            self.logger.write(Label.LOG_FOLDER_CREATED(path=path))

    def check_and_create_file(self, path, initContent=None):
        """ Vérifie et crée un fichier si nécessaire """
        if not os.path.exists:
            if not initContent:
                self.logger.write(Label.LOG_FILE_MUSTEXIST(path=path))
                sys.exit(1)
            with open(path, 'x') as file:
                file.write(initContent)
            self.logger.write(Label.LOG_FILE_CREATED(path=path))


    def verify_structure(self):
        """ Vérifie que la structure du projet est correcte """
        self.logger.write(Label.LOG_STRUCTURE_CHECK)
        # 🛠 Création des dossiers manquants si nécessaire
        self.check_and_create_directory(TEMPLATES_DIR, must_exist=True)
        self.check_and_create_directory(LOGS_DIR)
        self.check_and_create_directory(HOMES_DIR)
        self.check_and_create_directory(CLIENTS_DIR)
        self.check_and_create_directory(SKEL_DIR, must_exist=True)
        self.check_and_create_file(GLOBAL_CONFIG_FILE, GLOBAL_CONFIG_INITCONTENT)
        self.config.verify_clients()
        self.config.verify_profiles()
        self.logger.write(Label.LOG_STRUCTURE_OK)

