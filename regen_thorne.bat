@echo off
REM regen_thorne.bat - Wrapper to run .bin\regen_thorne.py from PowerShell/CMD
REM Generates grayscale item atlases from dragitem source files, auto-triggers slot regen
REM Usage:
REM   regen_thorne.bat                                     (Default: .Master directory)
REM   regen_thorne.bat .Master
REM   regen_thorne.bat --class Thorne                      (Generate single class + auto-regen slots)
REM   regen_thorne.bat --all-classes                       (Generate .Master + all class overrides)
REM   regen_thorne.bat --verbose                           (Detailed per-item output)
REM   regen_thorne.bat --class Thorne --verbose            (Class regen with details)

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
set "HAS_VERBOSE=0"
set "EXPECT_CLASS=0"
for %%A in (%*) do (
    if /I "%%~A"=="--all-classes" set "RUN_ALL_COMBOS=1"
    if /I "%%~A"=="--class" set "EXPECT_CLASS=1"
    if /I "%%~A"=="--verbose" set "HAS_VERBOSE=1"
    if "!EXPECT_CLASS!"=="1" if /I not "%%~A"=="--class" (
        set "CLASS_NAME=%%~A"
        set "EXPECT_CLASS=0"
    )
)

set "VERBOSE_FLAG="
if "%HAS_VERBOSE%"=="1" set "VERBOSE_FLAG=--verbose"

if "%RUN_ALL_COMBOS%"=="1" (
    call "%SCRIPT_DIR%regen_slots.bat" --all-combos %VERBOSE_FLAG%
) else if not "%CLASS_NAME%"=="" (
    call "%SCRIPT_DIR%regen_slots.bat" --class %CLASS_NAME% %VERBOSE_FLAG%
) else (
    call "%SCRIPT_DIR%regen_slots.bat" --all %VERBOSE_FLAG%
)
