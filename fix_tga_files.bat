@echo off
REM fix_tga_files.bat - Wrapper to run .bin\fix_tga_files.py from PowerShell/CMD
REM Converts mislabeled PNG files (with .tga extension) to proper TGA format
REM
REM Usage:
REM   fix_tga_files.bat                                        (Default: --scan . recursively from current dir)
REM   fix_tga_files.bat gauge_inlay_thorne01.tga                    (Fix single file)
REM   fix_tga_files.bat thorne_drak\Options\Gauges            (Fix directory, non-recursive)
REM   fix_tga_files.bat --scan thorne_drak                    (Recursively scan and fix from thorne_drak)
REM   fix_tga_files.bat --check gauge_inlay_thorne01.tga            (Check single file without converting)
REM   fix_tga_files.bat --check --scan .                      (Check all files recursively)

setlocal
set "SCRIPT_DIR=%~dp0"

REM If no arguments provided, default to scanning current directory
if "%~1"=="" (
    python "%SCRIPT_DIR%.bin\fix_tga_files.py" --scan .
) else (
    python "%SCRIPT_DIR%.bin\fix_tga_files.py" %*
)

exit /b %errorlevel%
