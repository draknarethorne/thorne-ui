@echo off
REM ============================================================================
REM Thorne UI Sync Script
REM ============================================================================
REM Purpose: Sync thorne_drak UI files from development to TAKP game directory
REM Author: Draknare Thorne
REM ============================================================================

echo.
echo ========================================
echo   Thorne UI Sync Script
echo ========================================
echo.

REM Define source and destination paths
set "SOURCE_DIR=%~dp0thorne_drak"
set "DEST_DIR=C:\TAKP\uifiles\thorne_dev"

echo Source: %SOURCE_DIR%
echo Destination: %DEST_DIR%
echo.

REM Verify source directory exists
if not exist "%SOURCE_DIR%" (
    echo ERROR: Source directory not found!
    echo %SOURCE_DIR%
    pause
    exit /b 1
)

REM Create destination directory if it doesn't exist
if not exist "%DEST_DIR%" (
    echo Creating destination directory...
    mkdir "%DEST_DIR%"
)

echo Starting sync...
echo.

REM ROBOCOPY Options:
REM /MIR     - Mirror (delete files in destination that don't exist in source)
REM /R:2     - Retry 2 times on failed copies
REM /W:3     - Wait 3 seconds between retries
REM /NP      - No progress (cleaner output)
REM /NDL     - No directory list
REM /NFL     - No file list (comment out to see files being copied)
REM /XD      - Exclude directories
REM /XF      - Exclude files

ROBOCOPY "%SOURCE_DIR%" "%DEST_DIR%" /MIR /R:2 /W:3 /NP /NDL ^
    /XD ".git" "__pycache__" ".vscode" ^
    /XF "*.backup_*" "*.bak" "*.old" "*.tmp" ".DS_Store" "Thumbs.db"

REM ROBOCOPY exit codes:
REM 0 = No files copied (no changes)
REM 1 = Files copied successfully
REM 2 = Extra files/directories detected (and removed with /MIR)
REM 3 = Files copied + extra files removed
REM 4+ = Errors occurred

if %ERRORLEVEL% GEQ 8 (
    echo.
    echo ERROR: Sync failed with errors!
    echo Error level: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo No changes detected - already in sync!
)

if %ERRORLEVEL% EQU 1 (
    echo.
    echo Files copied successfully!
)

if %ERRORLEVEL% EQU 2 (
    echo.
    echo Extra files removed from destination!
)

if %ERRORLEVEL% EQU 3 (
    echo.
    echo Files copied and extra files removed!
)

echo.
echo ========================================
echo   Sync Complete!
echo ========================================
echo.
echo thorne_drak UI is ready to test in TAKP
echo In-game command: /loadskin thorne_drak
echo.

pause
