@echo off
title MP3 Turbo Downloader - Installation & Setup
echo ==================================================
echo      MP3 TURBO DOWNLOADER - AUTO SETUP
echo ==================================================
echo.

:: 1. Check for Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python first.
    pause
    exit /b
)
echo [OK] Python is found.

:: 2. Install Python Libraries
echo.
echo [2/4] Installing required Python libraries...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install libraries. Check internet connection.
    pause
    exit /b
)
echo [OK] Libraries installed.

:: 3. Auto-Download FFmpeg (The Magic Part)
echo.
echo [3/4] Checking for FFmpeg...
if exist "ffmpeg.exe" (
    echo [OK] FFmpeg already exists. Skipping download.
) else (
    echo [INFO] FFmpeg not found. Downloading automatically...
    echo        (This may take a minute depending on your internet)
    
    :: Download FFmpeg Zip using PowerShell
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'"
    
    echo [INFO] Extracting FFmpeg...
    powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg_temp'"
    
    echo [INFO] Configuring files...
    :: Move ffmpeg.exe to main folder
    move "ffmpeg_temp\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "%~dp0" >nul
    
    :: Clean up rubbish
    del "ffmpeg.zip"
    rmdir /s /q "ffmpeg_temp"
    
    if exist "ffmpeg.exe" (
        echo [OK] FFmpeg downloaded and installed successfully!
    ) else (
        echo [ERROR] Automatic download failed. You may need to download ffmpeg.exe manually.
    )
)

:: 4. Add to Windows PATH
echo.
echo [4/4] Creating 'mp3' command shortcut...
set "CurrentDir=%~dp0"
if "%CurrentDir:~-1%"=="\" set "CurrentDir=%CurrentDir:~0,-1%"

echo %PATH% | find /i "%CurrentDir%" >nul
if %errorlevel% equ 0 (
    echo [INFO] Shortcut already exists.
) else (
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%CurrentDir%', 'User')"
    echo [SUCCESS] Shortcut created.
)

echo.
echo ==================================================
echo    SETUP COMPLETE!
echo ==================================================
echo.
echo You can now open any Command Prompt and type:
echo    mp3
echo.
pause