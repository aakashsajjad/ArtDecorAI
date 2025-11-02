@echo off
echo ========================================
echo Starting FastAPI Server
echo ========================================
echo.
echo 📡 Server binding: 0.0.0.0:8000 (all interfaces)
echo.
echo 🌐 Access your server at:
echo    • http://localhost:8000
echo    • http://127.0.0.1:8000
echo.
echo 📚 API Documentation:
echo    • Swagger UI: http://localhost:8000/docs
echo    • ReDoc: http://localhost:8000/redoc
echo.
echo ⚠️  Note: Use localhost or 127.0.0.1 (NOT 0.0.0.0) in browser!
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

cd /d "%~dp0"

REM Check if uvicorn is installed
python -c "import uvicorn" 2>nul
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install fastapi uvicorn
)

echo Starting FastAPI server...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
