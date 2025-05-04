param (
    [string]$TargetScript,
    [string]$Arg1 = "install"
)

$ps7 = Join-Path $PSScriptRoot "ps\pwsh.exe"
Start-Process -FilePath $ps7 -ArgumentList "-ExecutionPolicy Bypass -File `"$TargetScript`" $Arg1" -Verb RunAs
