param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "uninstall", "start", "stop")]
    [string]$Action
)

# ✅ Vérifie que le script n'est pas exécuté en tant qu'administrateur
if (([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script ne doit pas être exécuté en tant qu'administrateur."
    exit 1
}

# 📦 Vérifie que VcXsrv est installé
$vcxsrvPath = "C:\Program Files\VcXsrv\vcxsrv.exe"
$runArgs = ":0 -multiwindow -clipboard -wgl"
$regKeyPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$regValueName = "VcXsrv"

# ✅ Lancement manuel (si pas déjà en cours)
function Start-VcXsrv() {
    if (Get-Process -Name "vcxsrv" -ErrorAction SilentlyContinue) {
        Write-Host "✅ VcXsrv déjà en cours d'exécution"
        return
    }

    if (-not (Test-Path $vcxsrvPath)) {
        Write-Host "❌ VcXsrv introuvable à l'emplacement attendu : $vcxsrvPath"
        exit 1
    }

    Write-Host "🚀 Lancement de VcXsrv..."
    Start-Process -FilePath $vcxsrvPath -ArgumentList $runArgs
}

function Stop-VcXsrv() {
    if (-not (Get-Process -Name "vcxsrv" -ErrorAction SilentlyContinue)) {
        Write-Host "✅ VcXsrv déjà est déjà arrêté"
        return
    }
    Write-Host "Arrêt de VcXsrv..."
    Stop-Process -Name "vcxsrv"
}

# ✅ Ajout clé registre pour démarrage auto
function Register-VcXsrvStartup() {
    if (-not (Test-Path $vcxsrvPath)) {
        Write-Host "❌ VcXsrv introuvable. Installation nécessaire avant enregistrement auto."
        exit 1
    }

    $cmd = "`"$vcxsrvPath`" $runArgs"
    Set-ItemProperty -Path $regKeyPath -Name $regValueName -Value $cmd
    Write-Host "✅ Démarrage automatique de VcXsrv enregistré pour l'ouverture de session."
}

# ❌ Suppression démarrage automatique
function Unregister-VcXsrvStartup() {
    if ( Get-ItemProperty $regKeyPath -Name $regValueName -ErrorAction SilentlyContinue ) {
        Stop-VcXsrv
        Remove-ItemProperty -Path $regKeyPath -Name $regValueName -ErrorAction SilentlyContinue
        Write-Host "✅ VcXsrv ne sera plus lancé automatiquement à l'ouverture de session."
    } else {
        Write-Host "ℹ️ Aucun démarrage automatique VcXsrv détecté."
    }
}

# 🧠 Vérification Admin : inutile ici (clé HKCU → pas besoin d’être admin)

switch ($Action) {
    "start"     { Start-VcXsrv }
    "stop"      { Stop-VcXsrv }
    "install"   {
        Register-VcXsrvStartup
        Start-VcXsrv
    }
    "uninstall" { Unregister-VcXsrvStartup }
}
