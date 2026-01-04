@echo off
title MP3 Turbo Downloader - SUPER FAST SETUP
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
echo [ALERT] Python is NOT installed.
echo.
set /p ask_py=">>> Install Python automatically? (y/n): "

if /i "%ask_py%" neq "y" (
    echo [ERROR] Cannot proceed without Python. Exiting.
    pause
    exit /b
)

echo.
echo [INFO] Downloading Python...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe' -OutFile 'python_setup.exe'"

echo [INFO] Installing Python (Silent Mode)...
start /wait python_setup.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
del python_setup.exe

echo.
echo [SUCCESS] Python installed! Restarting installer...
timeout /t 2 >nul
start "" "%~f0"
exit

:install_libs
:: --- STEP 2: INSTALL LIBRARIES ---
echo.
echo [2/4] Installing libraries...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed. Check internet.
    pause
    exit /b
)
echo [OK] Libraries installed.

:: --- STEP 3: FFMPEG CHECK (TURBO MODE) ---
echo.
echo [3/4] Checking for FFmpeg...
if exist "ffmpeg.exe" (
    echo [OK] FFmpeg already exists.
) else (
    echo [INFO] Downloading FFmpeg...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'"
    
    echo [INFO] Extracting... (Using High-Speed TAR)
    :: GUNA TAR - LAJU GILA BANDING POWERSHELL
    tar -xf ffmpeg.zip
    
    echo [INFO] Configuring...
    :: Pindahkan fail dari folder yang diextract
    move "ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "%~dp0" >nul
    
    :: Cuci sampah
    del "ffmpeg.zip"
    rmdir /s /q "ffmpeg-master-latest-win64-gpl"
    
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

start "MP3 Turbo Downloader" cmd /k "echo Welcome! & mp3"
exit
