param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("install", "uninstall")]
    [string]$Action
)

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur."
    exit 1
}

$AppName = "VPN Manager"
$AppVersion = "0.1.0"
$InstallPath = "$env:LOCALAPPDATA\VpnManager"
$UninstallerPath = "$InstallPath\uninstall.exe"
$IconPath = "$InstallPath\config\icons\vpn-manager.ico"

$registryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"

if ($Action -eq "install") {
    Write-Host "📝 Enregistrement de l'application dans Programmes et Fonctionnalités..."
    New-Item -Path $registryPath -Force | Out-Null
    Set-ItemProperty -Path $registryPath -Name "DisplayName" -Value $AppName
    Set-ItemProperty -Path $registryPath -Name "UninstallString" -Value $UninstallerPath
    Set-ItemProperty -Path $registryPath -Name "InstallLocation" -Value $InstallPath
    Set-ItemProperty -Path $registryPath -Name "DisplayIcon" -Value $IconPath
    Set-ItemProperty -Path $registryPath -Name "Publisher" -Value "openkame"
    Set-ItemProperty -Path $registryPath -Name "DisplayVersion" -Value $AppVersion
}
elseif ($Action -eq "uninstall") {
    Write-Host "🧹 Suppression de l'entrée Programmes et Fonctionnalités..."
    Remove-Item -Path $registryPath -Recurse -Force -ErrorAction SilentlyContinue
}
