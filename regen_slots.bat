@echo off
REM regen_slots.bat - Wrapper to run .bin\regen_slots.py from PowerShell/CMD
REM Composites item atlases onto button backgrounds for themed inventory slots
REM Usage:
REM   regen_slots.bat                                      (Regenerate all slot variants)
REM   regen_slots.bat --all
REM   regen_slots.bat --all-combos                         (All class/theme combos)
REM   regen_slots.bat --class Thorne                       (Single class, all themes)
REM   regen_slots.bat --class Thorne --theme Gold          (Single class+theme combo)
REM   regen_slots.bat Gold Silver Bronze                   (Multiple variant names)
REM   regen_slots.bat --verbose                            (Detailed per-item output)
REM   regen_slots.bat --class Thorne --verbose             (Class regen with details)

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to --all
if "%~1"=="" (
    python "%SCRIPT_DIR%.bin\regen_slots.py" --all
) else (
    python "%SCRIPT_DIR%.bin\regen_slots.py" %*
)

exit /b %errorlevel%
