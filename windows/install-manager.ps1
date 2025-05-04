param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("install", "update", "uninstall")]
    [string]$Action
)

# 📁 Détermine le chemin d'installation = racine du projet Git
$BASE_DIR = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$INSTALL_PATH = Split-Path -Path $BASE_DIR -Parent

# 🔁 Redirige vers PS7 si on n'y est pas encore
$ps7 = Join-Path $BASE_DIR "ps\pwsh.exe"
if (-not $PSVersionTable.PSVersion -or $PSVersionTable.PSVersion.Major -lt 7) {
    if (Test-Path $ps7) {
        Write-Host "🔁 Redirection vers PowerShell 7.5..."
        & "$ps7" -File $MyInvocation.MyCommand.Definition @args
        exit
    } else {
        Write-Host "❌ PowerShell 7.5 n'est pas encore installé. Veuillez exécuter 'ps7.ps1 install' d'abord."
        exit 1
    }
}

function Initialize-UserPath {
    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath    = [Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path    = "$userPath;$machinePath"
    Write-Host "♻️ PATH utilisateur rechargé localement pour cette session."
}

function Invoke-AsAdmin {
    param (
        [string]$ScriptPath,
        [string[]]$Arguments = @()
    )
    $argLine = "-ExecutionPolicy Bypass -File `"$ScriptPath`" $Arguments"
    Start-Process -FilePath $ps7 -ArgumentList $argLine -Verb RunAs -Wait
}

Write-Host "📦 Action : $Action"
Write-Host "📁 INSTALL_PATH = $INSTALL_PATH"

# ⚙️ Scripts à exécuter dans l’ordre
if ($Action -ne "update") {
    Invoke-AsAdmin "$BASE_DIR\winget.ps1" @($Action)
}

Invoke-AsAdmin "$BASE_DIR\winget-tools.ps1" @($Action)
Initialize-UserPath

Invoke-AsAdmin "$BASE_DIR\wsl.ps1" @($Action)

if ($Action -ne "update") {
    & "$BASE_DIR\vcxsrv.ps1" $Action
}

& "$BASE_DIR\python.ps1" $Action $INSTALL_PATH

# 🎯 Raccourci
if ($Action -eq "install" -or $Action -eq "update") {
    $pythonExe = Join-Path $INSTALL_PATH "lib\venv\Scripts\pythonw.exe"
    & $pythonExe "$INSTALL_PATH\lib\shortcut_manager.py"
}
elseif ($Action -eq "uninstall") {
    $shortcut = Join-Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs" "VPN-Manager.lnk"
    if (Test-Path $shortcut) {
        Remove-Item $shortcut -Force
        Write-Host "🧹 Raccourci supprimé : $shortcut"
    }
}
