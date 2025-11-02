@echo off
echo Opening Supabase Dashboard...
echo.
echo Choose what you want to do:
echo.
echo 1. Add Service Role Key (recommended - bypasses RLS)
echo    - Will open: Settings / API page
echo.
echo 2. Add SQL Policy (adds INSERT permission)
echo    - Will open: SQL Editor
echo.
choice /C 12 /M "Enter choice"

if errorlevel 2 goto :sql
if errorlevel 1 goto :api

:api
start https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api
echo.
echo ========================================
echo Steps:
echo 1. Find "service_role" key
echo 2. Copy it
echo 3. Open backend/.env
echo 4. Add: SUPABASE_SERVICE_ROLE_KEY=paste-key-here
echo 5. Save and run: python test_add_record.py
echo ========================================
goto :end

:sql
start https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/sql/new
echo.
echo ========================================
echo Steps:
echo 1. Paste this SQL:
echo.
echo    CREATE POLICY IF NOT EXISTS "Anyone can insert artwork"
echo        ON public.artwork FOR INSERT WITH CHECK (true);
echo.
echo 2. Click "Run"
echo 3. Run: python test_add_record.py
echo ========================================

:end
pause

