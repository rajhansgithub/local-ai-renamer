@echo off
setlocal enabledelayedexpansion
title Building AutoImageRenamer.exe

echo ========================================================
echo        Building AutoImageRenamer Standalone EXE
echo ========================================================
echo.

:: Detect Python or Venv Python
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    set "PYINSTALLER_EXE=%~dp0.venv\Scripts\pyinstaller.exe"
) else (
    set "PYTHON_EXE=python"
    set "PYINSTALLER_EXE=pyinstaller"
)

echo Checking for PyInstaller...
"%PYTHON_EXE%" -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    "%PYTHON_EXE%" -m pip install pyinstaller
)

echo.
echo Compiling LocalAIRenamer.exe (this may take 1-2 minutes)...

"%PYINSTALLER_EXE%" --noconfirm --onedir --windowed ^
    --name "LocalAIRenamer" ^
    --icon "assets\app_icon.ico" ^
    --add-data "config.json;." ^
    --hidden-import "PIL" ^
    --hidden-import "PIL.Image" ^
    --hidden-import "PIL.ImageTk" ^
    --hidden-import "transformers" ^
    --hidden-import "torch" ^
    --hidden-import "timm" ^
    --hidden-import "einops" ^
    --hidden-import "google.genai" ^
    --hidden-import "tkinter" ^
    --hidden-import "tkinter.ttk" ^
    --hidden-import "winreg" ^
    main.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo [SUCCESS] LocalAIRenamer.exe built successfully!
    echo Output directory: dist\LocalAIRenamer\
    echo.
    echo Copying executable to workspace root for quick access...
    copy /y "dist\LocalAIRenamer\LocalAIRenamer.exe" "%~dp0LocalAIRenamer.exe" >nul 2>&1
    copy /y "dist\LocalAIRenamer\LocalAIRenamer.exe" "%~dp0AutoImageRenamer.exe" >nul 2>&1
    echo.
    echo You can now run 'install_context_menu.bat' to register it!
    echo ========================================================
) else (
    echo.
    echo [Error] Build failed. Please check the error messages above.
)

echo.
pause
