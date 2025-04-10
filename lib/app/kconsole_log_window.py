from PySide6.QtWidgets import QVBoxLayout
from core.widgets import KWindow, KHeader, KWidget, KLogsTabs, KButton
from core.labels import Label

class KConsoleLogWindow(KWindow):
    def __init__(self, main_pos):
        super().__init__()
        self.main_pos = main_pos
        self.setFixedSize(600, 400)
        self.update_position()

        # ───────────── Central widget
        self.central_widget = KWidget()
        # ───────────── Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        
        self.header = self._build_header()
        self.installHeader(self.header)

        # # 🏗️ Création des onglets
        self._tabs = KLogsTabs()
        self.main_layout.addWidget(self._tabs)
    
    def _build_header(self):
        """ 🔧 En-tête avec boutons """
        btn_close = KButton("❌")
        btn_close.setFixedSize(30, 30)
        # TODO faire une action pour restaurer une fenêtre
        # TODO elle doit connaitre la dernière fenêtre qui a été hide (compact ou full)
        # TODO elle remplacera le clicked.connect
        btn_close.clicked.connect(self.close)
        return KHeader(self, title=Label.UI_CONSOLE_LOGS_WINDOW_NAME, right_buttons=[btn_close])
        
 
    def update_position(self, main_pos=None):
        """ 📍 Se repositionne en fonction de la fenêtre principale """
        if main_pos:
            self.move(main_pos.x() + 50, main_pos.y() + 50)
        else:
            self.move(self.main_pos.x() + 50, self.main_pos.y() + 50)


