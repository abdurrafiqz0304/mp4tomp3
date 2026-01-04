@echo off
title MP3 Turbo Downloader - Installation
echo ==================================================
echo      MP3 TURBO DOWNLOADER INSTALLATION
echo ==================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python first.
    pause
    exit /b
)

:: 2. Install Dependencies
echo [INFO] Installing required libraries...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install libraries. Check your internet connection.
    pause
    exit /b
)

:: 3. Add to Windows PATH (User Scope)
echo.
echo [INFO] Configuring system path...
:: This command gets the current folder and adds it to the User Path safely
set "CurrentDir=%~dp0"
:: Remove trailing backslash
if "%CurrentDir:~-1%"=="\" set "CurrentDir=%CurrentDir:~0,-1%"

:: Check if already in PATH to avoid duplicates
echo %PATH% | find /i "%CurrentDir%" >nul
if %errorlevel% equ 0 (
    echo [INFO] Path already configured. Skipping.
) else (
    :: Use PowerShell to modify the User Environment Variable (Safer than setx)
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%CurrentDir%', 'User')"
    echo [SUCCESS] Folder added to Environment Variables.
)

echo.
echo ==================================================
echo    INSTALLATION COMPLETE!
echo ==================================================
echo.
echo Please RESTART your Command Prompt (CMD).
echo Then, type 'mp3' to start the tool.
echo.
pause