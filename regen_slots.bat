@echo off
REM regen_slots.bat - Wrapper to run .bin\regen_slots.py from PowerShell/CMD
REM Usage:
REM   regen_slots.bat                                      (Regenerate all slot variants)
REM   regen_slots.bat --all
REM   regen_slots.bat Gold
REM   regen_slots.bat Metal Patriot

setlocal
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to --all
if "%~1"=="" (
    python "%SCRIPT_DIR%.bin\regen_slots.py" --all
) else (
    python "%SCRIPT_DIR%.bin\regen_slots.py" %*
)

exit /b %errorlevel%
