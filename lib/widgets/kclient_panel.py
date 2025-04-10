from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt

from core.manager import tr, config, states
from core.actions import (
    KStartVpnFullAction, KStopVpnFullAction, KRefreshVpnFullAction,
    KOpenTerminalFullAction, KOpenBrowserFullAction,
    KDeleteClientAction, KToggleAutoStartVpnAction, KToggleFavoriteAction
)
from widgets.kwidgets import KWidget, KLabel, KCheckBox, KButton
from widgets.kframe import KFrame
from widgets.klayouts import KVBoxLayout, KHBoxLayout
from core.vpn_tools import is_vpn_container_running

from core.labels import Label
from core.configs import GlobalConfig, ClientConfig

class KClientPanel(KWidget):
    def __init__(self):
        super().__init__()

        # définition des vriable internes
        self._client_name=None
        self._container_name = None
        self._username = None

        self._frame = KFrame(style="client_panel_frame")
        self._frame_layout = KVBoxLayout(self._frame)
        self.main_layout = KVBoxLayout(self)
        self.main_layout.addWidget(self._frame)
        self.main_layout.setSpacing(10)

        # ──────────── Title + Status (Nom du client + emoji statut)
        title_layout = KVBoxLayout()
        title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label = KLabel(Label.UI_CLIENT_PANEL_LABEL_CLIENT_NAME(
            client_name=tr(Label.UI_CLIENT_PANEL_LABEL_CHECKING)
        ), "client_panel_title")
        self.title_label.setFixedWidth(400)

        self.status_label = KLabel(
            Label.UI_CLIENT_PANEL_LABEL_CLIENT_STATUS(status=tr(Label.STATUS_VPN_CHECKING)),
            "client_panel_status"
        )  # État actuel
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.status_label)
        title_layout.addStretch()
        self._frame_layout.addLayout(title_layout)
        self._frame_layout.addStretch()

        # ──────────── Toggle Autostart + profil VPN utilisé
        self.details_frame = KFrame(style="clientpanel_block")
        self._frame_layout.addWidget(self.details_frame)

        self.details_layout = KVBoxLayout(self.details_frame)
        
        self.details_sublayout = KHBoxLayout()
        self.details_layout.addLayout(self.details_sublayout)
        
        self.vpn_profile_label = KLabel(Label.UI_CLIENT_PANEL_LABEL_PROFILE(
            profile_name=tr(Label.UI_CLIENT_PANEL_LABEL_CHECKING)
        ), "client_panel_profile")
        self.details_sublayout.addWidget(self.vpn_profile_label)
        self.details_sublayout.addStretch()
        self.favorite_toggle = KCheckBox(action=KToggleFavoriteAction(), style="client_panel_favorite")
        self.details_sublayout.addWidget(self.favorite_toggle)
        
        self.autostart_toggle = KCheckBox(action=KToggleAutoStartVpnAction())
        self.details_layout.addWidget(self.autostart_toggle)

        # ──────────── Dernière action + Démarré le
        # TODO c'est toujours en mock cette partie n'est pas implémenté dans l'appli encore
        # TODO -> Récupération de la dernière action + date depuis la log
        # TODO -> ou alors enregistrer daans global config la dernière action :
        # TODO -> grâce au signal action_triggered on peu faire un truc
        # TODO -> et donc on peut récupérer la last action depuis la config globale et le signal
        # self.last_action_frame = KFrame(style="clientpanel_block")
        # self._frame_layout.addWidget(self.last_action_frame)

        # self.last_action_layout = KVBoxLayout(self.last_action_frame)
        # self.last_action_label = KLabel(Label.UI_CLIENT_PANEL_LABEL_LAST_ACTION(
        #     action=tr(Label.LOG_ACTIONS_START_VPN)
        # ), "client_panel_last_action")
        # self.last_action_status_label = KLabel(
        #     Label.LOG_ACTIONS_START_SUCCESS(date="2025-03-23 14:21"),
        #     "clientpanel_status_label"
        # )
        # self.last_action_layout.addWidget(self.last_action_label)
        # self.last_action_layout.addWidget(self.last_action_status_label)


        # ──────────── Actions principales (Start / Stop / Refresh VPN)
        self.main_actions_frame = KFrame(style="clientpanel_block")
        self._frame_layout.addWidget(self.main_actions_frame)

        self.main_actions_layout = KHBoxLayout(self.main_actions_frame)
        self.btn_start = KButton(style="clientpanel_action_button", action=KStartVpnFullAction())
        self.btn_stop = KButton(style="clientpanel_action_button", action=KStopVpnFullAction())
        self.btn_refresh = KButton(style="clientpanel_action_button", action=KRefreshVpnFullAction())
        self.main_actions_layout.addWidget(self.btn_start)
        self.main_actions_layout.addWidget(self.btn_stop)
        self.main_actions_layout.addWidget(self.btn_refresh)

        # ──────────── Quick actions (Terminal / Browser)
        self.quick_actions_frame = KFrame(style="clientpanel_block")
        self._frame_layout.addWidget(self.quick_actions_frame)

        self.quick_actions_layout = KHBoxLayout(self.quick_actions_frame)
        self.btn_terminal = KButton(style="clientpanel_action_button", action=KOpenTerminalFullAction())
        self.btn_browser = KButton(style="clientpanel_action_button", action=KOpenBrowserFullAction())

        self.quick_actions_layout.addWidget(self.btn_terminal)
        self.quick_actions_layout.addWidget(self.btn_browser)

        # ──────────── Delete button (Red, bottom-aligned)
        self.btn_delete = KButton(style="delete_button", action=KDeleteClientAction())
        self.btn_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self._frame_layout.addStretch()
        self._frame_layout.addWidget(self.btn_delete)

        states.client_loading_requested.connect(self._updatePanel)
        self._updatePanel()
   
    
    def _updatePanel(self, client_name=None):
        """ Charge un VPN dans le panneau """
        # Chargement initiale sans VPN ( utile aussi lors d'une suppression)
        # TODO remplacer le layout principal (self._frame_layout) pour afficher un klabel 'no selection'
        if not self._client_name and not client_name:
            self.title_label.updateText(Label.UI_CLIENT_PANEL_LABEL_CLIENT_NAME(
                client_name=tr(Label.UI_CLIENT_PANEL_LABEL_CHECKING)
            ))
            self.status_label.updateText(Label.UI_CLIENT_PANEL_LABEL_CLIENT_STATUS(
                status=tr(Label.STATUS_VPN_CHECKING)
            ))
            self.vpn_profile_label.updateText(Label.UI_CLIENT_PANEL_LABEL_NO_PROFILE)
            return
        # si un client est envoyé alors on remplace, sinon c'est jsute un reload du client actuel
        if client_name:
            self._client_name = client_name
                    
        self._container_name = self._client_name.replace("@", "-")
        self._container_name = self._client_name.split("@")[0]

        isRunning = is_vpn_container_running(self._container_name)

        self.title_label.updateText(Label.UI_CLIENT_PANEL_LABEL_CLIENT_NAME(
            client_name=self._client_name
        ))
        if isRunning:
            self.status_label.updateText(Label.UI_CLIENT_PANEL_LABEL_CLIENT_STATUS(
                status=tr(Label.STATUS_VPN_CONNECTED)
            ))
        else:
            self.status_label.updateText(Label.UI_CLIENT_PANEL_LABEL_CLIENT_STATUS(
                status=tr(Label.STATUS_VPN_DISCONNECTED)
            ))
        
        if config.getValue(GlobalConfig.CLIENT_FAVORITE(client_id=self._client_name)) != None:
            self.favorite_toggle.setDisabled(False)
            self.favorite_toggle.setChecked(config.getValue(GlobalConfig.CLIENT_FAVORITE(client_id=self._client_name)))
        else:
            self.favorite_toggle.setDisabled(True)

        if config.getValue(ClientConfig.AUTOSTART, client_name) != None:
            self.autostart_toggle.setDisabled(False)
            self.autostart_toggle.setChecked(config.getValue(ClientConfig.AUTOSTART, client_name))
        else:
            self.autostart_toggle.setDisabled(True)
        
        profile_name = config.getValue(ClientConfig.PROFILE, client_name)
        if profile_name and not config.getValue(GlobalConfig.PROFILE_ERROR(profile_id=profile_name)):
            self.vpn_profile_label.updateText(Label.UI_CLIENT_PANEL_LABEL_PROFILE(
                profile_name=profile_name
            ))
            self.setDisabled(False)
        else:
            self.vpn_profile_label.updateText(Label.UI_CLIENT_PANEL_LABEL_NO_PROFILE)
            self.setDisabled(True)
        if isRunning:
            self.autostart_toggle.setDisabled(True)
        else:
            self.autostart_toggle.setDisabled(False)