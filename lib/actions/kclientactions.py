import os, shutil
from PySide6.QtGui import QIcon
from core.actions import KAction, KCheckableAction
from core.env import CLIENTS_DIR, FAVORITE_ICON_PATH, NO_FAVORITE_ICON_PATH
from core.configs import GlobalConfig
from core.manager import config, logger, states, tr
from core.vpn_tools import is_vpn_container_running
from core.labels import Label

class KDeleteClientAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent=None):
        from core.widgets import KMessageBox as km, KMessageBoxButton as kmb
        self.KMessageBox = km
        self.KMessageBoxButton = kmb
        super().__init__(parent, Label.UI_CLIENT_PANEL_LABEL_DELETE_VPN)
        self._parent = parent
        self._client_name = None
        self._container_name = None

        self.triggered.connect(self._on_triggered)
        states.client_loading_requested.connect(self._update_client)
        states.vpn_status_changed.connect(self._on_client_update)
        self._on_client_update()  # état initial

    def _on_triggered(self):
        if self.isEnabled():
            """ 🗑 Demande la suppression d'un VPN via MainWindow """
            if is_vpn_container_running(self._container_name):
                self.KMessageBox.warning(
                    self,
                    Label.UI_CLIENT_PANEL_MSG_TITLE_VPN_DELETE_ERROR,
                    Label.UI_CLIENT_PANEL_MSG_CONTENT_VPN_DELETE_ERROR
                )
                return
            msgtitle = tr(Label.UI_CLIENT_PANEL_MSG_TITLE_VPN_DELETE_CONFIRM)
            msgtext = tr(Label.UI_CLIENT_PANEL_MSG_CONTENT_VPN_DELETE_CONFIRM(client_name=self._client_name))
            confirm = self.KMessageBox.warning(
                self._parent,
                msgtitle, msgtext,
                [self.KMessageBoxButton.Yes, self.KMessageBoxButton.No]
            )
            if confirm == self.KMessageBoxButton.No:
                return
            
            """ 🚀 Supprime un VPN depuis MainWindow """
            logger.write(Label.LOG_ACTIONS_DELETE_CLIENT(client_name=self._client_name))

            # Supprime l'entrée du `config.json` global
            config.deleteClientConfig(self._client_name)

            # # Supprime le dossier client (sans toucher à home)
            shutil.rmtree(os.path.join(CLIENTS_DIR, self._client_name), ignore_errors=True)

            # Réduit et désactive le VPN Panel
            # TODO gérer un client actif depuis le config manager direct
            # A faire dès que j'ai rework toutes les actions et la liste des vpns
                        
            # Mise à jour de l'affichage

            self.KMessageBox.information(self._parent,
                Label.UI_CLIENT_PANEL_MSG_TITLE_VPN_DELETED,
                Label.UI_CLIENT_PANEL_MSG_CONTENT_VPN_DELETED
            )

            states.emit_clients_list_update()
            states.emit_client_loading_request(None)
            states.emit_action_trigger(Label.ACTIONS_DELETE_CLIENT)

    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_client_update()

    def _on_client_update(self):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        if self._client_name is None:
            self.setDisabled(True)
        else:
            self.setDisabled(is_vpn_container_running(self._container_name))

class KToggleFavoriteAction(KCheckableAction):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._client_name = None
        self._container_name = None

        self.checked_changed.connect(self._on_toggle)
        states.client_loading_requested.connect(self._update_client)
        self._on_update()  # État initial

    def _on_toggle(self, state: bool):
        self._save_config()
    
    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_update()
    
    def _save_config(self):
        if self._client_name:
            # TODO si c'est un ajout, regarder si on  déjà 3 favoris set up 
            # TODO si oui alors on refuse de mettre à jour et on rollback le toggle (self.setChecked(False))
            # TODO si non, on continue normalement
            config.setValue(GlobalConfig.CLIENT_FAVORITE(client_id=self._client_name), self.isChecked())
            states.emit_client_favorite_update(self._client_name, self.isChecked())

    def _on_update(self):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        if not self._client_name:
            self.setDisabled(True)
            self.setCheckable(False)
        else:
            isFav = config.getValue(GlobalConfig.CLIENT_FAVORITE(client_id=self._client_name))
            self.setCheckable(True)
            self.setChecked(bool(isFav))
            self.setDisabled(False)

