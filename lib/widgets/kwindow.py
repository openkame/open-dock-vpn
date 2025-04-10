from PySide6.QtWidgets import QSizeGrip
from PySide6.QtCore import Qt

from widgets.kwidgets import KWidget, KMenuBar, KStatusBar
from widgets.kframe import KFrame
from widgets.klayouts import KVBoxLayout
from widgets.kheader import KHeader
from widgets.krootmenu_bar import KRootMenuBar
from widgets.krootstatus_bar import KRootStatusBar
from widgets.krootsystray import KRootSystemTray

from core.labels import Label

class KWindow(KWidget):
    """🪟 Fenêtre principale sans QMainWindow, full custom"""
    def __init__(self):
        super().__init__()
        self.setThemeStyle("root_window")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Window |
            Qt.WindowType.CustomizeWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ───── Layout Principal correspondant à la fenêtre
        self._layout = KVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # # ───── Zone Centrale (à surcharger par la vue réelle)
        self._central_frame = KFrame()
        self._central_frame.setObjectName("central_frame")
        self._central_layout = KVBoxLayout(self._central_frame)
        self._central_layout.setContentsMargins(0, 0, 0, 0)
        self._central_layout.setSpacing(0)
        self._layout.addWidget(self._central_frame, 1)

        self._header = None
        self._status_bar = None
        self._central_widget = None

        # self.size_grip = QSizeGrip(self)
        # self.size_grip.setVisible(False)

    def setCentralWidget(self, widget):
        if self._central_widget:
            self._central_layout.removeWidget(self._central_widget)
            self._central_widget.deleteLater()

        self._central_widget = widget
        if self._central_layout.isEmpty():
            self._central_layout.addWidget(widget)
        else:
            self._central_layout.insertWidget(1, widget)  # Toujours au centre

    def installHeader(self, header:KMenuBar|KHeader|None=None):
        if self._header:
            return  # Header déjà installé
        self._header = header if header else KRootMenuBar(self)
        self._central_layout.insertWidget(0, self._header)

    def installStatusBar(self, status_bar:KStatusBar|None=None):
        if self._status_bar:
            return
        self._status_bar = status_bar if status_bar else KRootStatusBar(None, Label.STATUS_MANAGER_READY)
        self._central_layout.addWidget(self._status_bar)

    def installSystray(self, systray=None):
        self._systray = systray if systray else KRootSystemTray(self)

    def toggle_grip(self, state: bool):
        self.size_grip.setVisible(state)
