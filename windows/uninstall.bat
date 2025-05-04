@echo off
echo 🧹 Désinstallation de l’environnement de dev...

:: 🔧 Répare le PATH manquant pour System32 (si lancé depuis NSIS)
set PATH=%SystemRoot%\System32;%SystemRoot%;%SystemRoot%\System32\Wbem;%PATH%;;%SystemRoot%\System32\WindowsPowerShell\v1.0\

chcp 65001

echo 🔽 Suppression de tous les composants (via dev-manager)...
.\ps\pwsh.exe -ExecutionPolicy Bypass -File .\install-manager.ps1 uninstall

echo 🔽 Suppression de PowerShell 7.5...
powershell -ExecutionPolicy Bypass -File .\ps7.ps1 uninstall

echo ✅ Environnement de développement nettoyé.
pause
