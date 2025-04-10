import os
import platform
import subprocess
import psutil
# from PySide6.QtWidgets import QApplication
# from PySide6.QtGui import QPalette

from core.manager import logger

from core.labels import Label

# 📌 Définition du chemin du fichier de verrouillage
if platform.system() == "Windows":
    LOCKFILE = os.path.join(os.getenv("TEMP"), "vpn_manager.lock")
else:
    LOCKFILE = "/tmp/vpn_manager.lock"

def is_another_instance_running():
    """ 📌 Vérifie si une autre instance de VPN Manager tourne déjà. """
    
    if os.path.exists(LOCKFILE):
        try:
            with open(LOCKFILE, "r") as f:
                processid = f.read().strip()
                pid = int(processid)
            if psutil.pid_exists(pid):
                logger.write(Label.LOG_ALREADY_RUNNING(processid=str(processid)))
                return True

        except Exception:
            pass  # 📌 Ignore les erreurs de lecture du fichier
    return False

def create_lockfile():
    """ 🔐 Crée un fichier de verrouillage avec le PID actuel. """
    with open(LOCKFILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lockfile():
    """ 🗑 Supprime le fichier de verrouillage à la fermeture. """
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

def enable_xhost():
    """ 🔥 Active `xhost +local:` si on est sous Linux avec X11 """
    if platform.system() == "Linux":
        try:
            display = os.environ.get("DISPLAY")
            if display:
                # TODO vérifier d'abord si le host est pas déjà setup, comme ça on exécute pas pour rien
                subprocess.run(["xhost", "+local:"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logger.write(Label.LOG_XHOST_ENABLED)
            else:
                logger.write(Label.LOG_XHOST_DISPLAY_ERROR)
        except Exception as error:
            logger.write(Label.LOG_XHOST_ERROR(error=error))
