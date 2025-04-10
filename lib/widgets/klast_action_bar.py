from PySide6.QtCore import QTimer
from widgets.kwidgets import KStatusBar
from core.labels import Label
from core.manager import states

class KLastActionBar(KStatusBar):

    """📌 Barre de statut avec effacement automatique du message"""
    def __init__(self, parent=None, timeout=5000):
        KStatusBar.__init__(self, parent)
        self._timeout = timeout
        self._default_label = Label.ACTIONS_NO_RECENT_ACTION  # "Pas d'action récente"
        self.setFixedHeight(32)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._clearStatus)

        # Initialise avec le label par défaut
        self.updateText(self._default_label)
        states.action_triggered.connect(self._setStatus)
        

    def _setStatus(self, message: Label|str):
        """🟢 Affiche un message temporaire dans la statusbar"""
        self.updateText(message)
        self._timer.start(self._timeout)

    def _clearStatus(self):
        """🧹 Remet le message par défaut"""
        self.updateText(self._default_label)