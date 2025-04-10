from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt

from core.widgets import (
    KWindow, KHeader, KWidget, KVBoxLayout,
    KLabel, KButton, KClientFavCard, KLastActionBar
)
from core.manager import states, config
from core.labels import Label
from core.configs import GlobalConfig
from core.actions import KSwitchViewAction

class KCompactMainWindow(KWindow):
    def __init__(self):
        super().__init__()
        self._drag_position = None  # 📦 Stocke la position de départ du drag

        self._fav_widgets: dict[str, KClientFavCard] = {}
        self._displayed_fav_widgets: set[str] = set()

        # ───────────── Central widget 
        central_widget = KWidget()
        central_widget.setThemeStyle("favcard")
        self.setCentralWidget(central_widget)
        # ───────────── Layout principal
        self.main_layout = KVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.header = self._build_header()
        self.installHeader(self.header)

        self.installStatusBar(KLastActionBar())
        
        self.client_zone = KVBoxLayout()
        self.client_zone.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.client_zone)

        self.label_empty = KLabel(Label.UI_MAIN_LABEL_NO_CLIENTS)
        self.label_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_empty.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.client_zone.addWidget(self.label_empty)
        self.populate_clients()
        #states.clients_list_updated.connect(self.populate_clients)
        states.client_favorite_updated.connect(self.populate_clients)

    def _build_header(self):
        """ 🔧 En-tête avec boutons """
        switch_button = KButton(action=KSwitchViewAction())
        switch_button.setFixedSize(30, 30)

        btn_hide = KButton("➖")
        btn_hide.setFixedSize(30, 30)
        # TODO faire une action pour restaurer une fenêtre
        # TODO elle doit connaitre la dernière fenêtre qui a été hide (compact ou full)
        # TODO elle remplacera le clicked.connect
        btn_hide.clicked.connect(self.hide)

        return KHeader(
            self,
            title=Label.UI_MAIN_LABEL_COMPACT_TITLE,
            left_buttons=[btn_hide],
            right_buttons=[switch_button]
        )
    
    def showEvent(self, event):
        size = self.sizeHint()
        self.setFixedSize(size)
        return super().showEvent(event)

    def populate_clients(self):
        """ 🔄 Met à jour la liste avec les clients reçus """
         # 🧹 Retire tous les widgets visuellement, mais ne les détruit pas

        # if not self.label_empty.isHidden():
        #     self.client_zone.removeWidget(self.label_empty)
        #     #self.label_empty.hide()
        print("entering populate_clients of compact")

        while self.client_zone.count():
            item = self.client_zone.takeAt(0)
            widget = item.widget()
            if widget:
                self.client_zone.removeWidget(widget)
                if isinstance(widget, KClientFavCard):
                    widget.updateDisplayed(False)
                
                #widget.hide()
                widget.setParent(None)  # ❌ Ne pas deleteLater                

        # Clear des fav actuels et rebuild
        self._displayed_fav_widgets.clear()

        # Si pas de client ffav
        if not config.hasValue(GlobalConfig.CLIENTS):
            self.client_zone.addWidget(self.label_empty)
            #self.label_empty.show()
            return
        
        # 🧩 Ajout des nouvelles cartes fav
        displayed = 0
        print(self._fav_widgets)
        # Récupération des clients fav uniquement
        for client_name in config.getValue(GlobalConfig.CLIENTS).keys():
            print("Client : ", client_name)
            if displayed >= 3:
                break
            isFav = config.getValue(GlobalConfig.CLIENT_FAVORITE(client_id=client_name))
            print('Client isFav ? ', isFav)
            if not isFav:
                continue
            if client_name not in self._fav_widgets:
                widget = KClientFavCard(client_name=client_name)
                self._fav_widgets[client_name] = widget
            self._displayed_fav_widgets.add(client_name)

        # 🔁 (Re)ajout dans la vue
        for client_name in self._displayed_fav_widgets:
            if(self._fav_widgets[client_name]):
                self._fav_widgets[client_name].updateDisplayed(True)
                self.client_zone.addWidget(self._fav_widgets[client_name])
                #self._fav_widgets[client_name].show()
                
            

