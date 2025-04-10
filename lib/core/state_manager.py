from PySide6.QtCore import QObject, Signal
from core.labels import Label

class StateManager(QObject):
    """ 🎛️ Gestionnaire de l'état global de l'application """
    switch_view_requested = Signal() # 🔄 Signal pour notifier qu'on switch compact/full view
    hide_view_requested = Signal(str) # 🔄 Signal pour notifier qu'un widget demande à être "hide"
    widget_shown = Signal(object) # 🔄 Signal pour notifier qu'un widget s'affiche
    quit_app_requested = Signal() # 🔄 Signal pour notifier que l'utilisateur veut quitter l'application
    open_logs_requested = Signal() # 🔄 Signal pour notifier l'ouverture des logs
    open_add_client_requested = Signal() # 🔄 Signal pour notifier l'ouverture du modal Ajout d'un client
    open_profiles_manager_requested = Signal() # 🔄 Signal pour notifier l'ouverture du profiles manager
    manager_status_changed = Signal(str) # 🔄 Signal pour notifier que vpn-manager a changé de statut
    lang_updated = Signal()  # 🔄 Signal pour notifier le changement de langue
    theme_updated = Signal(str) # 🔄 Signal pour notifier un changement de thème (mode, name)
    theme_mode_updated = Signal(str) # 🔄 Signal pour notifier un changement de thème (mode)
    clients_list_updated = Signal() # 🔄 Signal pour notifier un changement dans la liste du vpn (add_client ou delete ie)
    client_loading_requested = Signal(str) # (client_name) 🔄 Signal pour notifier une demande chargement des infos d'un client 
    vpn_status_changed = Signal(str, str)  # (client_name, status) 🔄 Signal pour notifier un changement de statut sur un VPN
    client_favorite_updated = Signal(str, bool) # (client_name, isFavorite) 🔄 Signal pour notifier le toggle du favoriteCheckbox
    client_log_updated = Signal(str, str)  # (log_message, client_name)
    global_log_updated = Signal(str)  # (log_message)
    action_triggered = Signal(Label) # (Label) correspond au message envoyé par la dernière action effectuée

    def __init__(self, manager):
        self.manager = manager
        super().__init__()

    """ 🔄 Émission des signaux en fonction pour customisation si besoin est """
    def emit_switch_view_request(self):
        self.switch_view_requested.emit()
        
    def emit_hide_view_requested(self, viewName):
        self.hide_view_requested.emit(viewName)

    def emit_theme_update(self, theme):
        self.theme_updated.emit(theme)
    
    def emit_widget_show(self, object):
        self.widget_shown.emit(object)
        
    def emit_theme_mode_update(self, mode):
        self.theme_mode_updated.emit(mode)

    def emit_client_log_update(self, log_message, client_name):
        self.client_log_updated.emit(log_message, client_name)
    
    def emit_global_log_update(self, log_message):
        self.global_log_updated.emit(log_message)
    
    def emit_open_logs_request(self):
        self.open_logs_requested.emit()
    
    def emit_open_add_client_request(self):
        self.open_add_client_requested.emit()
    
    def emit_open_profiles_manager_request(self):
        self.open_profiles_manager_requested.emit()

    def emit_quit_app_request(self):
        self.quit_app_requested.emit()

    def emit_manager_status_change(self, status):
        self.manager_status_changed.emit(status)

    def emit_lang_update(self):
        self.lang_updated.emit()

    def emit_clients_list_update(self):
        self.clients_list_updated.emit()
    
    def emit_client_loading_request(self, client_name):
        self.client_loading_requested.emit(client_name)

    def emit_vpn_status_change(self, client_name, status):
        self.vpn_status_changed.emit(client_name, status)
    
    def emit_client_favorite_update(self, client_name, status):
        self.client_favorite_updated.emit(client_name, status)
    
    def emit_action_trigger(self, action_message:Label):
        self.action_triggered.emit(action_message)

