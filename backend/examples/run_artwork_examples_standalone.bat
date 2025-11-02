@echo off
echo 🎨 ArtDecorAI - Running Artwork Examples (Standalone Mode)
echo ===========================================================
echo 📝 This version works without requiring a database connection
echo ===========================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Run the standalone artwork examples
echo 🚀 Starting Artwork Examples (Standalone Mode)...
python artwork_examples_standalone.py

REM Pause to see results
echo.
echo Press any key to exit...
pause >nul

