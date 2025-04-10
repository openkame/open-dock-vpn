import sys
from PySide6.QtWidgets import QApplication

from core.sys_utils import remove_lockfile
from core.vpn_tools import stop_non_autostart_vpns
from core.manager import states, logger
from core.widgets import KWidget
from core.labels import Label

from app.kfull_main_window import KFullMainWindow
from app.kcompact_main_window import KCompactMainWindow

class KAppController(KWidget):
    def __init__(self):
        super().__init__()

        # On ne montre JAMAIS ce widget, mais il sert de parent logique
        self.full_view = KFullMainWindow()
        self.compact_view = KCompactMainWindow()    

        # Démarrage sur la full view
        self.compact_view.hide()
        self.full_view.show()
        self.active_view = self.full_view

        # Un seul signal pour le switch
        states.switch_view_requested.connect(self.toggle_view)
        # 📡 Écoute du signal de sortie
        states.quit_app_requested.connect(self.quit_app)

    def toggle_view(self):
        if self.full_view.isVisible():
            self.active_view = self.compact_view
            self.full_view.showMinimized()
            self.compact_view.show()
            self.compact_view.raise_()
            self.compact_view.activateWindow()

            self.full_view.hide()
        else:
            self.active_view = self.full_view
            self.compact_view.showMinimized()
            self.full_view.show()
            self.full_view.raise_()
            self.full_view.activateWindow()
            self.compact_view.hide()
    
    def quit_app(self):
        """ ❌ Ferme réellement l'application et toutes les fenêtres ouvertes """
        logger.write(Label.LOG_CLOSE_APPLICATION)
        stop_non_autostart_vpns()

        # 🔥 Fermer toutes les fenêtres ouvertes
        for widget in QApplication.instance().topLevelWidgets():
            if widget.isVisible():
                widget.close()

        # self.tray_icon.hide()
        # 📌 Suppression du verrou à la fermeture
        import atexit
        atexit.register(remove_lockfile)
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = KAppController()
    sys.exit(app.exec())
