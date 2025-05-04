import os, sys
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

def get_docker_cmd():
    system = platform.system()
    if system == "Windows":
        return ["wsl", "-d", "vpn-manager", "docker"]
    else:
        return ["docker"]
    
def convert_path_to_wsl(path: str) -> str:
    """Convertit un chemin Windows vers un chemin accessible depuis WSL"""
    if platform.system() != "Windows":
        return path  # Pas besoin de conversion sous Linux/macOS

    path = path.replace("\\", "/")
    # Appelle `wsl wslpath` pour convertir le chemin
    try:
        result = subprocess.run(
            ["wsl", "-d", "vpn-manager", "wslpath", "-a", f"{path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur conversion chemin WSL : {e.stderr}")
        return path

def get_subprocess_no_window_args():
    """🚫 No window on Windows when using subprocess (for pythonw.exe calls)"""
    if sys.platform == "win32":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return {"startupinfo": si}
    return {}

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
