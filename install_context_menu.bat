@echo off
setlocal enabledelayedexpansion
title Installing Local AI Renamer Context Menu

echo ========================================================
echo          Local AI Renamer - Context Menu Setup
echo ========================================================
echo.

set "SCRIPT_DIR=%~dp0"
:: Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

set "EXE_PATH=%SCRIPT_DIR%\LocalAIRenamer.exe"
if not exist "%EXE_PATH%" (
    set "EXE_PATH=%SCRIPT_DIR%\AutoImageRenamer.exe"
)
set "MAIN_PY=%SCRIPT_DIR%\main.py"
set "ICON_PATH=%SCRIPT_DIR%\assets\app_icon.ico"

:: Determine command to execute
if exist "%EXE_PATH%" (
    echo [OK] Found standalone executable: %EXE_PATH%
    set "CMD_FOLDER=\"%EXE_PATH%\" \"%%1\""
    set "CMD_BG=\"%EXE_PATH%\" \"%%V\""
) else (
    echo [Notice] Standalone executable not found yet. Using Python script runner.
    set "CMD_FOLDER=python \"%MAIN_PY%\" \"%%1\""
    set "CMD_BG=python \"%MAIN_PY%\" \"%%V\""
)

echo Registering context menu in Windows Explorer...

:: Clean up legacy key if present
reg delete "HKCU\Software\Classes\Directory\shell\AutoImageRenamer" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Directory\Background\shell\AutoImageRenamer" /f >nul 2>&1

:: 1. Register for clicking ON a folder
reg add "HKCU\Software\Classes\Directory\shell\LocalAIRenamer" /ve /d "Rename with Local AI" /f >nul
if exist "%ICON_PATH%" (
    reg add "HKCU\Software\Classes\Directory\shell\LocalAIRenamer" /v "Icon" /d "%ICON_PATH%" /f >nul
)
reg add "HKCU\Software\Classes\Directory\shell\LocalAIRenamer\command" /ve /d "%CMD_FOLDER%" /f >nul

:: 2. Register for clicking ON EMPTY BACKGROUND inside a folder
reg add "HKCU\Software\Classes\Directory\Background\shell\LocalAIRenamer" /ve /d "Rename with Local AI" /f >nul
if exist "%ICON_PATH%" (
    reg add "HKCU\Software\Classes\Directory\Background\shell\LocalAIRenamer" /v "Icon" /d "%ICON_PATH%" /f >nul
)
reg add "HKCU\Software\Classes\Directory\Background\shell\LocalAIRenamer\command" /ve /d "%CMD_BG%" /f >nul

echo.
echo ========================================================
echo [SUCCESS] Windows Context Menu installed successfully!
echo.
echo You can now:
echo  1. Right-click any folder in Windows Explorer.
echo  2. Click 'Rename with Local AI'.
echo  3. The AI model will load into memory, rename your images,
echo     and immediately unload to free 100%% of GPU memory!
echo ========================================================
echo.
pause
