param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("install", "update", "uninstall")]
    [string]$Action
)

# ✅ Vérifie que le script est exécuté en tant qu'administrateur
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur."
    exit 1
}

# 🔧 Paramètres
$wslName = "vpn-manager"
$wslBin = "C:\Program Files\WSL\wsl.exe"
$ubuntuDistro = "Ubuntu-24.04"
$wslUser = "vpn"
$wslTools = @("x11-apps", "x11-xserver-utils", "docker.io", "docker-compose-v2")

function Invoke-WslRoot {
    param (
        [string]$Command
    )
    & $wslBin -d $wslName --user root -- bash -c $Command
}


# ✅ Vérifie que WSL est activé
function Test-WslEnabled {
    $feature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    return ($feature.State -eq "Enabled")
}

function Enable-Wsl {
    if (-not (Test-WslEnabled)) {
        Write-Host "📦 Activation de la fonctionnalité WSL..."
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart
    }
}

# ✅ Met à jour le moteur WSL (runtime)
function Update-WslSystem {
    Write-Host "🔄 Mise à jour du runtime WSL..."
    & "C:\Windows\System32\wsl.exe" --update
}


# ✅ Vérifie si la distrib est installée
function Test-WslDistro {
    $distros = & $wslBin --list --quiet
    return ($distros -contains $wslName)
}

# ✅ Mise à jour des paquets dans la distrib
function Update-WslPackages {
    Invoke-WslRoot "apt update && apt upgrade -y"
}

# ✅ Installation des paquets requis
function Install-WslTools {
    $tools = $wslTools -join " "
    Invoke-WslRoot "apt install -y $tools"
}

# ✅ Création du user et ajout à docker
function Initialize-WslUser {
    Invoke-WslRoot "id -u $wslUser >/dev/null 2>&1 || useradd -m -p $wslUser $wslUser"
    Invoke-WslRoot "usermod -aG docker $wslUser"
}

# ✅ Installation complète
function Install-Wsl {
    Enable-Wsl
    Update-WslSystem

    if (Test-WslDistro) {
        Write-Host "✅ Distribution '$wslName' déjà installée."
        return
    }

    Write-Host "📦 Installation de la distribution '$wslName'..."
    & $wslBin --install $ubuntuDistro --name $wslName -n
    Start-Sleep -Seconds 3

    Write-Host "🔧 Configuration de la distribution '$wslName'..."
    Update-WslPackages
    Install-WslTools
    Initialize-WslUser
    & $wslBin --manage $wslName --set-default-user root

    Write-Host "✅ Distribution '$wslName' installée et configurée."
}

# ❌ Suppression de la distribution
function Remove-Wsl {
    if (Test-WslDistro) {
        Write-Host "🧹 Suppression de la distribution '$wslName'..."
        & $wslBin --unregister $wslName
    } else {
        Write-Host "ℹ️ Distribution '$wslName' non installée."
    }
}

# 🚀 Routine principale
switch ($Action) {
    "install" {
        Install-Wsl
    }
    "update" {
        if (Test-WslDistro) {
            Update-WslSystem
            Update-WslPackages
            Install-WslTools
        } else {
            Write-Host "❌ Distribution '$wslName' non installée. Lancez 'install' d'abord."
            exit 1
        }
    }
    "uninstall" {
        Remove-Wsl
    }
}
