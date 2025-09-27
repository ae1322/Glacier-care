@echo off
echo Starting Glacier Care Application...
echo.

echo Starting Backend Server (Flask)...
start "Backend Server" cmd /k "python app.py"

echo Waiting 3 seconds...
timeout /t 3 /nobreak > nul

echo Starting Frontend Server (React)...
start "Frontend Server" cmd /k "npm run dev"

echo.
echo Both servers are starting...
echo Frontend: http://localhost:8080
echo Backend: http://localhost:5000
echo.
echo Press any key to exit...
pause > nul
