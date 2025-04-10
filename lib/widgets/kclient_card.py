from PySide6.QtWidgets import QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt

from widgets.kwidgets import KWidget, KLabel, KButton
from widgets.kframe import KFrame
from widgets.klayouts import KVBoxLayout, KGridLayout
from core.manager import states, config
from core.labels import Label
from core.configs import GlobalConfig
from core.configs import ClientConfig
from core.vpn_tools import is_vpn_container_running
from core.actions import (
    KStartVpnShortAction, KStopVpnShortAction,
    KOpenTerminalShortAction, KOpenBrowserShortAction
)

class KClientFullCard(KWidget):
    """🧩 Carte complète pour client VPN (Vue Complète)"""

    def __init__(self, client_name: str, parent=None):
        super().__init__(parent)
        self.client_name = client_name
        self.container_name = client_name.replace("@", "-")
        self._displayed=False
        self._selected = False

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        
        self._layout = KVBoxLayout(self)
        

        # 🔲 Encadrement principal
        self._frame = KFrame(style="fullcard_frame")
        self._layout.addWidget(self._frame)

        self._frame_layout = KGridLayout(self._frame)
        self._frame_layout.setSpacing(8)
        

        # 🔹 Nom du client
        self.name_label = KLabel(client_name, "fullcard_name")
        #self.name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._frame_layout.addWidget(self.name_label, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # 🔹 Label Autostart
        autostart = config.getValue(ClientConfig.AUTOSTART, client_name)
        autostart_label = Label.FULLCARD_AUTOSTARTING if autostart else Label.FULLCARD_NOTAUTOSTARTING
        self.autostart_label = KLabel(autostart_label, "fullcard_autostarting")
        self._frame_layout.addWidget(self.autostart_label, 1, 0, 1, 1)

        # self.spacer = QSpacerItem(48,0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        # self._frame_layout.addItem(self.spacer, 0, 1, 2, 2)

        # 🔹 Étiquette de statut
        self.status_label = KLabel(Label.STATUS_VPN_CHECKING, "fullcard_status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.status_label.setFixedWidth(36)
        self._frame_layout.addWidget(self.status_label, 0, 1, 2, 1, Qt.AlignmentFlag.AlignCenter)

        # 🔹 Étiquette favori
        is_fav = config.getValue(GlobalConfig.CLIENT_FAVORITE(client_id=client_name))
        self.fav_label = KLabel("⭐", "fullcard_fav")
        if is_fav:
            self._frame_layout.addWidget(self.fav_label, 0, 1, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        
        


    def updateDisplayed(self, displayed: bool):
        self._displayed = displayed
        if displayed:
            self._connectAll()
            self._update_status(self.client_name)
        else:
            self._disconnectAll()
    
    def setSelected(self, selected: bool):
        if selected == self._selected:
            return
        self._selected = selected
        self._frame.setProperty("selected", selected)
        print("---", self.client_name, selected)
        # ✅ Ne rafraîchit le style que si le widget a un parent (rattaché à l'UI)
        if self._displayed:
            print("processing frame update")
            self._frame.style().unpolish(self._frame)
            self._frame.style().polish(self._frame)
            self._frame.update()

    def _connectAll(self):
        # 🔁 Signaux
        try:
            states.client_loading_requested.connect(self._updateSelected)
            states.vpn_status_changed.connect(self._update_status)
            states.client_favorite_updated.connect(self._update_fav)
            return True
        except Exception as e:
            print("An error issued while connecting signals : \n", e)
            return False
            

    def _disconnectAll(self):
        # 🔁 Signaux
        try:
            states.vpn_status_changed.disconnect(self._update_status)
            states.client_favorite_updated.disconnect(self._update_fav)
            states.client_loading_requested.disconnect(self._updateSelected)
        except Exception as e:
            print("An error issued while disconnecting signals : \n", e)
            return False
    
    def _updateSelected(self, client_name):
        if client_name == self.client_name:
            self.setSelected(True)
        else:
            self.setSelected(False)

    def _update_status(self, client=None, status=None):
        if client and self.client_name != client:
            return
        self.vpn_running = is_vpn_container_running(self.container_name)
        self.status_label.updateText(Label.STATUS_VPN_CONNECTED if self.vpn_running else Label.STATUS_VPN_DISCONNECTED)

    def _update_fav(self, client, status):
        if self.client_name != client:
            return
        if status:
            self._frame_layout.addWidget(self.fav_label, 0, 1, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        else:
            self._frame_layout.removeWidget(self.fav_label)
            self.fav_label.setParent(None)        

    # 🔘 Rend la carte cliquable
    def mousePressEvent(self, event):
        states.emit_client_loading_request(self.client_name)
        
class KClientFavCard(KWidget):
    """🧩 Carte compacte pour client favori (Vue Compacte)"""
    def __init__(self, client_name: str, parent=None):
        super().__init__(parent)
        self._displayed = False
        self.client_name = client_name
        self.container_name = client_name.replace("@", "-")
        self.vpn_running = is_vpn_container_running(self.container_name)

        # 💡 Layout horizontal
        self._layout = KVBoxLayout(self)
        
        # On encadre chaque carte
        self._frame = KFrame(style="favcard_frame")

        self._frame_layout = KGridLayout(self._frame)
        self._frame_layout.setSpacing(6)
        self._frame_layout.setContentsMargins(5,5,5,5)

        self._layout.addWidget(self._frame)
        self.setLayout(self._layout)

        # 🔹 Nom du client
        self.name_label = KLabel(client_name, "favcard_name")
        self.name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._frame_layout.addWidget(self.name_label, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # 🔹 Étiquette autostart
        autostart = config.getValue(ClientConfig.AUTOSTART, client_name)
        autostart_label = Label.COMPACTCARD_AUTOSTARTING if autostart else Label.COMPACTCARD_NOTAUTOSTARTING
        self.autostart_label = KLabel(autostart_label, "favcard_autostarting")
        self._frame_layout.addWidget(self.autostart_label, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom) 
        
        self._frame_layout.addItem(QSpacerItem(64, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 1, 2, 1)

        # 🔹 Bouton d'action VPN (▶️ ou ⏹)
        self.start_button = KButton(action=KStartVpnShortAction(client_name))
        self.start_button.setFixedSize(32, 32)
        self.stop_button = KButton(action=KStopVpnShortAction(client_name))
        self.stop_button.setFixedSize(32, 32)

        self._frame_layout.addWidget(self.stop_button, 0, 2, 2, 1, Qt.AlignmentFlag.AlignCenter)

        # 🔹 Boutons Terminal et Browser
        self.terminal_button = KButton(action=KOpenTerminalShortAction(client_name))
        self.terminal_button.setFixedSize(32, 32)
        self._frame_layout.addWidget(self.terminal_button, 0, 3, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.browser_button = KButton(action=KOpenBrowserShortAction(client_name))
        self.browser_button.setFixedSize(32, 32)
        self._frame_layout.addWidget(self.browser_button, 0, 4, 2, 1, Qt.AlignmentFlag.AlignCenter)

        # 🔹 Étiquette de statut VPN
        self.status_label = KLabel("⏳", "favcard_status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.status_label.setFixedWidth(32)
        self._frame_layout.addWidget(self.status_label, 0, 5, 2, 1, Qt.AlignmentFlag.AlignCenter)
        

    def updateDisplayed(self, displayed: bool):
        self._displayed = displayed
        if displayed:
            self._connectAll()
            self._update_status(self.client_name)
        else:
            self._disconnectAll()

    def _connectAll(self):
        # 🔁 Signaux
        try:
            states.vpn_status_changed.connect(self._update_status)
            return True
        except Exception as e:
            print("An error issued while connecting signals : \n", e)
            return False

    def _disconnectAll(self):
        # 🔁 Signaux
        try:
            states.vpn_status_changed.disconnect(self._update_status)
            return True
        except Exception as e:
            print("An error issued while disconnecting signals : \n", e)
            return False

    def _update_status(self, client=None, status=None):
        if client and self.client_name != client:
            return

        self.vpn_running = is_vpn_container_running(self.container_name)
        # 📍 On garde la même position fixe (0, 1) dans le grid layout
        row, col = 0, 1
        # 🧹 Supprime les deux boutons possibles à cette position (si présents)
        for btn in (self.start_button, self.stop_button):
            self._frame_layout.removeWidget(btn)
            btn.setParent(None)  # important pour Qt

        # 🔁 Insère le bon bouton (sur 2 lignes = rowSpan=2)
        new_button = self.stop_button if self.vpn_running else self.start_button
        self._frame_layout.addWidget(new_button, row, col, 2, 1, Qt.AlignmentFlag.AlignRight)

        # 🟢🔴 Met à jour le label de statut
        self.status_label.updateText("🟢" if self.vpn_running else "🔴")
