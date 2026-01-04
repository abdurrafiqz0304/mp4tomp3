@echo off
title MP3 Turbo Downloader - ULTIMATE SETUP
echo ==================================================
echo      MP3 TURBO DOWNLOADER - AUTO SETUP
echo ==================================================
echo.

:: --- STEP 1: CHECK PYTHON ---
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is found.
    goto :install_libs
)

:: --- PYTHON NOT FOUND: AUTO INSTALLER ---
echo [ALERT] Python is NOT installed on this computer.
echo.
echo We can download and install it for you automatically.
set /p ask_py=">>> Do you want to install Python now? (y/n): "

if /i "%ask_py%" neq "y" (
    echo [ERROR] Cannot proceed without Python. Exiting.
    pause
    exit /b
)

echo.
echo [INFO] Downloading Python Installer (approx 25MB)...
:: Download Python 3.12 (Stable)
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe' -OutFile 'python_setup.exe'"

echo [INFO] Installing Python... (Please wait, this may take 1-2 minutes)
echo        * Installing silently...
echo        * Adding to System PATH...

:: Install silently and force Add to Path
start /wait python_setup.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

:: Cleanup installer file
del python_setup.exe

echo.
echo [SUCCESS] Python has been installed!
echo ==================================================
echo IMPORTANT: You must RESTART this installer.
echo ==================================================
echo Windows needs to refresh to recognize the new Python.
echo.
echo 1. Close this window.
echo 2. Double-click 'install.bat' again.
echo.
pause
exit

:install_libs
:: --- STEP 2: INSTALL LIBRARIES ---
echo.
echo [2/4] Installing required libraries...
:: Using 'python -m pip' to avoid pip path errors
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install libraries. Check internet connection.
    pause
    exit /b
)
echo [OK] Libraries installed.

:: --- STEP 3: FFMPEG CHECK ---
echo.
echo [3/4] Checking for FFmpeg...
if exist "ffmpeg.exe" (
    echo [OK] FFmpeg already exists.
) else (
    echo [INFO] FFmpeg not found. Downloading automatically...
    
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'"
    
    echo [INFO] Extracting FFmpeg...
    powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg_temp'"
    
    echo [INFO] Configuring files...
    move "ffmpeg_temp\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "%~dp0" >nul
    
    del "ffmpeg.zip"
    rmdir /s /q "ffmpeg_temp"
    
    if exist "ffmpeg.exe" (
        echo [OK] FFmpeg installed!
    ) else (
        echo [ERROR] Download failed. Check internet.
    )
)

:: --- STEP 4: CREATE SHORTCUT ---
echo.
echo [4/4] Creating 'mp3' shortcut...
set "CurrentDir=%~dp0"
if "%CurrentDir:~-1%"=="\" set "CurrentDir=%CurrentDir:~0,-1%"

echo %PATH% | find /i "%CurrentDir%" >nul
if %errorlevel% equ 0 (
    echo [INFO] Shortcut already active.
) else (
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%CurrentDir%', 'User')"
    echo [SUCCESS] Shortcut created.
)

echo.
echo ==================================================
echo    SETUP COMPLETE!
echo ==================================================
echo.
echo Please restart your CMD / Terminal.
echo Then type 'mp3' to start.
echo.
pause
