@echo off
REM regen_thorne.bat - Wrapper to run .bin\regen_thorne.py from PowerShell/CMD
REM Regenerates item atlases, then updates all slot variants
REM Usage:
REM   regen_thorne.bat                                     (Default: .Master directory)
REM   regen_thorne.bat .Master
REM   regen_thorne.bat CustomVariant
REM   regen_thorne.bat --all-classes                       (Generate .Master + class overrides)

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to .Master directory
if "%~1"=="" (
    python "%SCRIPT_DIR%.bin\regen_thorne.py" .Master
) else (
    python "%SCRIPT_DIR%.bin\regen_thorne.py" %*
)

if %errorlevel% neq 0 (
    echo Error: regen_thorne.py failed with exit code %errorlevel%
    exit /b %errorlevel%
)

echo.
echo ======================================================================
echo Regenerating slot variants...
echo ======================================================================

set "RUN_ALL_COMBOS=0"
set "CLASS_NAME="
set "EXPECT_CLASS=0"
for %%A in (%*) do (
    if /I "%%~A"=="--all-classes" set "RUN_ALL_COMBOS=1"
    if /I "%%~A"=="--class" set "EXPECT_CLASS=1"
    if "!EXPECT_CLASS!"=="1" if /I not "%%~A"=="--class" (
        set "CLASS_NAME=%%~A"
        set "EXPECT_CLASS=0"
    )
)

if "%RUN_ALL_COMBOS%"=="1" (
    call "%SCRIPT_DIR%regen_slots.bat" --all-combos
) else if not "%CLASS_NAME%"=="" (
    call "%SCRIPT_DIR%regen_slots.bat" --class %CLASS_NAME%
) else (
    call "%SCRIPT_DIR%regen_slots.bat" --all
)
