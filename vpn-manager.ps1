# Wrapper vpn-manager.ps1 (Windows)

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


chcp 65001 > $null


# 📁 Répertoires
$BASE_DIR = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$VENV_DIR = Join-Path $BASE_DIR "lib\venv"
$LIB_DIR = Join-Path $BASE_DIR "lib"
$SHARED_DIR = "$BASE_DIR\shared"

function Check-Install($label, $command, $packages) {
    if ($label -eq "python") {
        $isWindowsStore = $false
        $isCpython = $false

        $commandPath = Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
        if ($commandPath -like "*WindowsApps*") {
            $isWindowsStore = $true
        }

        foreach ($pathEntry in $env:Path.Split(';')) {
            if ($pathEntry -match "C:\\Python\d{2,}") {
                $isCpython = $true
                break
            }
        }

        if ($isWindowsStore -or -not $isCpython) {
            Write-Host "⚠️ Python Store détecté ou manquant → Réinstallation forcée"
            choco install python --force -y
            return
        }

        Write-Host "✅ Python OK"
        return
    }

    foreach ($pkg in $packages) {
        $result = choco list -exact $pkg
        if ($result -match "0 packages installed") {
            Write-Host "📦 Installation nécessaire : $pkg"
            choco install $pkg -y
        } else {
            Write-Host "✅ $pkg déjà installé"
        }
    }
}

# Vérifier Chocolatey sinon installer
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
	Write-Host "Installation Chocolatey..."
	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
	iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    Write-Host "`n🔁 Redémarrez votre session PowerShell pour activer Chocolatey."
    exit 0
}

$packages = @(
    @{label = "python"; command = "python"; packages = @("python") },
    @{label = "docker"; command = "docker"; packages = @("docker", "docker-cli", "docker-engine", "docker-compose") },
    #@{label = "openvpn"; command = "openvpn"; packages = @("openvpn") },
    @{label = "vcxsrv"; command = "vcxsrv"; packages = @("vcxsrv") }
)

foreach ($pkg in $packages) {
    Check-Install $pkg.label $pkg.command $pkg.packages
}

# 🚀 Lancement du service docker-engine si pas déjà lancé !
$service = Get-Service -Name "docker" -ErrorAction SilentlyContinue
if ($service.Status -ne "Running") {
    Write-Host "🚀 Lancement du service Docker..."
    Start-Service -Name "docker"
}

# 🚀 Lancer VcXsrv seulement si pas déjà en cours
if (!(Get-Process -Name "vcxsrv" -ErrorAction SilentlyContinue)) {
    $vcxsrvPath = "C:\Program Files\VcXsrv\vcxsrv.exe"
    if (Test-Path $vcxsrvPath) {
        Write-Host "🖥️ Lancement de VcXsrv..."
        Start-Process $vcxsrvPath -ArgumentList ":0 -multiwindow -clipboard -wgl"
    } else {
        Write-Host "⚠️ VcXsrv introuvable à l'emplacement attendu : $vcxsrvPath"
    }
} else {
    Write-Host "✅ VcXsrv déjà en cours d'exécution"
}

Write-Host "🔍 Vérification de l'environnement virtuel Python..." -NoNewline
if (Test-Path $VENV_DIR) {
    $pythonPath = Join-Path $VENV_DIR "Scripts\python.exe"
    $versionOK = & $pythonPath -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host " KO"
        Write-Host "⚠️ L'environnement virtuel semble corrompu. Suppression et recréation."
        Remove-Item -Recurse -Force $VENV_DIR
    } else {
        Write-Host " OK"
    }
}

if (-Not (Test-Path $VENV_DIR)) {
    Write-Host "🔹 Création de l'environnement virtuel Python..." # -NoNewline
    python -m venv $VENV_DIR
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK"
    } else {
        Write-Host " KO"
        exit 1
    }
}

Write-Host "🔹 Activation de l'environnement virtuel..." -NoNewline
$env:VIRTUAL_ENV = $VENV_DIR
$env:PATH = "$VENV_DIR\Scripts;$env:PATH"
$env:PYTHONUTF8 = "1"
Write-Host " done"

# 🔥 Vérifie pip
$pythonVenv = Join-Path $VENV_DIR "Scripts\python.exe"
if (-not (& $pythonVenv -m pip --version 2>$null)) {
    Write-Host "⚠️ pip n'est pas installé. Tentative d'installation..." -NoNewline
    if (& $pythonVenv -m ensurepip --default-pip) {
        Write-Host " OK"
    } else {
        Write-Host " KO"
    }
}

# 🔄 Mise à jour si nécessaire
$outdated = & $pythonVenv -m pip list --outdated
if ($outdated) {
    Write-Host "🔄 Mise à jour de l'environnement..." -NoNewline
    if (& $pythonVenv -m pip install -U --no-input -r "$LIB_DIR\requirements.txt" 2>$null) {
        Write-Host " OK"
    } else {
        Write-Host " KO"
        exit 1
    }
}

# 📦 Vérification/installation des dépendances
Write-Host "🔍 Vérification et installation des dépendances python..." -NoNewline
$testImports = Join-Path $LIB_DIR "test_imports.py"
if (-not (& $pythonVenv $testImports)) {
    if (& $pythonVenv -m pip install -r "$LIB_DIR\requirements.txt" 2>$null) {
        Write-Host " OK"
    } else {
        Write-Host " KO"
        exit 1
    }
} else {
    Write-Host " OK"
}

# 📌 Création du raccourci global au besoin
& $pythonVenv "$LIB_DIR/shortcut_manager.py"

& $pythonVenv "$LIB_DIR\vpn-manager.py" $args

