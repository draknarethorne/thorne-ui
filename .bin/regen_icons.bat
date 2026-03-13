@echo off
REM regen_icons.bat - Wrapper to run regen_icons.py from .bin directory
REM Usage:
REM   regen_icons.bat                                      (Default: --all variants)
REM   regen_icons.bat --all
REM   regen_icons.bat Thorne
REM   regen_icons.bat Thorne Classic
REM   regen_icons.bat Thorne --labels

setlocal
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to processing all variants
if "%~1"=="" (
    python "%SCRIPT_DIR%regen_icons.py" --all
) else (
    python "%SCRIPT_DIR%regen_icons.py" %*
)

exit /b %errorlevel%
