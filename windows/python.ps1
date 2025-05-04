param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "update", "uninstall")]
    [string]$Action,

    [Parameter(Mandatory=$true)]
    [string]$InstallPath
)

# ✅ Vérifie que le script n'est pas exécuté en tant qu'administrateur
if (([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script ne doit pas être exécuté en tant qu'administrateur."
    exit 1
}

# 📁 Validation du répertoire d'installation
if (-Not (Test-Path $InstallPath)) {
    Write-Host "❌ Chemin d'installation invalide : $InstallPath"
    exit 1
}

# 📁 Paths
$BASE_DIR = $InstallPath
$VENV_DIR = Join-Path $BASE_DIR "lib\venv"
$LIB_DIR  = Join-Path $BASE_DIR "lib"
$PYTHON_VENV = Join-Path $VENV_DIR "Scripts\python.exe"
$REQ_FILE = Join-Path $BASE_DIR "windows\requirements.txt"
$TEST_IMPORTS = Join-Path $LIB_DIR "test_imports.py"

# 🔧 Vérifie si le venv est valide (version Python >= 3.8)
function Test-Venv() {
    if (Test-Path $PYTHON_VENV) {
        & $PYTHON_VENV -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" | Out-Null
        return ($LASTEXITCODE -eq 0)
    }
    return $false
}

function Install-Venv() {
    Write-Host "🔍 Vérification de l'environnement virtuel Python..."
    if (-Not (Test-Venv)) {
        if (Test-Path $VENV_DIR) {
            Write-Host "⚠️ Venv existant invalide. Suppression..."
            Remove-Item -Recurse -Force $VENV_DIR
        }

        Write-Host "🔧 Création du venv..."
        python -m venv $VENV_DIR
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Erreur lors de la création du venv."
            exit 1
        }
    } else {
        Write-Host "✅ Venv existant valide."
    }
}

function Start-Venv() {
    $env:VIRTUAL_ENV = $VENV_DIR
    $env:PATH = "$VENV_DIR\Scripts;$env:PATH"
    $env:PYTHONUTF8 = "1"
}

function Update-Pip() {
    & $PYTHON_VENV -m pip --version | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ pip manquant. Installation via ensurepip..."
        & $PYTHON_VENV -m ensurepip --default-pip
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Impossible d'installer pip."
            exit 1
        }
    } else {
        Write-Host "✅ pip est présent."
    }

    Write-Host "🔄 Mise à jour de pip lui-même..."
    & $PYTHON_VENV -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erreur lors de la mise à jour de pip."
        exit 1
    }
}

function Update-Venv() {
    Write-Host "🔄 Vérification des mises à jour pip..."
    $outdated = & $PYTHON_VENV -m pip list --outdated
    if ($outdated) {
        Write-Host "📦 Mise à jour des dépendances..."
        & $PYTHON_VENV -m pip install -U --no-input -r $REQ_FILE
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Échec de mise à jour des paquets."
            exit 1
        }
    } else {
        Write-Host "✅ Aucune mise à jour nécessaire."
    }
}

function Install-Dependencies() {
    Write-Host "🔍 Vérification des imports Python..."
    & $PYTHON_VENV $TEST_IMPORTS | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "📦 Installation des requirements..."
        & $PYTHON_VENV -m pip install -r $REQ_FILE
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Erreur d'installation des dépendances."
            exit 1
        }
    } else {
        Write-Host "✅ Tous les modules nécessaires sont déjà installés."
    }
}

function Uninstall-Venv() {
    if (Test-Path $VENV_DIR) {
        Write-Host "🧹 Suppression de l'environnement virtuel Python..."
        Remove-Item -Recurse -Force $VENV_DIR
        Write-Host "✅ Venv supprimé."
    } else {
        Write-Host "ℹ️ Aucun venv à supprimer."
    }
}

switch ($Action) {
    "install" {
        Install-Venv
        Start-Venv
        Update-Pip
        Install-Dependencies
    }
    "update" {
        if (-Not (Test-Venv)) {
            Write-Host "❌ Aucun venv valide détecté. Lancez 'install' d'abord."
            exit 1
        }
        Start-Venv
        Update-Pip
        Update-Venv
        Install-Dependencies
    }
    "uninstall" {
        Uninstall-Venv
    }
}
