@echo off
echo ========================================
echo Testing Add Embedding to Database
echo ========================================
echo.

cd /d "%~dp0"
python test_add_embedding.py

echo.
echo ========================================
echo Test completed
echo ========================================
pause

