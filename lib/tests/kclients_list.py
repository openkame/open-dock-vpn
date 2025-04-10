from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from kclient_card import KClientFullCard  # Assure-toi d'avoir cette classe dans un fichier séparé

class KClientsFullList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def populate_clients(self, clients: list|None = None):
        """ 🔄 Met à jour la liste avec les clients reçus """
        # 🧹 Nettoyage
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 🧩 Ajout des nouvelles cartes
        if not clients:
            self.layout.addWidget(QLabel("No VPN clients found"))
            return

        for client in clients:
            card = KClientFullCard(
                client_name=client["name"],
                status_icon=client["status"],
                autostart=client["autostart"],
                is_favorite=client["favorite"]
            )
            self.layout.addWidget(card)
