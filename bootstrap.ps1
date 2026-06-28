# PowerShell bootstrap for Windows
# Usage: Open PowerShell (preferably as normal user) and run:
#   .\bootstrap.ps1

param()

function Write-Info($msg) { Write-Host $msg -ForegroundColor Cyan }
function Write-Err($msg) { Write-Host $msg -ForegroundColor Red }

# Find python
$pythonCmd = "python"
$python = Get-Command $pythonCmd -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Err "Python not found in PATH. Please install Python 3.10+ and ensure 'python' is on PATH."
    exit 1
}

Write-Info "Creating virtual environment .venv ..."
& $pythonCmd -m venv .venv
if ($LASTEXITCODE -ne 0) { Write-Err "Failed to create virtualenv"; exit 1 }

$pip = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\pip.exe"
$pythonInVenv = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\python.exe"

if (-not (Test-Path $pip)) {
    Write-Err "pip not found in .venv. Activation might be required or the venv creation failed."
    exit 1
}

Write-Info "Upgrading pip..."
& $pip install --upgrade pip setuptools wheel

if (Test-Path "requirements.txt") {
    Write-Info "Installing requirements.txt..."
    & $pip install -r requirements.txt
}

# Install editable packages in workspace
$packages = @("packages/ai","packages/core","packages/permissions")
foreach ($p in $packages) {
    if (Test-Path $p) {
        Write-Info "Installing editable package: $p"
        & $pip install -e $p
    }
}

Write-Info "Bootstrap complete. Activate the venv with (PowerShell):"
Write-Host "  . \.venv\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "Or in CMD: .\.venv\Scripts\activate.bat" -ForegroundColor Green

Write-Info "To run tests:" 
Write-Host "  python -m unittest discover -s packages -p 'test_*.py' -v" -ForegroundColor Yellow

Write-Info "If PowerShell execution policy prevents running scripts, you can temporarily bypass with:" 
Write-Host "  powershell -ExecutionPolicy Bypass -File .\\bootstrap.ps1" -ForegroundColor Yellow
