param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("install", "uninstall")]
  [string]$Action
)

$RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$ValueName = "VPN Manager"
$ShortcutPath = "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\VPN Manager\VPN-Manager.lnk"

# ⬆️ Redemande droits admin
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur."
    exit 1
}

if ($Action -eq "install") {
    if (-Not (Test-Path $ShortcutPath)) {
        Write-Host "❌ Raccourci introuvable à : $ShortcutPath"
        exit 1
    }
    Set-ItemProperty -Path $RegPath -Name $ValueName -Value "`"$ShortcutPath`""
    Write-Host "✅ Clé d’exécution ajoutée."
}
elseif ($Action -eq "uninstall") {
    Remove-ItemProperty -Path $RegPath -Name $ValueName -ErrorAction SilentlyContinue
    Write-Host "🧹 Clé supprimée."
}
