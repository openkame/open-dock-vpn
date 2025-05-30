#!/usr/bin/env python
import sys, io, os
from core.manager import manager
from PySide6.QtWidgets import QApplication
from app.kapp_controller import KAppController

from core.sys_utils import is_another_instance_running, create_lockfile, enable_xhost
from core.exttools_manager import ExternalToolsManager

def main():
    # 📌 Vérifie si une autre instance tourne déjà
    if is_another_instance_running():
        sys.exit(1)  # ⛔ Quitte immédiatement

    ExternalToolsManager.is_vcxsrv_running()
    ExternalToolsManager.is_wsl_running()
    ExternalToolsManager.is_docker_running()

    # Initilisation de tous les managers
    manager.initialize()

    # 📌 Création du verrou pour cette instance
    create_lockfile()
    enable_xhost()  # 🔥 Activation automatique de `xhost`
    app = QApplication(sys.argv)
    # 🏗️ Création de la fenêtre principale
    controller = KAppController()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

