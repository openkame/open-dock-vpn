from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QTimer
from widgets.kwidgets import KTabWidget, KButton, KWidget, KTextEdit
from core.manager import tr, states, config, logger

from core.labels import Label
from core.configs import GlobalConfig


class KLogsTabs(KTabWidget):
    def __init__(self):
        super().__init__()
        # 📝 Onglet log globale
        self.global_log_tab = KWidget()
        self.global_log_layout = QVBoxLayout()
        self.global_log_tab.setLayout(self.global_log_layout)
        self.global_log_view = KTextEdit()
        self.global_log_view.setReadOnly(True)
        # 🗑 Bouton pour purger les logs globales (pas dans les onglets clients)
        self.clear_btn = KButton(Label.UI_CONSOLE_LOGS_BUTTON_PURGE_GLOBAL_LOGS)
        self.clear_btn.clicked.connect(lambda: self.clear_logs(None))  # 🌍 Aucun client → Log globale
        self.global_log_layout.addWidget(self.global_log_view)
        self.global_log_layout.addWidget(self.clear_btn)
        self.addTab(self.global_log_tab, tr(Label.UI_CONSOLE_LOGS_LABEL_GLOBAL_LOG))
                    
        # 📜 Onglets des logs clients
        self.create_clients_tabs()
        states.lang_updated.connect(self.update_labels)
        self.load_logs()
        states.global_log_updated.connect(self.append_log)
        states.client_log_updated.connect(self.append_log)
        self.currentChanged.connect(self.handle_tab_change)

        # 🔥 On sélectionne la log globale par défaut
        self.setCurrentIndex(0)
    
    def create_clients_tabs(self):
        """ 🔄 Génère dynamiquement les onglets des clients VPN """
        self.client_log_tabs = {}  # 📌 Dictionnaire des vues de logs par client
        self.client_log_views = {}  # 📌 Dictionnaire des vues de logs par client
        self.client_clear_buttons = {} # 📌 Dictionnaire des boutons clear par client
        # Charger la liste des clients depuis la config globale
        for client_name in config.getValue(GlobalConfig.CLIENTS).keys():
            log_tab = KWidget()
            log_layout = QVBoxLayout()
            log_tab.setLayout(log_layout)
            self.client_log_tabs[client_name] = log_tab
            log_view = KTextEdit()
            log_view.setReadOnly(True)
            self.client_log_views[client_name] = log_view
            
            # 🗑 Ajout d'un bouton "Purger"
            clear_btn = KButton(Label.UI_CONSOLE_LOGS_BUTTON_PURGE_CLIENT_LOGS(client_name=client_name))
            clear_btn.clicked.connect(lambda _, c=client_name: self.clear_logs(c))
            log_layout.addWidget(log_view)
            log_layout.addWidget(clear_btn)

            self.client_clear_buttons[client_name] = clear_btn
            self.addTab(log_tab, tr(Label.UI_CONSOLE_LOGS_LABEL_CLIENT_LOG(client_name=client_name)))

        #print(f"✅ Onglets des clients VPN générés : {list(self.client_log_views.keys())}")
    
    def update_labels(self):
        """ 🔄 Met à jour les titres des onglets après un changement de langue """
        GLOBAL_TAB_INDEX = 0
        self.setTabText(GLOBAL_TAB_INDEX, tr(Label.UI_CONSOLE_LOGS_LABEL_GLOBAL_LOG))

        for index, (client_name, _) in enumerate(self.client_log_tabs.items(), start=1):
            self.setTabText(index, tr(Label.UI_CONSOLE_LOGS_LABEL_CLIENT_LOG(client_name=client_name)))
    
    def handle_tab_change(self, index):
        """ 📌 Met à jour le scroll en bas lors du changement d'onglet """
        if index == 0:
            self.initScrollBar(self.global_log_view)  # 🌍 Log globale
        else:
            client_name = list(self.client_log_views.keys())[index - 1]  # 🔹 Trouver le bon client
            log_view = self.client_log_views.get(client_name)
            if log_view:
                self.initScrollBar(log_view)


    def initScrollBar(self, view: KTextEdit):
        # 🚀 Forcer le scroll après affichage
        # 🔽 Scroll tout en bas
        QTimer.singleShot(0, \
            lambda: view.verticalScrollBar()
            .setSliderPosition(view.verticalScrollBar().maximum()))


    def load_logs(self):
        """ 📖 Charge et affiche les logs """
        logs = logger.read()
        self.global_log_view.setPlainText("".join(logs))
        self.initScrollBar(self.global_log_view)

        # 🔹 Charger les logs des clients
        for client_name, log_view in self.client_log_views.items():
            logs = logger.read(client_name)
            log_view.setPlainText("".join(logs))

    def append_log(self, log_message, client_name=None):
        target_view = None
        if not client_name:
            target_view = self.global_log_view
        else:
            # 🔹 Log d'un client VPN spécifique
            target_view = self.client_log_views.get(client_name)
            if not target_view:
                logger.write(Label.LOG_CLIENT_LOG_APPEND_ERROR(client_name=client_name))
                return
        """ 🔥 Ajoute un message de log en temps réel """
        clean_log = log_message.strip()
        target_view.append(clean_log)
        target_view.verticalScrollBar().setSliderPosition(target_view.verticalScrollBar().maximum())

    def clear_logs(self, client_name=None):
        target_view = None
        """ 🗑 Supprime les logs du fichier et vide l'affichage """
        if not client_name:
            target_view = self.global_log_view
        else:
            # 🔹 Log d'un client VPN spécifique
            target_view = self.client_log_views.get(client_name)
            if not target_view:
                logger.write(Label.LOG_CLIENT_LOG_APPEND_ERROR(client_name=client_name))
                return
        logger.delete_logs(client_name)
        target_view.clear()