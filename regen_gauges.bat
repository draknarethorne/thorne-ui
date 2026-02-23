@echo off
REM regen_gauges.bat - Wrapper to run .bin\regen_gauges.py from PowerShell/CMD
REM Regenerates tall (120×64) and wide (120×32) gauge textures from source files
REM
REM Usage:
REM   regen_gauges.bat                                       (Default: --all variants)
REM   regen_gauges.bat --all
REM   regen_gauges.bat Thorne
REM   regen_gauges.bat Thorne Bars
REM   regen_gauges.bat --help

setlocal
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to processing all variants
if "%~1"=="" (
    python "%SCRIPT_DIR%.bin\regen_gauges.py" --all
) else (
    python "%SCRIPT_DIR%.bin\regen_gauges.py" %*
)

exit /b %errorlevel%
