from PySide6.QtWidgets import QInputDialog, QVBoxLayout, QMessageBox, QFileDialog
import os
import shutil
from core.env import TEMPLATES_DIR, CLIENTS_DIR, BASE_DIR
from core.manager import states, tr, config
from core.widgets import KDialog, KHeader, KWidget, KButton, KListWidget, KMessageBox, KMessageBoxButton
from core.labels import Label
from core.configs import GlobalConfig, ClientConfig

class KProfilesManagerDialog(KDialog):
    def __init__(self, main_pos, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 300, 400, 300)
        self.main_pos = main_pos
        self.update_position()

        # ───────────── Central widget
        self.central_widget = KWidget()
        # ───────────── Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        
        self.header = self._build_header()
        self.installHeader(self.header)

        # 📌 Liste des profils VPN existants
        self.profile_list = KListWidget()
        self.load_profiles()
        self.main_layout.addWidget(self.profile_list)

        # 📌 Boutons d'action
        self.btn_add = KButton(Label.UI_MANAGE_PROFILES_BUTTON_ADD_PROFILE)
        self.btn_rename = KButton(Label.UI_MANAGE_PROFILES_BUTTON_RENAME_PROFILE)
        self.btn_delete = KButton(Label.UI_MANAGE_PROFILES_BUTTON_DELETE_PROFILE)
        self.btn_refresh = KButton(Label.UI_MANAGE_PROFILES_BUTTON_REFRESH_PROFILE_LIST)

        self.btn_add.clicked.connect(self.add_profile)
        self.btn_rename.clicked.connect(self.rename_profile)
        self.btn_delete.clicked.connect(self.delete_profile)
        self.btn_refresh.clicked.connect(self.load_profiles)

        self.main_layout.addWidget(self.btn_add)
        self.main_layout.addWidget(self.btn_rename)
        self.main_layout.addWidget(self.btn_delete)
        self.main_layout.addWidget(self.btn_refresh)

        states.lang_updated.connect(self.load_profiles)

    def _build_header(self):
        """ 🔧 En-tête avec boutons """
        btn_close = KButton("❌")
        btn_close.setFixedSize(30, 30)
        # TODO faire une action pour restaurer une fenêtre
        # TODO elle doit connaitre la dernière fenêtre qui a été hide (compact ou full)
        # TODO elle remplacera le clicked.connect
        btn_close.clicked.connect(self.close)
        return KHeader(self, title=Label.UI_MANAGE_PROFILES_WINDOW_NAME, right_buttons=[btn_close])
    
    def update_position(self, main_pos=None):
        """ 📍 Se repositionne en fonction de la fenêtre principale """
        if main_pos:
            self.move(main_pos.x() + 50, main_pos.y() + 50)
        else:
            self.move(self.main_pos.x() + 50, self.main_pos.y() + 50)

    def load_profiles(self):
        """ 🔄 Charge et affiche les profils VPN existants """
        self.profile_list.clear()
        for profile_name in config.getValue(GlobalConfig.PROFILES).keys():
        #for profile_name, profile_data in config.global_config.get("profiles", {}).items():
            if config.getValue(GlobalConfig.PROFILE_ERROR(profile_id=profile_name)):
                status = tr(Label.STATUS_PROFILE_MISSING)
            else:
                status = tr(Label.STATUS_PROFILE_OK)
            # status = tr(Label.STATUS_PROFILE_MISSING) if profile_data.get("error") else tr(Label.STATUS_PROFILE_OK)
            self.profile_list.addItem(f"{profile_name} - {status}")

    def add_profile(self):
        """ 📂 Ajoute un nouveau profil VPN """
        profile_name = QFileDialog.getExistingDirectory(self,
            tr(Label.UI_MANAGE_PROFILES_MSG_ADD_PROFILE_SELECT),
            BASE_DIR
        )

        if not profile_name:
            return

        profile_name = os.path.basename(profile_name)

        if config.getValue(GlobalConfig.PROFILE(profile_id=profile_name)):
        #if profile_name in config.global_config["profiles"]:
            KMessageBox.warning(self,
                Label.UI_MANAGE_PROFILES_MSG_TITLE_ADD_PROFILE_ALREADY_EXIST,
                Label.UI_MANAGE_PROFILES_MSG_CONTENT_ADD_PROFILE_ALREADY_EXIST
            )
            return

        # 📌 Copie du dossier sélectionné dans TEMPLATES_DIR
        profile_target = os.path.join(TEMPLATES_DIR, profile_name)
        if not os.path.exists(profile_target):
            shutil.copytree(profile_name, profile_target)

        # 📌 Mise à jour du `config.json`
        config.setValue(GlobalConfig.PROFILE_ERROR(profile_id=profile_name), False)
        #config.global_config["profiles"][profile_name] = {"error": False}
        #config.save_global_config()

        KMessageBox.information(self,
            Label.UI_MANAGE_PROFILES_MSG_TITLE_PROFILE_CREATED,
            Label.UI_MANAGE_PROFILES_MSG_CONTENT_PROFILE_CREATED
        )
        self.load_profiles()

    def delete_profile(self):
        """ 🗑 Supprime un profil VPN """
        selected_item = self.profile_list.currentItem()
        if not selected_item:
            return
        
        profile_name = selected_item.text().split(" - ")[0]
        used_by = []
        # Vérification pour chaque client
        for client_name in config.getValue(GlobalConfig.CLIENTS).keys():
            if config.getValue(ClientConfig.PROFILE, client_name) == profile_name:
                used_by.append(client_name)
        #for client_name in os.listdir(CLIENTS_DIR):
            # client_config = config.get_client_config(client_name)
            # if client_config and client_config.get("profile") == profile_name:
            #     used_by.append(client_name)

        if used_by:
            KMessageBox.warning(
                self,
                Label.UI_MANAGE_PROFILES_MSG_TITLE_CANNOT_DELETE_PROFILE,
                Label.UI_MANAGE_PROFILES_MSG_CONTENT_CANNOT_DELETE_PROFILE(
                    profile_name = profile_name,
                    clients = f"{', '.join(used_by)}"
                )
            )
            return

        
        confirm = KMessageBox.warning(self,
            Label.UI_MANAGE_PROFILES_MSG_TITLE_WARNING_DELETE_PROFILE,
            Label.UI_MANAGE_PROFILES_MSG_CONTENT_WARNING_DELETE_PROFILE(
                profile_name=profile_name),
            KMessageBoxButton.Yes | KMessageBoxButton.No
        )

        if confirm == KMessageBoxButton.No:
            return  

        # 📌 Suppression du dossier de templates
        profile_path = os.path.join(TEMPLATES_DIR, profile_name)
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path)

        # 📌 Suppression du profil dans `config.json`
        config.deleteValue(GlobalConfig.PROFILE(profile_id=profile_name))
        # del config.global_config["profiles"][profile_name]
        # config.save_global_config()

        KMessageBox.information(self,
            Label.UI_MANAGE_PROFILES_MSG_TITLE_PROFILE_DELETED,
            Label.UI_MANAGE_PROFILES_MSG_CONTENT_PROFILE_DELETED(profile_name=profile_name)
        )
        self.load_profiles()

    def rename_profile(self):
        """ ✏️ Renomme un profil VPN """
        selected_item = self.profile_list.currentItem()
        if not selected_item:
            return

        profile_name = selected_item.text().split(" - ")[0]
        new_name, ok = QInputDialog.getText(self,
            tr(Label.UI_MANAGE_PROFILES_MSG_TITLE_PROFILE_RENAME),
            tr(Label.UI_MANAGE_PROFILES_MSG_CONTENT_PROFILE_RENAME(profile_name=profile_name))
        )

        if not ok or not new_name.strip():
            return
        new_name = new_name.strip()

        # Vérifier si le nom existe déjà
        if new_name in config.getValue(GlobalConfig.PROFILES).keys():
            KMessageBox.warning(self,
                Label.UI_MANAGE_PROFILES_MSG_TITLE_PROFILE_RENAME_ERROR,
                Label.UI_MANAGE_PROFILES_MSG_CONTENT_PROFILE_RENAME_ERROR(profile_name=new_name),
            )
            return

        used_by = []
        # Vérification pour chaque client
        for client_name in config.getValue(GlobalConfig.CLIENTS).keys():
            if config.getValue(ClientConfig.PROFILE, client_name) == profile_name:
                used_by.append(client_name)
        # for client_name in os.listdir(CLIENTS_DIR):
        #     client_config = config.get_client_config(client_name)
        #     if client_config and client_config.get("profile") == profile_name:
        #         used_by.append(client_name)

        # Vérifier si le profil est utilisé
        if used_by:
            confirm = KMessageBox.warning(self,
                Label.UI_MANAGE_PROFILES_MSG_TITLE_PROFILE_RENAME_WARNING,
                Label.UI_MANAGE_PROFILES_MSG_CONTENT_PROFILE_RENAME_WARNING(
                    profile_name=profile_name,
                    new_name=new_name,
                    nbvpn=str(len(used_by))
                ),
                KMessageBoxButton.Yes | KMessageBoxButton.No
            )
            if confirm == KMessageBoxButton.No:
                return

        # Mettre à jour la config globale
        config.setValue(GlobalConfig.PROFILES, new_name)
        config.setValue(GlobalConfig.PROFILE_ERROR(profile_id=new_name),
            config.getValue(GlobalConfig.PROFILE_ERROR(profile_id=profile_name))
        )
        config.deleteValue(GlobalConfig.PROFILES, profile_name)
        #config["profiles"][new_name] = config["profiles"].pop(profile_name)

        # Mettre à jour les clients utilisant ce profil
        for client_name in used_by:
            config.setValue(ClientConfig.PROFILE, new_name, client_name)
            # client_config = config.get_client_config(client)
            # client_config["profile"] = new_name
            # config.save_client_config(client, client_config)

        #print(f"{config}")
        #config.save_global_config()

        # Renommer le dossier de templates
        old_path = os.path.join(TEMPLATES_DIR, profile_name)
        new_path = os.path.join(TEMPLATES_DIR, new_name)
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)

        KMessageBox.information(
            self,
            Label.UI_MANAGE_PROFILES_MSG_TITLE_PROFILE_RENAME_SUCCESS,
            Label.UI_MANAGE_PROFILES_MSG_CONTENT_PROFILE_RENAME_SUCCESS(
                profile_name=profile_name,
                new_name=new_name
            )
        )
        self.load_profiles()