@echo off
echo ========================================
echo Testing Add Record to Database
echo ========================================
echo.

cd /d "%~dp0"
python test_add_record.py

echo.
echo ========================================
echo Test completed
echo ========================================
pause

