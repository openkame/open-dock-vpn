import os
import platform
import subprocess
from core.env import BASE_DIR, APP_ICON_PATH

def get_python_command():
    """ 📌 Récupère la commande Python correcte selon l'OS """
    if platform.system() == "Windows":
        return f"{BASE_DIR}\\lib\\venv\\Scripts\\python.exe"
    return f"{BASE_DIR}/lib/venv/bin/python3"

def get_vpn_manager_command():
    """ 📌 Commande pour exécuter `vpn_manager.py` avec l'environnement activé """
    return f'"{get_python_command()}" "{BASE_DIR}/lib/vpn-manager.py"'

def get_linux_menu_path():
    """ 🔍 Détecte le chemin où placer un raccourci dans le menu Linux """
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    
    paths = {
        "kde": "~/.local/share/applications/",
        "plasma": "~/.local/share/applications/",
        "gnome": "~/.local/share/applications/",
        "xfce": "~/.local/share/applications/",
        "lxqt": "~/.local/share/applications/",
        "mate": "~/.local/share/applications/",
        "cinnamon": "~/.local/share/applications/",
        "deepin": "~/.local/share/applications/",
    }
    
    return os.path.expanduser(paths.get(desktop_env, "~/.local/share/applications/"))

def get_linux_autostart_path():
    """ 🔍 Détecte le chemin du dossier autostart selon l'environnement graphique sous Linux """
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

    paths = {
        "kde": "~/.config/autostart/",
        "plasma": "~/.config/autostart/",
        "gnome": "~/.config/autostart/",
        "xfce": "~/.config/autostart/",
        "lxqt": "~/.config/autostart/",
        "mate": "~/.config/autostart/",
        "cinnamon": "~/.config/autostart/",
        "deepin": "~/.config/autostart/",
    }

    # Retourne le chemin correspondant à l'ENV détecté, sinon un chemin générique
    return os.path.expanduser(paths.get(desktop_env, "~/.config/autostart/"))


def create_linux_shortcut():
    """ 🏗️ Crée un raccourci `.desktop` sous Linux """
    shortcut_path = os.path.join(BASE_DIR, "VPN-Manager.desktop")
    if os.path.exists(shortcut_path):
        print("✅ Raccourci Linux déjà existant.")
        return  # ✅ Déjà existant, on ne recrée pas   

    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=VPN Manager
Exec={get_vpn_manager_command()}
Icon={APP_ICON_PATH}
Path={BASE_DIR}
Terminal=false
"""
    with open(shortcut_path, "w") as f:
        f.write(content)
    os.chmod(shortcut_path, 0o755)  # 🔥 Permet l'exécution du raccourci
    print(f"🛠️ Pour ajouter au menu, placez le raccourci dans : {get_linux_menu_path()}")
    print(f"🛠️ Pour lancer l'application au démarrage, placez le raccourci dans : {get_linux_autostart_path()}")


def create_windows_shortcut():
    """ 🏗️ Crée un raccourci `.lnk` sous Windows """
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print("⚠️ Impossible de créer le raccourci Windows : module `winshell` manquant.")
        return

    shortcut_path = os.path.join(BASE_DIR, "VPN-Manager.lnk")
    if os.path.exists(shortcut_path):
        return  # ✅ Déjà existant

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = get_python_command()
    shortcut.Arguments = f'"{BASE_DIR}\\lib\\vpn-manager.py"'
    shortcut.WorkingDirectory = BASE_DIR
    shortcut.IconLocation = APP_ICON_PATH  # Icône générique
    shortcut.Save()
    WINDOWS_MENU_PATH = os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs")
    print(f"🛠️ Pour ajouter au menu, placez le raccourci dans : {WINDOWS_MENU_PATH}")
    print("🛠️ Pour un démarrage automatique sous Windows, placez ce raccourci dans `%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup`")


def create_mac_shortcut():
    """ 🏗️ Crée un alias sous macOS """
    shortcut_path = os.path.join(BASE_DIR, "VPN-Manager.alias")
    if os.path.exists(shortcut_path):
        return  # ✅ Déjà existant

    script = f'''
    osascript -e 'tell application "Finder" to make alias file to POSIX file "{get_vpn_manager_command()}" at POSIX file "{shortcut_path}"'
    '''
    subprocess.run(script, shell=True)
    MAC_MENU_PATH = os.path.expanduser("~/Applications/")
    print(f"🛠️ Pour ajouter au menu, placez le raccourci dans : {MAC_MENU_PATH}")
    print("🛠️ Pour un démarrage automatique sous macOS, placez le raccourci dans `~/Library/LaunchAgents/`")


def create_global_shortcut():
    """ 📌 Crée un raccourci pour VPN Manager selon l'OS """
    system = platform.system()
    if system == "Linux":
        create_linux_shortcut()
    elif system == "Windows":
        create_windows_shortcut()
    elif system == "Darwin":  # macOS
        create_mac_shortcut()


create_global_shortcut()