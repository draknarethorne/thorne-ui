# fix_tga_files.ps1
# Wrapper script for fix_tga_files.py

param(
    [string[]]$Arguments
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "fix_tga_files.py"

if (-not (Test-Path $pythonScript)) {
    Write-Host "❌ Error: fix_tga_files.py not found in $scriptDir" -ForegroundColor Red
    exit 1
}

# If no arguments provided, show help
if ($Arguments.Count -eq 0) {
    & python $pythonScript
    exit
}

# Pass arguments to Python script
& python $pythonScript @Arguments
