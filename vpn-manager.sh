#!/bin/bash
set -e

# 🎨 Définition des couleurs ANSI↲
GREEN="\e[32m"
BLUE="\e[34m"
RED="\e[31m"
CYAN="\e[36m"
WHITE="\e[37m"
YELLOW="\e[33m"
MAGENTA="\e[35m"
RESET="\e[0m"

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LIB_DIR="$BASE_DIR/lib"
VENV_DIR="$LIB_DIR/venv"
SHARED_DIR="$BASE_DIR/shared"

echo -e "🚀 ${CYAN}VPN-Manager Wrapper ${BLUE}(Linux/macOS)${RESET}"

OS=$(uname -s)
echo -e "🔹 ${CYAN}OS détecté : ${BLUE}${OS}${RESET}"

PRE_REQS=(python3 wmdocker)
MISSING_REQS=()

check_missing() {
    if ! command -v "$1" &>/dev/null; then
        echo -e "🔸 ${RED}Pré-requis manquant : ${1}${RESET}"
        MISSING_REQS+=("$1")
    else
        echo -e "✅ ${GREEN}$1 déjà installé.${RESET}"
    fi
}

# Vérification des prérequis de base
for cmd in "${PRE_REQS[@]}"; do
    check_missing "$cmd"
done

# Vérification spéciale pour docker compose
if ! docker compose version &>/dev/null; then
    echo -e "🔸 ${YELLOW}Pré-requis manquant : docker compose${RESET}"
    if [ "$OS" = "Linux" ]; then
        MISSING_REQS+=("docker-compose")
    else
        MISSING_REQS+=("docker-compose")
    fi
else
    echo -e "✅ ${GREEN}docker compose opérationnel.${RESET}"
fi

# Installation conditionnelle selon OS
if [ ${#MISSING_REQS[@]} -gt 0 ]; then
    echo -e "🔹 ${CYAN}Installation des prérequis : ${MISSING_REQS[*]}...${RESET}"

    if [ "$OS" = "Linux" ]; then
        if command -v apt &>/dev/null; then
            sudo apt update
			PKGINSTALLER="apt install -y"
        elif command -v dnf &>/dev/null; then
			PKGINSTALLER="dnf install -y"
        elif command -v pacman &>/dev/null; then
			PKGINSTALLER="pacman -Sy --needed"
        else
			echo -e "${YELLOW} KO${RESET}"
            echo -e "⚠️ Gestionnaire de paquets inconnu. Merci d'installer manuellement : ${MAGENTA}${MISSING_REQS[*]}${RESET}"
            exit 1
        fi

		if sudo $PKGINSTALLER "${MISSING_REQS[@]}" &> /dev/null; then
			echo -e "${GREEN} OK${RESET}"
		else
			echo -e "${RED} KO${RESET}"
			echo -e " ${RED}Un problème est survenu pendant l'installation des prérequis...${RESET}"
			exit 1
		fi

        # Vérification groupe docker Linux
        if ! groups "$USER" | grep -q docker; then
            echo "🔸 ${CYAN}Ajout de $USER au groupe docker...${RESET}"
            sudo usermod -aG docker "$USER"
            echo -e "⚠️ ${YELLOW}Déconnectez-vous puis reconnectez-vous pour activer le groupe docker.${RESET}"
        else
            echo -e "✅ ${GREEN}$USER déjà membre du groupe docker.${RESET}"
        fi

        # Activer Docker
        sudo systemctl enable --now docker

    elif [ "$OS" = "Darwin" ]; then
        if ! command -v brew &>/dev/null; then
            echo "🍺 Veuillez installer Homebrew d'abord : https://brew.sh/"
            exit 1
        fi
        brew install "${MISSING_REQS[@]}" xquartz

        # Démarrer Docker Desktop et XQuartz
        open -a Docker
        open -a XQuartz
        xhost +127.0.0.1
    else
        echo -e "⚠️ ${RED}OS non supporté : $OS${RESET}"
        exit 1
    fi
else
    echo -e "✅ ${GREEN}Aucun prérequis manquant.${RESET}"
fi


# 🛠 Vérification et création de l'environnement virtuel Python
echo -e -n "🔍 ${CYAN}Vérification de l'environnement virtuel Python...${RESET}"
if [ -d "$VENV_DIR" ]; then
    # ✅ Vérifie si le venv est fonctionnel
    if ! "$VENV_DIR/bin/python3" -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        echo -e " ${RED}KO${RESET}"
        echo -e "⚠️ ${RED}L'environnement virtuel semble corrompu. Suppression et recréation.${RESET}"
        rm -rf "$VENV_DIR"
    else
        echo -e " ${GREEN}OK${RESET}"
    fi
fi
# 📌 Création du venv si nécessaire
if [ ! -d "$VENV_DIR" ]; then
    echo -e -n "🔹 ${CYAN}Création de l'environnement virtuel Python...${RESET}"
    if python3 -m venv "$VENV_DIR" &> /dev/null; then
        echo -e " ${GREEN}OK${RESET}"
    else
        echo -e " ${RED}KO${RESET}"
        exit 1
    fi
fi
# 🌍 Activation de l'environnement virtuel
echo -e -n "🔹 ${CYAN}Activation de l'environnement virtuel...${RESET}"
source "$VENV_DIR/bin/activate"
echo -e " ${GREEN}done${RESET}"
# 🔥 Vérification de `pip`
if ! "$VENV_DIR/bin/python" -m pip --version &> /dev/null; then
    echo -e -n "⚠️ ${RED}pip n'est pas installé correctement. Installation...${RESET}"
    if python -m ensurepip --default-pip &> /dev/null; then
        echo -e " ${GREEN}OK${RESET}"
    else
        echo -e " ${RED}KO${RESET}"
    fi
fi
# 📦 Mise à jour de python et ses dépendances si nécessaire
OUTDATED=$(pip list --outdated 2>/dev/null)
if [ -n "$OUTDATED" ]; then
    echo -e -n "🔄 ${CYAN}Mise à jour de l'environnement...${RESET}"
    if pip install -U --no-input -r $LIB_DIR/requirements.txt &> /dev/null; then
        echo -e " ${GREEN}OK${RESET}"
    else
        echo -e " ${RED}KO${RESET}"
        exit 1
    fi
fi

# 📌 Installation des dépendances Python (ne réinstalle pas si déjà présentes)
echo -e -n "🔍 ${CYAN}Vérification et installation des dépendances python...${RESET}"
if ! python3 "$LIB_DIR/test_imports.py"; then
    if pip install -r $LIB_DIR/requirements.txt &> /dev/null; then
        echo -e " ${GREEN}OK${RESET}"
    else
        echo -e " ${RED}KO${RESET}"
        exit 1
    fi
else
    echo -e " ${GREEN}OK${RESET}"
fi

# 📌 Création du raccourci global au besoin
python3 "$LIB_DIR/shortcut_manager.py"

# Lancement du script Python avec pass-through des arguments
python3 "$LIB_DIR/vpn-manager.py"


