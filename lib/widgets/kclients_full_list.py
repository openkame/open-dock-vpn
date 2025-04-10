from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import Qt

from widgets.kclient_card import KClientFullCard
from widgets.kwidgets import KWidget, KLabel, KScrollArea
from widgets.klayouts import KVBoxLayout

from core.manager import states, config
from core.labels import Label
from core.manager import config
from core.configs import GlobalConfig

class KClientsFullList(KScrollArea):
    def __init__(self):
        super().__init__(None, "clients_full_list")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self._scroll_container = KWidget()
        self._scroll_layout = KVBoxLayout(self._scroll_container)
        #self._scroll_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._scroll_layout.setSpacing(6)
        self._scroll_layout.setContentsMargins(8, 8, 8, 8)
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWidget(self._scroll_container)

        self._client_widgets: dict[str, KClientFullCard] = {}
        self._displayed_clients: set[str] = set()
        states.clients_list_updated.connect(self.populate_clients)
        #states.lang_updated.connect(self._resizeOnContent)

        self.populate_clients()
        print(self._scroll_container.sizeHint())

    def _resizeOnContent(self):
        self.setFixedSize(self.viewport().size())
        #self.setFixedWidth(self.viewport().width())

    def showEvent(self, event):
        # 🔧 Force la largeur du widget contenu pour éviter les truncations
        #self._resizeOnContent()
        return super().showEvent(event)

    def populate_clients(self):
        """ 🔄 Met à jour la liste avec les clients reçus """
         # 🧹 Retire tous les widgets visuellement, mais ne les détruit pas
        while self._scroll_layout.count():
            item = self._scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.updateDisplayed(False)
                widget.setParent(None)  # ❌ Ne pas deleteLater

        self._displayed_clients.clear()

        # 🧩 Ajout des nouvelles cartes
        if not config.hasValue(GlobalConfig.CLIENTS):
            self._scroll_layout.addWidget(KLabel(Label.UI_MAIN_LABEL_NO_CLIENTS))
            return

        for client_name in config.getValue(GlobalConfig.CLIENTS).keys():
            if client_name not in self._client_widgets:
                widget = KClientFullCard(client_name=client_name)
                self._client_widgets[client_name] = widget

            self._client_widgets[client_name].updateDisplayed(True)
            # 🔁 (Re)ajout dans la vue
            self._scroll_layout.addWidget(self._client_widgets[client_name])

        self._resizeOnContent()