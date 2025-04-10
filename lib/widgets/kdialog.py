from PySide6.QtWidgets import QDialog, QVBoxLayout, QFrame, QSizeGrip
from PySide6.QtCore import Qt
from widgets.kmixins import KThemeMixin

from widgets.kwidgets import KMenuBar, KStatusBar
from widgets.kheader import KHeader
from widgets.krootmenu_bar import KRootMenuBar
from widgets.krootstatus_bar import KRootStatusBar

from core.manager import states
from core.labels import Label

class KDialog(QDialog, KThemeMixin):
    """ 🏷️ KDialog customisé avec thème et traduction dynamiques """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        KThemeMixin.__init__(self, style_name="root_window")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ───── Layout Principal correspondant à la fenêtre
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # # ───── Zone Centrale (à surcharger par la vue réelle)
        self._central_frame = QFrame()
        self._central_frame.setObjectName("central_frame")
        self._central_layout = QVBoxLayout(self._central_frame)
        self._central_layout.setContentsMargins(0, 0, 0, 0)
        self._central_layout.setSpacing(0)
        self._layout.addWidget(self._central_frame, 1)

        self._header = None
        self._status_bar = None
        self._central_widget = None

        self.size_grip = QSizeGrip(self)
        self.size_grip.setVisible(False)

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

    def toggle_grip(self, state: bool):
        self.size_grip.setVisible(state)
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)