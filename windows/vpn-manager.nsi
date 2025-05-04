; VPN Manager Installer (NSIS)

!define APP_NAME "VPN Manager"
!define APP_VERSION "0.1.0"
!define INSTALL_DIR "$LOCALAPPDATA\VpnManager"
!define OUTPUT_DIR "..\installers"

SetCompressor lzma
SetCompressorDictSize 64
RequestExecutionLevel user
; Unicode true

OutFile "${OUTPUT_DIR}\vpn-dock-windows11-${APP_VERSION}-x64.exe"
InstallDir "${INSTALL_DIR}"
InstallDirRegKey HKCU "Software\${APP_NAME}" "InstallPath"

Name "${APP_NAME}"
Caption "Installation de ${APP_NAME}"
BrandingText "Projet open-source par openkame"

; ========== VARIABLES ==========
Var installapp
Var desktopicon
Var runatstartup

Function .onInit
  ClearErrors
  ReadRegStr $0 HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation"
  IfErrors done
  ; Si une valeur a été trouvée, afficher un message et quitter
  MessageBox MB_OK|MB_ICONINFORMATION "${APP_NAME} est déjà installé, aucune action n'est requise." /SD IDOK
  Abort
done:
FunctionEnd

; ========== OPTIONS UTILISATEUR ==========
!include MUI2.nsh

!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "French"

Section "Install VPN Manager" SEC01
  SectionIn 1 RO
  StrCpy $installapp 1
SectionEnd

Section "Create Shorcut on Desktop" SEC_DESKTOP
  SectionIn 1
  StrCpy $desktopicon 1
SectionEnd

Section "Run at Startup" SEC_RUNATBOOT
  SectionIn 1
  StrCpy $runatstartup 1
SectionEnd


; ========== SECTION PRINCIPALE ==========
Section -PostInstall
  ${If} $installapp == 1
    ; Création dossier
    SetOutPath "$INSTDIR"
    ; Copie des fichiers nécessaires
    File /r /x venv /x __pycache__ "..\lib"
    File /r /x home /x clients "..\shared"
    File /r "..\windows"
    SetOutPath "$INSTDIR\config"
    File /r "..\config\locales"
    File /r "..\config\icons"
    File /r "..\config\templates"
    File /r "..\config\themes"

    ; Change le répertoire courant pour l'exécution des scripts
    SetOutPath "$INSTDIR\windows"

    ; Exécute le script principal d'installation
    ExecWait '"$INSTDIR\windows\install.bat"'

        ; Copie vers Menu Démarrer
    CopyFiles "$INSTDIR\VPN-Manager.lnk" "$SMPROGRAMS\${APP_NAME}\VPN-Manager.lnk"

    ; Copie vers le bureau (si coché)
    ${If} $desktopicon == 1
        CopyFiles "$INSTDIR\VPN-Manager.lnk" "$DESKTOP\VPN-Manager.lnk"
    ${EndIf}

    ${If} $runatstartup == 1
        ExecWait '"$INSTDIR\windows\ps\pwsh.exe" -ExecutionPolicy Bypass -File "$INSTDIR\windows\elevate.ps1" "$INSTDIR\windows\startuponboot.ps1" install'
    ${EndIf}

    ; Enregistrement de l'app dans Programmes et Fonctionnalités (via script PowerShell élevé)
    ExecWait '"$INSTDIR\windows\ps\pwsh.exe" -ExecutionPolicy Bypass -File "$INSTDIR\windows\elevate.ps1" "$INSTDIR\windows\appreg.ps1" install'

    WriteUninstaller "$INSTDIR\uninstall.exe"
  ${EndIf}

SectionEnd

; ========== Section Uninstall ==========
Section "Uninstall"

  SetOutPath "$INSTDIR\windows"

  ; Supprime l'exécution au démarrage
  ExecWait '"$INSTDIR\windows\ps\pwsh.exe" -ExecutionPolicy Bypass -File "$INSTDIR\windows\elevate.ps1" "$INSTDIR\windows\startuponboot.ps1" uninstall'

  ; Désenregistrement de l'app
  ExecWait '"$INSTDIR\windows\ps\pwsh.exe" -ExecutionPolicy Bypass -File "$INSTDIR\windows\elevate.ps1" "$INSTDIR\windows\appreg.ps1" uninstall'

  ; Supprime les outils externes (python, wsl, etc...)
  ExecWait '"$INSTDIR\windows\uninstall.bat"' 

  ; Suppression des fichiers et dossiers
  Delete "$DESKTOP\VPN-Manager.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\VPN-Manager.lnk"
  RMDir /r "$SMPROGRAMS\${APP_NAME}"
  RMDir /r "$INSTDIR"

  

SectionEnd
