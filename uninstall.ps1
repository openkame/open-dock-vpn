Write-Host "🗑️ Désinstallation VPN-Manager (Windows)"

function Ask-Remove ($pkg) {
    $choice = Read-Host "Voulez-vous désinstaller $pkg ? (y/n)"
    if ($choice -eq "y") {
        choco uninstall -y $pkg
    }
}

foreach ($pkg in "python","docker-desktop","openvpn","vcxsrv") {
    Ask-Remove $pkg
}

$delhome = Read-Host "Supprimer aussi la configuration persistante (home directory VPN) ? ⚠️ (y/n)"
if ($delhome -eq "y") {
    Remove-Item -Recurse -Force ./home
}

