@echo off
echo 🎨 ArtDecorAI - Running Artwork Examples (Database Mode)
echo ========================================================
echo 📝 This version requires a database connection
echo ========================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist ..\requirements.txt (
    echo 📦 Installing dependencies...
    python -m pip install -r ..\requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
)

REM Run the artwork examples
echo 🚀 Starting Artwork Examples (Database Mode)...
echo ⚠️  Make sure Supabase is running and database is connected
python artwork_examples.py

REM Pause to see results
echo.
echo Press any key to exit...
pause >nul

