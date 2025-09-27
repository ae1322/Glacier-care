@echo off
echo Starting Glacier Care - Full Stack Application
echo ========================================================

echo.
echo Step 1: Starting Flask Backend API...
start "Flask Backend" cmd /k "python run_server.py"

echo.
echo Step 2: Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 3: Starting React Frontend...
start "React Frontend" cmd /k "npm run dev"

echo.
echo ========================================================
echo Both servers are starting up!
echo.
echo Flask Backend: http://localhost:5000
echo React Frontend: http://localhost:8082 (or check the new window)
echo.
echo Press any key to exit this window...
pause >nul
