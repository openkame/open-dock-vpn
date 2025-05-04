param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "update", "uninstall")]
    [string]$Action
)

# ✅ Vérifie que le script est exécuté en tant qu'administrateur
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur."
    exit 1
}

# 📦 Liste des outils nécessaires
$packages = @(
    @{ label = "python";     id = "Python.Python.3.13" },
    @{ label = "vcxsrv";     id = "marha.VcXsrv" }
)

function Test-IsPackageInstalled($id) {
    $output = winget list --source winget | Where-Object { $_ -match $id }
    return ($null -ne $output -and $output -ne "")
}

function Install-Package($label, $id) {
    if (Test-IsPackageInstalled $id) {
        Write-Host "✅ $label déjà installé."
    } else {
        Write-Host "📦 Installation de $label ($id)..."
        winget install --id $id --silent --accept-package-agreements --accept-source-agreements
    }

}

function Update-Package($label, $id) {
    if (-not (Test-IsPackageInstalled $id)) {
        Write-Host "📦 $label non installé. Installation..."
        Install-Package $label $id
    } else {
        Write-Host "🔄 Mise à jour de $label ($id)..."
        winget upgrade --id $id --silent --accept-package-agreements --accept-source-agreements
    }
}

function Remove-Package($label, $id) {
    if (-not (Test-IsPackageInstalled $id)) {
        Write-Host "ℹ️ $label non installé. Rien à faire."
        return
    }

    Write-Host "🚮 Désinstallation de $label ($id)..."
    winget uninstall --id $id --silent --accept-source-agreements

}

# 🚀 Exécution principale
foreach ($pkg in $packages) {
    switch ($Action) {
        "install"   { Install-Package  $pkg.label $pkg.id }
        "update"    { Update-Package   $pkg.label $pkg.id }
        "uninstall" { Remove-Package   $pkg.label $pkg.id }
    }
}
