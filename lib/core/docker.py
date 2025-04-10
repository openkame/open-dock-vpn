import os
from jinja2 import Environment, FileSystemLoader
from core.env import TEMPLATES_DIR, CLIENTS_DIR
from core.manager import manager
from core.labels import Label

def generate_docker_files(username, vpn_name, domain, vpn_profile):
    profile_template_dir = os.path.join(TEMPLATES_DIR, vpn_profile)
    env = Environment(loader=FileSystemLoader(profile_template_dir))
    """
    Génère le Dockerfile et docker-compose.yaml pour un client VPN.
    """
    client_name = f"{username}@{vpn_name}.{domain}"
    client_dir = os.path.join(CLIENTS_DIR, client_name)
    os.makedirs(client_dir, exist_ok=True)

    # Définition des variables pour le template
    template_vars = {
        "username": username,
        "vpn_name": vpn_name,
        "domain": domain,
        "container_name": f"{username}-{vpn_name}.{domain}",
        "host_name": f"vpn{vpn_name}{domain}"
    }

    # Génération du Dockerfile
    dockerfile_template = env.get_template("dockerfile.j2")
    with open(os.path.join(client_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_template.render(template_vars))

    # Génération du docker-compose.yaml
    compose_template = env.get_template("docker-compose.j2")
    with open(os.path.join(client_dir, "docker-compose.yaml"), "w") as f:
        f.write(compose_template.render(template_vars))

    manager.logger.write(Label.LOG_DOCK_FILES_GENERATED(
        client_name=client_name,
        client_dir=client_dir
    ))

