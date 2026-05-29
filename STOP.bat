@echo off
TITLE Leo AI - Stop
color 0C
echo.
echo ================================================================
echo   LEO AI - STOPPING ALL SERVERS
echo ================================================================
echo.

echo Stopping Python backend...
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo   Backend stopped
) else (
    echo   No backend running
)

echo Stopping Node frontend...
taskkill /F /IM node.exe 2>nul
if %errorlevel% equ 0 (
    echo   Frontend stopped
) else (
    echo   No frontend running
)

echo.
echo ================================================================
echo   ALL SERVERS STOPPED
echo ================================================================
echo.
pause
