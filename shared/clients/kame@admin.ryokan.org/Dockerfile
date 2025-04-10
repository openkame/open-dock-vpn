# 📌 VPN Client DockerFile
# 📦 Image Alpine avec OpenVPN
FROM alpine:latest

# 🛠 Installer OpenVPN et les outils réseau essentiels
RUN apk add --no-cache \
    sudo \
    openssh \
    net-tools \
    iputils \
    bind-tools \
    jq \
    tcpdump \
    traceroute \
    iproute2 \
    coreutils \
    openvpn \
    bash \
    curl \
    chromium \
    ttf-freefont \
    mesa-dri-gallium \
    mesa-gl \
    mesa-egl \
    xvfb \
    dbus-x11 \
    xauth \
    xdg-utils \
    lxterminal \
    xfce4-terminal \
    adwaita-icon-theme \
    font-noto-emoji

# 🏗 Ajouter les fichiers skel pour root
COPY skel/ /etc/skel/
RUN cp -r /etc/skel/. /root/

# 🔹 Mettre à jour les icônes et polices GTK
RUN gtk-update-icon-cache -f /usr/share/icons/Adwaita

# 🔹 Créer un dossier de configuration OpenVPN
RUN mkdir -p /etc/openvpn
# 📂 Copie du fichier de configuration VPN
COPY kame.ovpn /etc/openvpn/kame.ovpn
# 🔹 Définir les permissions
RUN chmod 600 /etc/openvpn/kame.ovpn

# Créer l'utilisateur non-root 'kame'
ARG USER=kame
ARG UID=1000

RUN addgroup kame && \
    adduser -D -u 1000 -G kame -s /bin/bash kame && \
    echo "kame ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Répertoire home initial
RUN chown -R kame:kame /home/kame

# 🟢 Définir TERM pour activer la couleur
ENV TERM=xterm-256color
# 🔹 Définir l'environnement X11
ENV DISPLAY=:0
# ✅ Désactive les erreurs d'accessibilité
ENV NO_AT_BRIDGE=1
# ✅ Supprime l'erreur de session manager
ENV SESSION_MANAGER=""


# 🏃 Exécuter OpenVPN au démarrage
# 🔹 Script de démarrage pour X11 + OpenVPN + Chrome
CMD openvpn --config /etc/openvpn/kame.ovpn & \
    sleep 5 && \
    echo -e "nameserver 10.8.0.1\nsearch ryokan.org" > /etc/resolv.conf && \
    sudo -u kame bash -c "tail -f /dev/null"
