@echo off
echo 🎨 ArtDecorAI - Running Artwork CRUD Operations
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo 📦 Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
)

REM Run the CRUD operations
echo 🚀 Starting CRUD operations...
python run_crud.py

REM Pause to see results
echo.
echo Press any key to exit...
pause >nul
