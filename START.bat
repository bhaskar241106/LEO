@echo off
TITLE Leo AI - Start
color 0A
cls
echo.
echo ================================================================
echo   LEO AI - STARTING
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/3] Starting Backend...
cd backend
start "Leo Backend" cmd /k "venv\Scripts\python.exe main.py"
cd ..
timeout /t 5 /nobreak >nul
echo   Backend: http://localhost:8000
echo.

echo [2/3] Starting Frontend...
cd frontend
start "Leo Frontend" cmd /k "npm run dev"
cd ..
timeout /t 5 /nobreak >nul
echo   Frontend: http://localhost:5173
echo.

echo [3/3] Opening Browser...
timeout /t 8 /nobreak >nul
start http://localhost:5173
echo.

echo ================================================================
echo   LEO AI IS RUNNING
echo ================================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo To stop: Run STOP.bat
echo.
pause
