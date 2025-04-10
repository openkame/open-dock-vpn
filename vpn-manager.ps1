# Wrapper vpn-manager.ps1 (Windows)

$BASE_DIR = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$LIB_DIR = "$BASE_DIR\lib"
$SHARED_DIR = "$BASE_DIR\shared"

function Check-Install ($command, $package) {
	if (!(Get-Command $command -ErrorAction SilentlyContinue)) {
		Write-Host "🔸 Installation nécessaire : $package"
		choco install -y $package
	} else {
		Write-Host "✅ $package déjà installé."
	}
}

# Vérifier Chocolatey sinon installer
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
	Write-Host "🍫 Installation Chocolatey..."
	Set-ExecutionPolicy Bypass -Scope Process -Force
	[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
	iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

foreach ($pkg in @(
	@{command="python"; package="python"},
	@{command="docker"; package="docker-desktop"},
	@{command="openvpn"; package="openvpn"},
	@{command="vcxsrv"; package="vcxsrv"}
)) {
	Check-Install $pkg.command $pkg.package
}

Start-Process "C:\Program Files\VcXsrv\vcxsrv.exe" ":0 -multiwindow -clipboard -wgl"

pip install -r "$LIB_DIR\requirements.txt"

python "$LIB_DIR\vpn-manager.py" $args

