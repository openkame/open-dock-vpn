from core.actions import KAction, KCheckableAction
from core.manager import states, logger, tr, config
from core.vpn_tools import (
    is_vpn_container_running,
    start_vpn_container,
    stop_vpn_container,
    open_vpn_container_chromium,
    open_vpn_container_shell
)

from core.labels import Label
from core.configs import ClientConfig

class KStartVpnAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent=None, text:str|Label|None=None):
        KAction.__init__(self, parent, text)
        self._client_name = None
        self._container_name = None

        self.triggered.connect(self._on_triggered)
        states.vpn_status_changed.connect(self._on_update)
        self._on_update()  # état initial

    def _on_triggered(self):
        if self.isEnabled():
            if start_vpn_container(self._client_name):
                logger.write(
                    Label.LOG_VPNPANEL_GLOBAL_START_SUCCESS(client_name=self._client_name),
                    self._client_name,
                    Label.LOG_VPNPANEL_CLIENT_START_SUCCESS
                )
                states.emit_vpn_status_change(self._client_name, tr(Label.STATUS_VPN_CONNECTED))
                states.emit_action_trigger(Label.ACTIONS_START_VPN)
    
    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_update()

    def _on_update(self):
        # Active l'action uniquement si un client est set
        if self._client_name is None:
            self.setDisabled(True)
        else:
            self.setDisabled(is_vpn_container_running(self._container_name))

class KStopVpnAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent=None, text:str|Label|None=None):
        KAction.__init__(self, parent, text)
        self._client_name = None
        self._container_name = None

        self.triggered.connect(self._on_triggered)
        states.vpn_status_changed.connect(self._on_update)
        self._on_update()  # état initial

    def _on_triggered(self):
        if self.isEnabled():
            if stop_vpn_container(self._client_name):
                logger.write(
                    Label.LOG_VPNPANEL_GLOBAL_STOP_SUCCESS(client_name=self._client_name),
                    self._client_name,
                    Label.LOG_VPNPANEL_CLIENT_STOP_SUCCESS
                )
                states.emit_vpn_status_change(self._client_name, tr(Label.STATUS_VPN_DISCONNECTED))
                states.emit_action_trigger(Label.ACTIONS_STOP_VPN)
    
    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_update()

    def _on_update(self):
        # Active l'action uniquement si un client est set
        if self._client_name is None:
            self.setDisabled(True)
        else:
            self.setDisabled(not is_vpn_container_running(self._container_name))

class KRefreshVpnAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent=None, text:str|Label|None=None):
        KAction.__init__(self, parent, text)
        from core.widgets import KMessageBox as km, KMessageBoxButton as kmb
        self.KMessageBox = km
        self.KMessageBoxButton = kmb
        self._client_name = None
        self._container_name = None

        self.triggered.connect(self._on_triggered)
        states.vpn_status_changed.connect(self._on_update)
        self._on_update()  # état initial

    def _on_triggered(self):
        """ 🔄 Rafraîchit l'image Docker du VPN """
        if self.isEnabled():
            restart_after_refresh = False
            if is_vpn_container_running(self._container_name):
                confirm = self.KMessageBox.question(self,
                    Label.UI_CLIENT_PANEL_MSG_TITLE_VPN_REFRESH_WARNING,
                    Label.UI_CLIENT_PANEL_MSG_CONTENT_VPN_REFRESH_WARNING,
                    [self.KMessageBoxButton.Yes, self.KMessageBoxButton.No]
                )
                restart_after_refresh = (confirm == self.KMessageBoxButton.Yes)

            stop_vpn_container(self._client_name, delete_image=True)  # Supprime et arrête le container
            if restart_after_refresh:
                start_vpn_container(self._client_name)  # Relance si l’utilisateur a accepté
                states.emit_vpn_status_change(self._client_name, tr(Label.STATUS_VPN_CONNECTED))
            else:
                states.emit_vpn_status_change(self._client_name, tr(Label.STATUS_VPN_DISCONNECTED))
            states.emit_action_trigger(Label.ACTIONS_REFRESH_VPN)
    
    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_update()

    def _on_update(self):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        if self._client_name is None:
            self.setDisabled(True)
        else:
            self.setDisabled(False)

class KOpenTerminalAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent=None, text:str|Label|None=None):
        KAction.__init__(self, parent, text)
        self._client_name = None
        self._container_name = None

        self.triggered.connect(self._on_triggered)
        states.vpn_status_changed.connect(self._on_update)
        self._on_update()  # état initial

    def _on_triggered(self):
        if self.isEnabled():
            open_vpn_container_shell(self._container_name, self._client_name)
            states.emit_action_trigger(Label.ACTIONS_OPEN_TERMINAL(client_name=self._client_name))
    
    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_update()

    def _on_update(self):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        if self._client_name is None:
            self.setDisabled(True)
        else:
            self.setDisabled(not is_vpn_container_running(self._container_name))

class KOpenBrowserAction(KAction):
    """ 🎨 Action centrale pour changer le mode de thème """
    def __init__(self, parent=None, text:str|Label|None=None):
        KAction.__init__(self, parent, text)
        self._client_name = None
        self._container_name = None

        self.triggered.connect(self._on_triggered)
        states.vpn_status_changed.connect(self._on_update)
        self._on_update()  # état initial

    def _on_triggered(self):
        if self.isEnabled():
            open_vpn_container_chromium(self._container_name, self._client_name)
            states.emit_action_trigger(Label.ACTIONS_OPEN_BROWSER(client_name=self._client_name))
    
    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_update()

    def _on_update(self):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        if self._client_name is None:
            self.setDisabled(True)
        else:
            self.setDisabled(not is_vpn_container_running(self._container_name))


class KToggleAutoStartVpnAction(KCheckableAction):

    def __init__(self, parent=None):
        super().__init__(parent, Label.UI_CLIENT_PANEL_LABEL_CHECKBOX_AUTOSTART)
        self._client_name = None
        self._container_name = None
        self.checked_changed.connect(self._on_toggle)
        states.vpn_status_changed.connect(self._on_update)
        states.client_loading_requested.connect(self._update_client)
        self._on_update()  # état initial 

    def _on_toggle(self, state: bool):
        self._save_config()
    
    def _update_client(self, client_name):
        self._client_name = client_name
        self._container_name = self._client_name.replace("@", "-")
        self._on_update()
    
    def _save_config(self):
        if self._client_name:
            config.setValue(ClientConfig.AUTOSTART, self.isChecked(), self._client_name)   

    def _on_update(self):
        # Active l'action uniquement si elle n'est pas déjà sélectionnée
        if not self._client_name:
            self.setDisabled(True)
            self.setCheckable(False)
        else:
            running = is_vpn_container_running(self._container_name)
            isAutostarting = config.getValue(ClientConfig.AUTOSTART, self._client_name)
            if isAutostarting:
                self.setCheckable(True)
            self.setChecked(bool(isAutostarting))
            if running:
                self.setDisabled(True)
                self.setCheckable(False)
            else:
                self.setDisabled(False)
                self.setCheckable(True)


class KStartVpnFullAction(KStartVpnAction):
    def __init__(self, parent=None):
        KStartVpnAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_START_VPN)
        states.client_loading_requested.connect(self._update_client)

class KStartVpnShortAction(KStartVpnAction):
    def __init__(self, client_name:str, parent=None):
        KStopVpnAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_START_VPN_SHORT)
        self._update_client(client_name)
        
class KStopVpnFullAction(KStopVpnAction):
    def __init__(self, parent=None):
        KStopVpnAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_STOP_VPN)
        states.client_loading_requested.connect(self._update_client)

class KStopVpnShortAction(KStopVpnAction):
    def __init__(self, client_name:str, parent=None):
        KStopVpnAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_STOP_VPN_SHORT)
        self._update_client(client_name)

class KRefreshVpnFullAction(KRefreshVpnAction):
    def __init__(self, parent=None):
        KRefreshVpnAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_REFRESH_VPN)
        states.client_loading_requested.connect(self._update_client)

class KRefreshVpnShortAction(KRefreshVpnAction):
    def __init__(self, client_name:str, parent=None):
        KRefreshVpnAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_REFRESH_VPN_SHORT)
        self._update_client(client_name)

class KOpenTerminalFullAction(KOpenTerminalAction):
    def __init__(self, parent=None):
        KOpenTerminalAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_SHELL)
        states.client_loading_requested.connect(self._update_client)

class KOpenTerminalShortAction(KOpenTerminalAction):
    def __init__(self, client_name:str, parent=None):
        KOpenTerminalAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_SHELL_SHORT)
        self._update_client(client_name)

class KOpenBrowserFullAction(KOpenBrowserAction):
    def __init__(self, parent=None):
        KOpenBrowserAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_CHROMIUM)
        states.client_loading_requested.connect(self._update_client)

class KOpenBrowserShortAction(KOpenBrowserAction):
    def __init__(self, client_name:str, parent=None):
        KOpenBrowserAction.__init__(self, parent, Label.UI_CLIENT_PANEL_LABEL_CHROMIUM_SHORT)
        self._update_client(client_name)
