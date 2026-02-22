@echo off
REM Sync Option Script - Copy specific Options directory for testing
REM Usage: sync-option.bat <option_path>
REM Examples:
REM   sync-option.bat spellbook/large
REM   sync-option.bat inventory
REM   sync-option.bat spellbook

setlocal enabledelayedexpansion

if "%1"=="" (
    echo.
    echo Usage: sync-option.bat ^<option_path^>
    echo.
    echo Examples:
    echo   sync-option.bat spellbook/large
    echo   sync-option.bat inventory
    echo   sync-option.bat spellbook
    echo.
    exit /b 1
)

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "OPTION_PATH=%1"

REM Call the Python script
python "%SCRIPT_DIR%.bin\sync_option.py" "%OPTION_PATH%"

exit /b %errorlevel%
