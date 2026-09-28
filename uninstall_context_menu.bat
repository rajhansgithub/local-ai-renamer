@echo off
title Uninstalling Auto Image Renamer Context Menu

echo ========================================================
echo     Local Auto Image Renamer - Uninstall Context Menu
echo ========================================================
echo.

echo Removing context menu registry keys...

reg delete "HKCU\Software\Classes\Directory\shell\LocalAIRenamer" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Directory\Background\shell\LocalAIRenamer" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Directory\shell\AutoImageRenamer" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Directory\Background\shell\AutoImageRenamer" /f >nul 2>&1

echo.
echo ========================================================
echo [SUCCESS] Windows Context Menu uninstalled cleanly.
echo ========================================================
echo.
pause
