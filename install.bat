@echo off
title MP3 Turbo Downloader - ULTIMATE AUTO SETUP
echo ==================================================
echo      MP3 TURBO DOWNLOADER - AUTO SETUP
echo ==================================================
echo.

:: --- STEP 1: CHECK PYTHON ---
echo [1/4] Checking Python installation...
:: Cuba panggil python. Kalau error, maksudnya tak ada.
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is found.
    goto :install_libs
)

:: --- PYTHON NOT FOUND: AUTO INSTALLER ---
echo [ALERT] Python is NOT installed on this computer.
echo.
echo We need to install Python to run this tool.
set /p ask_py=">>> Install Python automatically? (y/n): "

if /i "%ask_py%" neq "y" (
    echo [ERROR] Cannot proceed without Python. Exiting.
    pause
    exit /b
)

echo.
echo [INFO] Downloading Python Installer...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe' -OutFile 'python_setup.exe'"

echo [INFO] Installing Python... (Please wait...)
:: Install senyap-senyap & paksa masuk PATH
start /wait python_setup.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

:: Buang fail installer
del python_setup.exe

echo.
echo [SUCCESS] Python installed! Restarting installer...
timeout /t 2 >nul

:: --- MAGIC PART 1: AUTO RESTART ---
:: Start balik script ini dalam window baru
start "" "%~f0"
:: Tutup window lama ni
exit

:install_libs
:: --- STEP 2: INSTALL LIBRARIES ---
echo.
echo [2/4] Installing required libraries...
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
    echo [INFO] Downloading FFmpeg...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'"
    
    echo [INFO] Extracting...
    powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg_temp'"
    
    echo [INFO] Configuring...
    move "ffmpeg_temp\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "%~dp0" >nul
    del "ffmpeg.zip"
    rmdir /s /q "ffmpeg_temp"
    
    if exist "ffmpeg.exe" (
        echo [OK] FFmpeg installed!
    ) else (
        echo [ERROR] Download failed.
    )
)

:: --- STEP 4: CREATE SHORTCUT ---
echo.
echo [4/4] Finalizing setup...
set "CurrentDir=%~dp0"
if "%CurrentDir:~-1%"=="\" set "CurrentDir=%CurrentDir:~0,-1%"

echo %PATH% | find /i "%CurrentDir%" >nul
if %errorlevel% equ 0 (
    echo [INFO] Shortcut active.
) else (
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%CurrentDir%', 'User')"
    echo [SUCCESS] Shortcut created.
)

echo.
echo ==================================================
echo    SETUP COMPLETE! LAUNCHING APP...
echo ==================================================
timeout /t 3 >nul

:: --- MAGIC PART 2: AUTO LAUNCH ---
:: Buka CMD baru yang environment dia dah refresh, dan terus run 'mp3'
start "MP3 Turbo Downloader" cmd /k "echo Welcome! & mp3"

:: Tutup installer ni
exit
