@echo off
setlocal

:: 🔧 Répare le PATH manquant pour System32 (si lancé depuis NSIS)
set PATH=%SystemRoot%\System32;%SystemRoot%;%SystemRoot%\System32\Wbem;%PATH%;;%SystemRoot%\System32\WindowsPowerShell\v1.0\

chcp 65001

echo ✅ Configuration de PowerShell ExecutionPolicy...
powershell -Command "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force"

echo 🚀 Installation de PowerShell 7.5.1...
powershell -ExecutionPolicy Bypass -File .\ps7.ps1 install

echo 🧱 Lancement de l’environnement via PowerShell 7.5 (utilisateur)...
ps\pwsh.exe -ExecutionPolicy Bypass -File install-manager.ps1 install

echo.
echo ✅ Installation terminée !
echo ------------------------------------------
echo Pour mettre à jour l'environnement : 
echo     .\ps\pwsh.exe -File .\install-manager.ps1 update
echo.
echo Pour désinstaller proprement :
echo     double-cliquez sur uninstall.bat
echo ------------------------------------------
pause