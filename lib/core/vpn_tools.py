import subprocess
import os
from core.env import CLIENTS_DIR
from core.manager import logger, tr, states, config
from core.labels import Label
from core.configs import GlobalConfig, ClientConfig

def is_vpn_container_running(container_name):
    """ Vérifie si un conteneur VPN est en cours d'exécution """
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    if container_name in result.stdout:
        return True
    else:
        return False

def start_vpn_container(client_name):
    """ 🚀 Démarre un conteneur VPN avec logging et gestion des erreurs """
    compose_file = os.path.join(CLIENTS_DIR, client_name, "docker-compose.yaml")
    command = ["docker", "compose", "-f", compose_file, "up", "-d"]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        command_str = ' '.join(command)

        # 📝 Log de la commande exécutée
        logger.write(
            Label.LOG_GLOBAL_START_VPN(client_name=client_name),
            client_name,
            f"{tr(Label.LOG_CLIENT_START_VPN)}{command_str}"
        )

        # 📜 Log de la sortie complète (stdout + stderr ensemble)
        full_output = (stdout.strip() + "\n" + stderr.strip()).strip()
        if full_output:
            logger.write(
                None,
                client_name,
                f"{tr(Label.LOG_CLIENT_LOG_STDOUT_LABEL)}\n{full_output}"
            )

        # 🛰️ Émettre le statut en fonction du retour
        if process.returncode == 0:
            states.emit_vpn_status_change(client_name, tr(Label.STATUS_VPN_CONNECTED))
            return True
        else:
            states.emit_vpn_status_change(client_name, tr(Label.STATUS_VPN_ERROR))
            return False
    except Exception as e:
        logger.write(
            Label.LOG_GLOBAL_START_VPN_ERROR(client_name=client_name, error=str(e)),
            client_name,
            Label.LOG_CLIENT_START_VPN_ERROR(error=str(e))
        )
        states.emit_vpn_status_change(client_name, tr(Label.STATUS_VPN_ERROR))
        return False

    
def stop_vpn_container(client_name, delete_image=False):
    """ ⛔ Arrête un conteneur VPN avec logging et gestion des erreurs """
    compose_file = os.path.join(CLIENTS_DIR, client_name, "docker-compose.yaml")
    command = ["docker", "compose", "-f", compose_file, "down"]
    if delete_image:
        command.extend(["--rmi", "local"])

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        command_str = ' '.join(command)

        # 📝 Log de la commande exécutée
        logger.write(
            Label.LOG_GLOBAL_STOP_VPN(client_name=client_name),
            client_name,
            f"{tr(Label.LOG_CLIENT_STOP_VPN)}{command_str}"
        )

        # 📜 Log de la sortie complète (stdout + stderr ensemble)
        full_output = (stdout.strip() + "\n" + stderr.strip()).strip()
        if full_output:
            logger.write(
                None,
                client_name,
                f"{tr(Label.LOG_CLIENT_LOG_STDOUT_LABEL)}\n{full_output}"
            )

        # 🛰️ Émettre le statut
        if process.returncode == 0:
            status = tr(Label.STATUS_VPN_DELETED) if delete_image else tr(Label.STATUS_VPN_DISCONNECTED)
            states.emit_vpn_status_change(client_name, status)
            return True
        else:
            states.emit_vpn_status_change(client_name, tr(Label.STATUS_VPN_ERROR))
            return False
    except Exception as e:
        logger.write(
            Label.LOG_GLOBAL_STOP_VPN_ERROR(client_name=client_name, error=str(e)),
            client_name,
            Label.LOG_CLIENT_STOP_VPN_ERROR(error=str(e))
        )
        states.emit_vpn_status_change(client_name, tr(Label.STATUS_VPN_ERROR))
        return False

def open_vpn_container_shell(container_name, client_name):
    """ Ouvre un terminal graphique dans le conteneur VPN """
    username = client_name.split("@")[0]
    command = [
        "docker", "exec", "-d", "-u", username, "-w", f"/home/{username}", "-it", container_name,
        "xfce4-terminal", "--disable-server"
    ]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        commandstr=' '.join(command)
        #  # 📝 Log de la commande exécutée
        logger.write(
            Label.LOG_GLOBAL_OPEN_SHELL(client_name=client_name),
            client_name,
            f"{tr(Label.LOG_CLIENT_OPEN_SHELL)}{commandstr}"
        )
        # 📜 Log de la sortie complète (stdout + stderr ensemble)
        full_output = (stdout.strip() + "\n" + stderr.strip()).strip()
        if full_output:
            logger.write(
                None,
                client_name,
                f"{tr(Label.LOG_CLIENT_LOG_STDOUT_LABEL)}\n{full_output}"
            )

        return process.returncode == 0  # ✅ True si succès, ❌ False si erreur
    except Exception as e:
        logger.write(
            Label.LOG_GLOBAL_OPEN_SHELL_ERROR(client_name=client_name, error=str(e)),
            client_name,
            Label.LOG_CLIENT_OPEN_SHELL_ERROR(client_name=client_name, error=str(e))
        )
        return False

def open_vpn_container_chromium(container_name, client_name):
    """ Ouvre Chromium dans le conteneur VPN """
    username = client_name.split("@")[0]
    command = [
        "docker", "exec", "-d", "-u", username, "-w", f"/home/{username}", "-it", container_name,
        "chromium"
    ]
    commandstr=' '.join(command)
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        commandstr=' '.join(command)
        #  # 📝 Log de la commande exécutée
        logger.write(
            Label.LOG_GLOBAL_OPEN_CHROMIUM(client_name=client_name),
            client_name,
            f"{tr(Label.LOG_CLIENT_OPEN_CHROMIUM)}{commandstr}"
        )
        # 📜 Log de la sortie complète (stdout + stderr ensemble)
        full_output = (stdout.strip() + "\n" + stderr.strip()).strip()
        if full_output:
            logger.write(
                None,
                client_name,
                f"{tr(Label.LOG_CLIENT_LOG_STDOUT_LABEL)}\n{full_output}"
            )

        return process.returncode == 0  # ✅ True si succès, ❌ False si erreur
    except Exception as e:
        logger.write(
            Label.LOG_GLOBAL_OPEN_CHROMIUM_ERROR(client_name=client_name, error=str(e)),
            client_name,
            Label.LOG_CLIENT_OPEN_CHROMIUM_ERROR(error=str(e))
        )
        return False
    
def stop_non_autostart_vpns():
    """ ⛔ Arrête tous les VPN qui ne sont pas configurés en autostart """
    for client_name in config.getValue(GlobalConfig.CLIENTS).keys():
    # for client_name in config.get_global_config().get("clients", {}):
        #client_config = config.get_client_config(client_name)
        if not config.getValue(ClientConfig.AUTOSTART, client_name) and is_vpn_container_running(client_name.replace("@", "-")):
            stop_vpn_container(client_name)

def start_autostart_vpns():
    """ 🚀 Démarre tous les VPN configurés en autostart """
    for client_name in config.getValue(GlobalConfig.CLIENTS).keys():
    #for client_name in config.get_global_config().get("clients", {}):
        #client_config = config.get_client_config(client_name)
        if config.getValue(ClientConfig.AUTOSTART, client_name) and not is_vpn_container_running(client_name.replace("@", "-")):
            start_vpn_container(client_name)

