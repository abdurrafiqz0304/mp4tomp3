@echo off
title MP3 Turbo Downloader - UNINSTALLER
color 0c
echo ==================================================
echo      MP3 TURBO DOWNLOADER - UNINSTALLATION
echo ==================================================
echo.
echo This script will:
echo 1. Remove the 'mp3' shortcut from your System PATH.
echo 2. Optionally uninstall the Python library (yt-dlp).
echo.
echo [WARNING] This action cannot be undone.
echo.
pause

:: 1. Remove from Windows PATH
echo.
echo [1/2] Removing 'mp3' command from System...
set "TargetDir=%~dp0"
:: Remove trailing backslash for matching
if "%TargetDir:~-1%"=="\" set "TargetDir=%TargetDir:~0,-1%"

:: Use PowerShell to cleanly remove the path from User Environment Variables
powershell -Command "$path = [Environment]::GetEnvironmentVariable('Path', 'User'); $newPath = ($path -split ';' | Where-Object { $_ -ne '%TargetDir%' }) -join ';'; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')"

echo [SUCCESS] System PATH cleaned. The 'mp3' command is removed.

:: 2. Uninstall Python Library (Optional)
echo.
echo [2/2] Do you want to uninstall the 'yt-dlp' library?
echo (Only say YES if you don't use yt-dlp for other projects)
set /p del_lib="Type 'y' to uninstall, or Enter to skip: "

if /i "%del_lib%"=="y" (
    echo Uninstalling yt-dlp...
    python -m pip uninstall yt-dlp -y
    echo [OK] Library removed.
) else (
    echo [SKIP] Library kept.
)

echo.
echo ==================================================
echo    UNINSTALLATION FINISHED
echo ==================================================
echo.
echo NOTE: Since this script is running inside the folder,
echo it cannot delete the folder automatically.
echo.
echo Please manually DELETE this folder:
echo "%TargetDir%"
echo.
echo Goodbye!
pause
