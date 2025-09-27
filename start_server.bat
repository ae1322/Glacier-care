@echo off
echo Starting Glacier Care API...
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found
    echo Please run setup.py first or create .env file manually
    pause
    exit /b 1
)

REM Start the server
echo Starting Flask server...
python start_server.py

pause
