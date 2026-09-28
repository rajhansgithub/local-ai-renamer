@echo off
setlocal enabledelayedexpansion
title Setting Up Local AI Renamer Environment

echo ========================================================
echo          Local AI Renamer - Environment Setup
echo ========================================================
echo.

:: Check for python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [Error] Python was not found in your PATH.
        echo Please ensure Python 3.10, 3.11, or 3.12 is installed and added to PATH.
        echo You can download it from https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set "PY_CMD=py"
    )
) else (
    set "PY_CMD=python"
)

echo [1/4] Found Python: %PY_CMD%

:: Create venv if not already created
if not exist "%~dp0.venv" (
    echo [2/4] Creating dedicated virtual environment in .venv...
    %PY_CMD% -m venv "%~dp0.venv"
) else (
    echo [2/4] Virtual environment .venv already exists.
)

set "VENV_PYTHON=%~dp0.venv\Scripts\python.exe"
set "VENV_PIP=%~dp0.venv\Scripts\pip.exe"

echo [3/4] Installing PyTorch with CUDA 12.1+ acceleration (NVIDIA GPU / CUDA)...
"%VENV_PIP%" install --upgrade pip
"%VENV_PIP%" install torch torchvision --index-url https://download.pytorch.org/whl/cu121

echo [4/4] Installing AI vision and GUI dependencies...
"%VENV_PIP%" install -r "%~dp0requirements.txt"

echo.
echo ========================================================
echo [SUCCESS] Environment is fully configured!
echo.
echo Next steps:
echo  1. Run 'install_context_menu.bat' to add the right-click menu.
echo  2. Or run 'build_exe.bat' to package into a standalone .exe.
echo ========================================================
echo.
pause
