@echo off
REM regen_thorne.bat - Wrapper to run .bin\regen_thorne.py from PowerShell/CMD
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

exit /b %errorlevel%
