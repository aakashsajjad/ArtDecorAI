@echo off
echo 🎨 ArtDecorAI - Running Direct CRUD Demo (No Database Required)
echo ================================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Run the direct CRUD demo
echo 🚀 Starting Direct CRUD Demo...
python direct_crud_demo.py

REM Pause to see results
echo.
echo Press any key to exit...
pause >nul

