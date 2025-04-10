from PySide6.QtWidgets import QVBoxLayout
import os
import shutil
from core.env import CLIENTS_DIR, HOMES_DIR, SKEL_NAME, SKEL_DIR
from core.manager import tr, config, logger, states
from core.docker import generate_docker_files
from core.widgets import (
    KHeader, KDialog, KWidget, KButton,
    KComboBox, KLabel, KLineEdit, KFileDialog,
    KMessageBox, KMessageBoxButton
)
from core.labels import Label
from core.configs import GlobalConfig

class KAddClientDialog(KDialog):
    def __init__(self, main_pos, parent=None):
        super().__init__(parent)
        self.setGeometry(200, 200, 400, 300)
        self.main_pos = main_pos
        self.update_position()
       
        # ───────────── Central widget
        self.central_widget = KWidget()
        # ───────────── Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        
        self.header = self._build_header()
        self.installHeader(self.header)

        # 📌 Sélection du fichier OVPN
        self.btn_select_ovpn = KButton(Label.UI_ADD_CLIENT_BUTTON_SELECT_OVPN)
        self.btn_select_ovpn.clicked.connect(self.select_ovpn)
        self.main_layout.addWidget(self.btn_select_ovpn)

        # 📌 Affichage du statut du fichier sélectionné
        self.ovpn_status_label = KLabel(Label.STATUS_OVPN_NOFILE)
        self.main_layout.addWidget(self.ovpn_status_label)

        # 📌 Champs utilisateur / VPN / domaine (désactivés au départ)
        self.user_input = KLineEdit()
        self.vpn_input = KLineEdit()
        self.domain_input = KLineEdit()
        self.ovpn_file = None  # 📂 Fichier OVPN sélectionné

        self.main_layout.addWidget(KLabel(Label.UI_ADD_CLIENT_LABEL_VPN_USER))
        self.main_layout.addWidget(self.user_input)
        self.main_layout.addWidget(KLabel(Label.UI_ADD_CLIENT_LABEL_VPN_NAME))
        self.main_layout.addWidget(self.vpn_input)
        self.main_layout.addWidget(KLabel(Label.UI_ADD_CLIENT_LABEL_DOMAIN_NAME))
        self.main_layout.addWidget(self.domain_input)

        self.user_input.setDisabled(True)
        self.vpn_input.setDisabled(True)
        self.domain_input.setDisabled(True)

        # 📌 Liste des profils disponibles
        self.main_layout.addWidget(KLabel(Label.UI_ADD_CLIENT_LABEL_PROFILE_LIST))
        self.profile_select = KComboBox()
        self.profile_select.addItem(tr(Label.UI_ADD_CLIENT_LABEL_PROFILE_SELECT))
        self.profile_select.setDisabled(True)  # Désactivée tant qu'on n'a pas choisi un fichier OVPN
        self.main_layout.addWidget(self.profile_select)

        # 📌 Chargement des profils VPN disponibles
        self.load_profiles()

        # 📌 Bouton de validation (désactivé au départ)
        self.btn_submit = KButton(Label.UI_ADD_CLIENT_BUTTON_SUBMIT)
        self.btn_submit.setDisabled(True)
        self.btn_submit.clicked.connect(self.add_client)
        self.main_layout.addWidget(self.btn_submit)
    
    def _build_header(self):
        """ 🔧 En-tête avec boutons """
        btn_close = KButton("❌")
        btn_close.setFixedSize(30, 30)
        # TODO faire une action pour restaurer une fenêtre
        # TODO elle doit connaitre la dernière fenêtre qui a été hide (compact ou full)
        # TODO elle remplacera le clicked.connect
        btn_close.clicked.connect(self.close)
        return KHeader(self, title=Label.UI_ADD_CLIENT_WINDOW_NAME, right_buttons=[btn_close])

    def update_position(self, main_pos=None):
        """ 📍 Se repositionne en fonction de la fenêtre principale """
        if main_pos:
            self.move(main_pos.x() + 50, main_pos.y() + 50)
        else:
            self.move(self.main_pos.x() + 50, self.main_pos.y() + 50)

    def load_profiles(self):
        """ 🔄 Charge les profils VPN depuis `config.json` """
        if config.hasValue(GlobalConfig.PROFILES):
            self.profile_select.addItems(config.getValue(GlobalConfig.PROFILES).keys())
        #if "profiles" in config.global_config:
            #self.profile_select.addItems(config.global_config["profiles"].keys())

    def select_ovpn(self):
        """ 📂 Sélectionne un fichier OVPN et remplit les champs automatiquement """
        file, _ = KFileDialog.getOpenFileName(
            self,
            Label.UI_ADD_CLIENT_MSG_TITLE_SELECT_OVPN,
            None,
            Label.UI_ADD_CLIENT_MSG_TYPE_SELECT_OVPN)
        if file:
            self.ovpn_file = file
            filename = os.path.basename(file)
            self.ovpn_status_label.updateText(Label.STATUS_OVPN_SELECTED(file_name=filename))
            #self.ovpn_status_label.setText(tr({"key" : "OVPN_STATUS.selected", "file_name" : filename}))

            # 📌 Extraction automatique du nom utilisateur et VPN depuis le fichier
            
            if "@" in filename and "." in filename:
                client_name = filename.replace(".ovpn", "")
                user, vpn_domain = client_name.split("@", 1)
                vpn, domain = vpn_domain.split(".", 1)

                self.user_input.setText(user)
                self.vpn_input.setText(vpn)
                self.domain_input.setText(domain)
            else:
                self.user_input.setText("")
                self.vpn_input.setText("")
                self.domain_input.setText("")

            # 📌 Activation des champs
            self.user_input.setDisabled(False)
            self.vpn_input.setDisabled(False)
            self.domain_input.setDisabled(False)
            self.profile_select.setDisabled(False)

            self.profile_select.setCurrentIndex(0)  # On force l'utilisateur à choisir un profil

            # 📌 Activation du bouton "Ajouter" uniquement si un profil est sélectionné
            self.profile_select.currentIndexChanged.connect(self.update_submit_button)

    def update_submit_button(self):
        """ ✅ Active le bouton Ajouter uniquement si tout est rempli """
        if self.profile_select.currentIndex() > 0:
            self.btn_submit.setDisabled(False)
        else:
            self.btn_submit.setDisabled(True)

    def add_client(self):
        """ 📌 Ajoute le client VPN et génère les fichiers nécessaires """
        user = self.user_input.text().strip()
        vpn = self.vpn_input.text().strip()
        domain = self.domain_input.text().strip()
        profile = self.profile_select.currentText()
        client_name = f"{user}@{vpn}.{domain}"
        
        if not user or not vpn or not domain or not self.ovpn_file:
            KMessageBox.warning(
                self,
                Label.UI_ADD_CLIENT_MSG_TITLE_ERROR,
                Label.UI_ADD_CLIENT_MSG_CONTENT_MISSING_FIELDS_ERROR
            )
            return

        vpn_dir = os.path.join(CLIENTS_DIR, client_name)

        # ⚠️ Vérifier si le VPN existe déjà
        if os.path.exists(vpn_dir):
            confirm = KMessageBox.warning(self,
                Label.UI_ADD_CLIENT_MSG_TITLE__VPN_ALREADY_EXISTS,
                Label.UI_ADD_CLIENT_MSG__CONTENT_VPN_ALREADY_EXISTS,
                [KMessageBoxButton.Yes, KMessageBoxButton.No]
            )
            if confirm == KMessageBoxButton.No:
                return

        home_dir = os.path.join(HOMES_DIR, client_name)
        skel_target = os.path.join(vpn_dir, SKEL_NAME)

        # 📌 Vérifier si le home directory existait déjà
        home_exists = os.path.exists(home_dir)

        os.makedirs(vpn_dir, exist_ok=True)
        os.makedirs(home_dir, exist_ok=True)

        # 📌 Copier `skel` dans `home_dir` si c'est une première création
        if not home_exists and os.path.exists(SKEL_DIR):
            for item in os.listdir(SKEL_DIR):
                src = os.path.join(SKEL_DIR, item)
                dest = os.path.join(home_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dest)

        # 📌 Copie du fichier OVPN
        shutil.copy(self.ovpn_file, os.path.join(vpn_dir, f"{user}.ovpn"))

        # 📌 Copier `skel` dans `vpn_dir/skel` pour que Docker y accède correctement
        if not os.path.exists(skel_target) and os.path.exists(SKEL_DIR):
            shutil.copytree(SKEL_DIR, skel_target, dirs_exist_ok=True)

        # 🔥 Générer les fichiers Docker directement
        generate_docker_files(user, vpn, domain, profile)

        # 🆕 Sauvegarde du fichier `config.json` local avec le profil sélectionné

        config.createClientConfig(client_name, {"profile": profile, "autostart": False})

        states.emit_clients_list_update()

        logger.write(Label.LOG_CLIENT_ADDED(
            client_name=client_name,
            profile=profile
        ))
        self.close()
