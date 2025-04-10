from PySide6.QtWidgets import QSizePolicy, QSpacerItem

from core.widgets import (
    KWindow, KWidget,
    KClientsFullList, KClientPanel,
    KVBoxLayout, KHBoxLayout
)

from app.kadd_client_dialog import KAddClientDialog
from app.kprofiles_manager_dialog import KProfilesManagerDialog
from app.kconsole_log_window import KConsoleLogWindow

from core.manager import states

class KFullMainWindow(KWindow):
    def __init__(self):
        super().__init__()
        # # ❌ Désactive le redimensionnement
        #self.setFixedSize(1000, 600)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # ───────────── Central widget 
        central_widget = KWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # ───────────── Main layout
        main_layout = KHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        # Installation des composants
        self.installHeader()
        self.installStatusBar()
        self.installSystray()

        # 🧱 Placeholder client list
        self.clients_list = KClientsFullList()
        main_layout.addWidget(self.clients_list)
        #self.clients_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # 🧱 Placeholder client panel
        self.client_panel = KClientPanel()
        #self.client_panel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        #client_panel.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.client_panel)

        # 📡 Écoute du signal de sortie
        states.open_add_client_requested.connect(self.open_add_client)
        states.open_profiles_manager_requested.connect(self.open_manage_profiles)
        states.open_logs_requested.connect(self.open_log_console)

        # 📌 Initialisation des fenêtres modales
        self.addclient = KAddClientDialog(self.pos(), self)
        self.profiles_mgr_dialog = KProfilesManagerDialog(self.pos(), self)
        self.log_console = KConsoleLogWindow(self.pos())
        
        states.lang_updated.connect(self._onContentUpdate)
        #self._onContentUpdate()
        
    def showEvent(self, event):
        self._onContentUpdate()
        return super().showEvent(event)
    
    def _onContentUpdate(self):
        size = self.sizeHint()
        print(size)
        print(self.clients_list.sizeHint(), self.client_panel.sizeHint())
        #self.setFixedSize(size)

    def closeEvent(self, event):
        """ 🛑 Intercepte la fermeture et cache la fenêtre au lieu de quitter """
        event.ignore()
        self.hide()
    
    def open_manage_profiles(self):
        """ Ouvre le gestionnaire de profils VPN """
        self.profiles_mgr_dialog.update_position(self.pos())
        self.profiles_mgr_dialog.exec()

    def open_add_client(self):
        """ Ouvre la fenêtre d'ajout d'un client VPN """
        self.addclient.update_position(self.pos())
        self.addclient.exec()
        # Mise à jour du tableau après ajout d'un VPN
        states.emit_clients_list_update()
    
    def open_log_console(self):
        """ Ouvre la fenêtre de logs """
        self.log_console.update_position(self.pos())
        self.log_console.show()

