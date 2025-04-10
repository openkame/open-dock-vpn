#!/bin/bash
echo "🗑️ Désinstallation VPN-Manager"

ask_remove() {
  read -p "Voulez-vous désinstaller $1 ? (y/n) " choice
  if [[ "$choice" =~ ^[Yy]$ ]]; then
    sudo $2 remove -y "$1"
  fi
}

OS=$(uname -s)
case $OS in
  Linux)
    if command -v apt &>/dev/null; then PM="apt"; fi
    if command -v dnf &>/dev/null; then PM="dnf"; fi
    if command -v pacman &>/dev/null; then PM="pacman"; fi

    for pkg in python3 docker docker-compose-plugin openvpn; do
      ask_remove "$pkg" "$PM"
    done
    ;;
  Darwin)
    for pkg in python3 docker docker-compose openvpn xquartz; do
      read -p "Voulez-vous désinstaller $pkg via Homebrew ? (y/n) " choice
      if [[ "$choice" =~ ^[Yy]$ ]]; then brew uninstall "$pkg"; fi
    done
    ;;
esac

read -p "Supprimer aussi la configuration persistante (home directory VPN) ? ⚠️ (y/n) " delhome
if [[ "$delhome" =~ ^[Yy]$ ]]; then
  rm -rf ./home
fi

