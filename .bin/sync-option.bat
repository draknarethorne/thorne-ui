@echo off
REM Sync Option Script - Copy specific Options directory for testing
REM Usage: sync-option.bat <option_path>
REM Examples:
REM   sync-option.bat spellbook/large
REM   sync-option.bat inventory
REM   sync-option.bat spellbook
REM   sync-option.bat "Music/Thorne 14 Row"

setlocal

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

if "%~1"=="" (
    echo.
    echo Usage: sync-option.bat ^<option_path^>
    echo.
    echo Examples:
    echo   sync-option.bat spellbook/large
    echo   sync-option.bat inventory
    echo   sync-option.bat spellbook
    echo   sync-option.bat "Music/Thorne 14 Row"
    echo.
    python "%SCRIPT_DIR%sync_option.py" --help
    exit /b 1
)

REM Pass all original arguments through to Python (supports spaces, flags, etc.)
python "%SCRIPT_DIR%sync_option.py" %*

exit /b %errorlevel%
