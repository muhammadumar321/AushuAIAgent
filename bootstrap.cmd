@echo off
REM Simple CMD bootstrap for Windows (cmd.exe)
REM Usage: bootstrap.cmd

where python >nul 2>nul
if %errorlevel% neq 0 (
  echo Python not found in PATH. Please install Python 3.10+ and add to PATH.
  exit /b 1
)

python -m venv .venv
if %errorlevel% neq 0 (
  echo Failed to create virtualenv
  exit /b 1
)

.venv\Scripts\pip.exe install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
  echo Failed to upgrade pip
  exit /b 1
)

if exist requirements.txt (
  .venv\Scripts\pip.exe install -r requirements.txt
)

for %%p in (packages\ai packages\core packages\permissions) do (
  if exist %%p (
    .venv\Scripts\pip.exe install -e %%p
  )
)

echo Bootstrap complete.
echo Activate with:

echo    . .venv\Scripts\activate.bat

echo Run tests with:

echo    python -m unittest discover -s packages -p "test_*.py" -v
