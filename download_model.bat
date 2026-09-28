@echo off
title Downloading Local Vision Model

echo ========================================================
echo       Downloading Florence-2 Local Vision Model
echo ========================================================
echo.

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" "%~dp0download_model.py" microsoft/Florence-2-base

echo.
pause
