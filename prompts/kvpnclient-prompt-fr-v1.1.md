```markdown
# 🧠 Prompt Template - Projet : `kvpnclient` — client VPN multiplateforme basé sur Docker et Python/Qt

## 🔖 CONTEXTE
> Développement d’un client VPN en python/QtPy open source Multiplateforme via Docker.
> Python/Qt :
- Créer un 'venv' dans le dossier lib de l'application python
- Utilises les widgets Qt pour la partie GUI
- toutes les classes Qt de sont héritées et mixées pour gérer les locales, la config et les thèmes en entière autonomie.

> Linux : utilises Docker/Python depuis les installations systèmes directement
> Windows : utilises Winget pour installer VcXsrv/python et WSL pour installer et utiliser docker, installeur NSI
> Mac : pas encore implémenté/testé

> Objectif : automatiser la connexion VPN + configuration réseau + création d’un installateur.

### ✅ TODO Liste (mise à jour manuellement) pour la V1
#### 🛠️ Global
- [x] Dockerfile + docker-compose fonctionnel avec `openvpn` (template admin-default créé et fonctionnel, déploie xterm and chrome sur le vpn)
- [x] Ajout support forwarding X11 Linux → Windows (WSL)
- [x] Labéliser les locales : utilisation d'énum. python pour chaque chaine de caractères afin d'aller chercher le texte dans la langue configurée
- [x] Labéliser la config : utilisation d'énum. python pour les configs (chaque entrée dans les fichier JSON est un énum)
- [ ] Labéliser les themes : utilisation d'énum. python pour chaque classe visuelle afin de personnaliser l'affichage grâce au qss trouvé dans le JSON correspondant au theme
- [ ] Débugger la suppression des objets Qt en python (desynchro entre gc de python et l'allocation mémoire du code C++ de PyQt)
- [ ] Rework les classes kwidgets pour séparer classes abstraites et objects finaux (refonte de l'arbo des fichiers)
- [ ] Rework la gestion des "messages applicatifs" afin que tout soit centralisé dans une classe manager (ie exchanges_manager.py, pas grand chose à faire, on utilises déjà des signaux)
    -> On a déjà des classes managers pour chaque point à gérer dans l'appli (locales, themes, fichiers, logs, configs, exttools)
    -> donc celle-ci devra être le point central de chaque message/info/comm. et devra l'envoyer ou devra être appelée par le manager qui aura besoin du message
    -> donc on a les logs bien sur, mais aussi les messages infos bulles et statuts (on ne veut pas dupliquer les sources ou autre)
- [ ] Définir et développer le menu systray et les infos bulles (le rework des messages doit être effectué)
- [ ] Fonction d'export/import complet (templates j2, config.json and home+client dirs) avec des options pour importer/exporter que ce qui nous interesse
    -> Cases à cocher/décocher (templates,configs,shared/skel, shared/home,shared/clients)
- [ ] Modifier la manière dont on gère les profiles "VPN Client" : 
    -> intégrer un template docker dans le profile au lieu d'voir des templates globaux
    -> demander un archive qui contient le template et le fichier ovpn (côté serveur faire le process qui génére ce fichier)
    -> et donc protéger cette archive avec GPG : “Service GPG prévu côté serveur (hors scope client) mais avec gestion de clé publique côté client”
#### 🐧 Linux
- [ ] Créer un linux/
- [ ] Modifier l'emplacement des fichiers .sh et les mettre dans linux/
- [ ] Créer des installeurs (.deb,.rpm, etc..)
#### 🪟 Windows
- [x] Rendre compatible l'application sous windows
- [x] Script d’installation/désinstallation global PowerShell (`install-manager.ps1`)
- [x] Scripts d’installation/désinstallation des outils PowerShell (lancé et managé par `install-manager.ps1`) :
- [x] .bat Wrappers (`install.bat`|`uninstall.bat`) : execute install-manager.ps1 avec l'executionpolicy en bypass
- [x] Création du fichier `.nsi` Nullsoft Installer automatisé
#### 🍎 Mac
- [ ] Rendre compatible l'application sous mac
- [ ] Créer le dossier macos/ (si besoin est)
- [ ] Créer/Modifier Scripts + Installeurs mac (des fonctions non testés existent déjà dans les fichiers .sh, à prendre en compte)

---

## 📂 RÉFÉRENCES TECHNIQUES

### 🧱 Stack technique
- OS : Linux (kernel 6+, pas testé en dessous)/Windows11/MacOS(pas encore testé, pas de version)
- Langages : Python 3.13 & + / PySide6 6.8.3 (pb de compatibilité à partir de 6.9 : gestion de la transparence KO)
- Outils : Docker 26 & + (Windows:vcxsrv/wsl)
- Environnement(s) cibles : multiplatforme(desktop)

### 💻 Environnements de test utilisés
- Windows 11 (WSL2.4 (last), PowerShell 7.5 (last), VcXsrv 21+)
- Linux Gentoo (kernel 6.6+, docker+docker-compose-plugin, X11)
- MacOS : pas encore testé (prévu après la v1)

### 🗂️ Arborescence simplifiée (si connue)
```
racine/
├── config/ : dossier contenant toute la configuration globale de l'application
│   ├── icons/ : dossier contenant toutes les images nécessaaires à l'appli
│       ├── *.png
│       ├── *.ico
│       └── *.svg
│   ├── locales/ : dossier contenaant les fichiers json pour chaque locales prise en compte(dynamique)
│       ├── fr.json
│       └── en.json
│   ├── templates/ : dossier contenant les templates pour build les dockerfile et compose
|       └── admin-default/ : template par défaut
│          ├── docker-compose.j2
│          └── dockerfile.j2
│   ├── themes/ : dossier contenaant les fichiers json pour chaque thème pris en compte(dynamique)
│       ├── default.json
│       └── blue.json
│   └── config.json : fichier globale de la configuration de l'appli
├── lib/ : dossier contenant toute l'applicaation en python
│   ├── venv/ : dossier de l'environnement virtuel python
│   ├── actions/ : dossier contenant toutes les actions (QAction)
│       ├── kactions.py
│       ├── kclientactions.py
│       ├── klangsactions.py
│       ├── kmanageractions.py
│       ├── kthemesactions.py
│       └── kvpnactions.py
│   ├── app/ : dossier contenant toutes les fenêtres
│       ├── kadd_client_dialog.py
│       ├── kapp_controller.py
│       ├── kcompact_main_window.py
│       ├── kconsole_log_window.py
│       ├── kfull_main_window.py
│       └── kprofiles_manager_dialog.py
│   ├── core/ : dossier contenant le core de l'application (managers, labels , centralisation de l'export des classes, etc...)
│       ├── actions.py
│       ├── config_manager.py
│       ├── configs.py
│       ├── docker.py
│       ├── env.py
│       ├── exttools_manager.py
│       ├── file_manager.py
│       ├── labels.py
│       ├── locales_manager.py
│       ├── log_manager.py
│       ├── manager.py
│       ├── state_manager.py
│       ├── sys_utils.py
│       ├── theme_manager.py
│       ├── vpn_tools.py
│       └── widgets.py
│   ├── widgets/ : tous les composants visuels avec les mixins appliqués
│       ├── kclient_card.py
│       ├── kclient_panel.py
│       ├── kclient_full_list.py
│       ├── kcontrols.py
│       ├── kdialog.py
│       ├── kframe.py
│       ├── kheader.py
│       ├── klast_action_bar.py
│       ├── klayouts.py
│       ├── klogstabs.py
│       ├── kmessagebox.py
│       ├── kmixins.py
│       ├── krootmenu_bar.py
│       ├── krootstatus_bar.py
│       ├── krootsystray.py
│       ├── kwidgets.py
│       └── kwindow.py
│   ├── shorcut_manager.py : gestionnaire de raccourci (multiplateforme)
│   ├── test_imports.py : test si tout est ok pour que l'appli fonctionne
│   └── vpn-manager.py : fichier root de l'applicaation
├── shared/
│   ├── clients/ : contient un dossier par client configuré/installé
│   ├── home/ : contient un dossier home pour le docker par client
│   └── skel/ : contient la base du skel qui doit être copiée dans le docker au premier démarrage
├── windows/
│   ├── ps/ : powershell 7.5 installé localement
│   ├── requirements.txt : pip (python) requirements file pour windows
│   ├── vpn-manager.nsi : nullsoft autoinstaller file
│   ├── ps7.ps1 : install/uninstall ps7 localement pour exécuter tous les autres scripts (script en ps5)
│   ├── elevate.ps1 : exécute les scripts ps avec les droits admin
│   ├── winget.ps1 : install/update l'outil winget
│   ├── winget-tools.ps1 : install/uninstall vcxsrv/python avec winget
│   ├── wsl.ps1 : install/uninstall wsl container basé sur Ubuntu2404
│   ├── appreg.ps1 : register/unregister app sur le windows App manager
│   ├── startuponboot.ps1 : install/uninstall application au boot
│   ├── python.ps1 : install/uninstall le venv, les dépendances pythons(avec pip)
│   ├── vcxsrv.ps1 : register/start | unregister/stop l'outil vcxsrv au démarrage
│   ├── install-manager.ps1 : install/uninstall toute l'application avec ses dépendances (lance les scripts ps1 dans le bon ordre et avec les bons droits)
│   ├── install.bat : execute 'install-manager.ps1 install' avec l'executionpolicy en bypass
│   └── uninstall.bat : execute 'install-manager.ps1 uninstall' avec l'executionpolicy en bypass
├── installers/ : dossier 'output' pour les installateurs windows(peut-être mac/linux plus tard)
├── logs/ : dossiers contenant toutes les logs de l'appli
├── .gitignore : fichier gitignore
├── uninstall.sh : uninstalleur Linux/Mac
└── vpn-manager.sh : installeur/updateur Linux/Mac
````

### 🔗 Liens utiles
- [Dépôt GitHub](https://github.com/openkame/open-dock-vpn)
- Documentation interne (si dispo) : pas encore effectuée
- Références externes (RFC, guides, etc.) : N/A

---

## 🎯 INSTRUCTIONS DE COMPORTEMENT POUR CHATGPT

- Réponses **structurées, concises et techniques**
- **Pas de blabla inutile** ou de reformulation de la question
- **Commentaires en anglais** dans tout le code
- Pose **une seule question ciblée** si un point est ambigu
- Priorité : efficacité, rapidité de compréhension, pas de distraction

---

## 📅 Versioning

* Version : `v1.1`
* Dernière mise à jour : `2025-05-20`

```