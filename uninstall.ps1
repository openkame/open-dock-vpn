Write-Host "Désinstallation VPN-Manager (Windows)"

# Vérifie les droits admin
$IsAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $IsAdmin) {
    Write-Host "⚠️ Ce script nécessite des droits administrateur pour certaines opérations."

    $arguments = "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
    $proc = Start-Process powershell -ArgumentList $arguments -Verb RunAs -PassThru

    # Attendre la fin du processus relancé
    $proc.WaitForExit()

    Write-Host "`nℹ️ Le script s'est terminé. Appuyez sur Entrée pour quitter."
    Read-Host
    exit
}

function Ask-Remove($nameLike) {
    $installedPackages = choco list | ForEach-Object {
        ($_ -split '\s+')[0]  # Garde uniquement le nom (avant le premier espace)
    }

    $pkgToRemove = $installedPackages | Where-Object { $_ -like "$nameLike*" }

    if ($pkgToRemove) {
        foreach ($pkg in $pkgToRemove) {
            $choice = Read-Host "Voulez-vous désinstaller $pkg ? (y/n)"
            if ($choice -eq "y") {
                choco uninstall -y $pkg
            }
        }
    } else {
        Write-Host "ℹ️ Aucun package correspondant à '$nameLike' n'est installé."
    }
}

foreach ($pkg in "python","docker-desktop","openvpn","vcxsrv") {
    Ask-Remove $pkg
}

# ──────────────── 🔻 Suppression de Chocolatey
$delChoco = Read-Host "Souhaitez-vous également désinstaller Chocolatey ? (y/n)"
if ($delChoco -eq "y") {
    Write-Host "`n🚮 Suppression de Chocolatey..."

    # Désinstalle Chocolatey + ses variables d'env
    $envPaths = @(
        "$env:ProgramData\chocolatey",
        "$env:ProgramData\chocolatey\bin",
        "$env:ChocolateyInstall"
    )

    foreach ($path in $envPaths) {
        if (Test-Path $path) {
            Remove-Item -Recurse -Force $path -ErrorAction SilentlyContinue
            Write-Host "✅ Supprimé : $path"
        }
    }

    # Supprime choco des variables d'environnement PATH utilisateur + système
    $currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
    $newPath = ($currentPath -split ';') | Where-Object { $_ -notmatch "chocolatey" } -join ';'
    [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::Machine)

    $userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
    $newUserPath = ($userPath -split ';') | Where-Object { $_ -notmatch "chocolatey" } -join ';'
    [Environment]::SetEnvironmentVariable("Path", $newUserPath, [EnvironmentVariableTarget]::User)

    Write-Host "`n♻️ Un redémarrage est recommandé pour finaliser la désinstallation de Chocolatey."
}


$delhome = Read-Host "Supprimer aussi la configuration persistante (home directory VPN) ? (y/n)"
if ($delhome -eq "y") {
    Remove-Item -Recurse -Force .\shared\home
}

