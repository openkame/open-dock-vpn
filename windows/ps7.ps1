param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("install", "uninstall")]
    [string]$Action
)

$zipUrl = "https://github.com/PowerShell/PowerShell/releases/download/v7.5.1/PowerShell-7.5.1-win-x64.zip"
$zipFile = "$env:TEMP\powershell-7.5.1.zip"
$installDir = Join-Path $PSScriptRoot "ps"
$pwshExe = Join-Path $installDir "pwsh.exe"

function Add-ToUserPath($newPath) {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$newPath*") {
        $newPathString = "$currentPath;$newPath"
        [Environment]::SetEnvironmentVariable("Path", $newPathString, "User")
        Write-Host "Added to user {PATH} : $newPath"
    }
}

function Remove-FromUserPath($removePath) {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $filtered = ($currentPath -split ';') | Where-Object { $_ -ne $removePath } | Where-Object { $_ -ne "" }
    [Environment]::SetEnvironmentVariable("Path", ($filtered -join ';'), "User")
    Write-Host "Path deleted from user {PATH} : $removePath"
}

function Install-PS7 {
    if (-not (Test-Path $zipFile)) {
        Write-Host "Downloading PowerShell 7.5.1 ZIP..."
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile
    } else {
        Write-Host "Archive already downloaded : $zipFile"
    }

    Write-Host "Extracting in $installDir..."
    Expand-Archive -Path $zipFile -DestinationPath $installDir -Force

    if (Test-Path $pwshExe) {
        Add-ToUserPath $installDir
        Write-Host "PowerShell 7.5.1 ready for use in : $installDir"
    } else {
        Write-Host "Extract failed or file missing."
        exit 1
    }
}

function Remove-PS7 {
    if (Test-Path $installDir) {
        Write-Host "Removing $installDir..."
        Remove-Item -Recurse -Force $installDir
        Remove-FromUserPath $installDir
        Write-Host "PowerShell 7.5.1 uninstalled successfully."
    } else {
        Write-Host "Nothing to remove."
    }
}

switch ($Action) {
    "install"   { Install-PS7 }
    "uninstall" { Remove-PS7 }
}
