@echo off
REM regen_gems.bat - Wrapper to run .bin\regen_gems.py from PowerShell/CMD
REM Usage:
REM   regen_gems.bat                                       (Default: --all variants)
REM   regen_gems.bat --all
REM   regen_gems.bat Thorne
REM   regen_gems.bat Thorne Classic
REM   regen_gems.bat Thorne --border
REM   regen_gems.bat Thorne --border black

setlocal
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to processing all variants
if "%~1"=="" (
    python "%SCRIPT_DIR%.bin\regen_gems.py" --all
) else (
    python "%SCRIPT_DIR%.bin\regen_gems.py" %*
)

exit /b %errorlevel%
