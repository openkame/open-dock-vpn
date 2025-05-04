param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "uninstall")]
    [string]$Action
)

# 🛡️ Vérifie si admin
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur."
    exit 1
}

# 📍 Fonctions utilitaires
function Test-WingetInstalled {
    return $null -ne (Get-Command winget.exe -ErrorAction SilentlyContinue)
}

function Get-WingetPath {
    return "$env:ProgramFiles\WindowsApps\Microsoft.DesktopAppInstaller_1.25.390.0_x64__8wekyb3d8bbwe"
}

function Test-WingetInPath {
    $wingetDir = Get-WingetPath
    if (-Not (Test-Path "$wingetDir\winget.exe")) {
        Write-Host "❌ winget.exe non trouvé dans $wingetDir"
        return
    }

    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($machinePath -notmatch [Regex]::Escape($wingetDir)) {
        Write-Host "➕ Ajout de winget au PATH système..."
        $newPath = "$machinePath;$wingetDir"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        Write-Host "✅ winget ajouté au PATH système."
    } else {
        Write-Host "✅ winget est déjà dans le PATH."
    }
}

function Install-Winget {
    if (Test-WingetInstalled) {
        Write-Host "✅ Winget est déjà installé."
        
        return
    } elseif (Test-WingetInPath) {
        Write-Host "✅ Winget installé mais sans path."
    }

    $uri = "https://aka.ms/getwinget"
    $pkg = "$env:TEMP\winget.msixbundle"

    if (-not (Test-Path $pkg)) {
        Write-Host "📦 Téléchargement de Winget..."
        Invoke-WebRequest -Uri $uri -OutFile $pkg
    } else {
        Write-Host "Winget déjà téléchargée : $zipFile"
    }
    Write-Host "📦 Installation de Winget..."
    Add-AppxPackage -Path $pkg -ForceApplicationShutdown

    Start-Sleep -Seconds 2

    if (Test-WingetInstalled) {
        Write-Host "✅ Winget installé avec succès."
        Test-WingetInPath
    } else {
        Write-Host "❌ Échec d'installation de Winget."
        exit 1
    }
}

function Remove-Winget {
    Write-Host "🚫 Winget ne peut pas être désinstallé proprement par script."
    Write-Host "ℹ️ Il est intégré à Windows via App Installer."
}

# 🎬 Exécution principale
switch ($Action) {
    "install"   { Install-Winget }
    "uninstall" { Remove-Winget }
}
