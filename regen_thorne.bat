@echo off
REM regen_thorne.bat - Wrapper to run .bin\regen_thorne.py from PowerShell/CMD
REM Regenerates item atlases, then updates all slot variants
REM Usage:
REM   regen_thorne.bat                                     (Default: .Master directory)
REM   regen_thorne.bat .Master
REM   regen_thorne.bat CustomVariant

setlocal
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to .Master directory
if "%~1"=="" (
    python "%SCRIPT_DIR%.bin\regen_thorne.py" .Master
) else (
    python "%SCRIPT_DIR%.bin\regen_thorne.py" %*
)

if %errorlevel% neq 0 (
    echo Error: regen_thorne.py failed with exit code %errorlevel%
    exit /b %errorlevel%
)

echo.
echo ======================================================================
echo Regenerating slot variants...
echo ======================================================================
call "%SCRIPT_DIR%regen_slots.bat" --all
