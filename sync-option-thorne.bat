@echo off
REM Sync Thorne Option Backups - Wrapper for options_thorne_sync.py
REM Usage:
REM   sync-option-thorne.bat --window Spellbook
REM   sync-option-thorne.bat --all
REM   sync-option-thorne.bat --all --verbose
REM   sync-option-thorne.bat --window Cast --dry-run

setlocal

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=%SCRIPT_DIR%.venv\Scripts\python.exe"

REM Ensure relative paths resolve from repo root
pushd "%SCRIPT_DIR%" >nul

REM Prefer local venv python if available, otherwise fall back to system python
if not exist "%PYTHON_EXE%" (
    where py >nul 2>&1
    if %errorlevel%==0 (
        set "PYTHON_EXE=py -3"
    ) else (
        set "PYTHON_EXE=python"
    )
)

if "%~1"=="" (
    echo.
    echo Usage: sync-option-thorne.bat ^<options^>
    echo.
    echo Examples:
    echo   sync-option-thorne.bat --window Spellbook
    echo   sync-option-thorne.bat --all
    echo   sync-option-thorne.bat --all --verbose
    echo   sync-option-thorne.bat --window Spellbook --dry-run
    echo.
    exit /b 1
)

%PYTHON_EXE% "%SCRIPT_DIR%.bin\options_thorne_sync.py" %*

set "EXIT_CODE=%errorlevel%"
popd >nul

exit /b %EXIT_CODE%
