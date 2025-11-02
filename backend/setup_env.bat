@echo off
echo ========================================
echo Setting up backend/.env file
echo ========================================
echo.

cd /d "%~dp0"

if exist .env (
    echo .env file already exists!
    echo.
    choice /C YN /M "Do you want to overwrite it"
    if errorlevel 2 goto :end
    if errorlevel 1 goto :create
) else (
    goto :create
)

:create
echo Creating backend/.env file...
echo.
echo Copy this file and add your Service Role Key:
echo.
echo Go to: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api
echo Find "service_role" key and copy it.
echo.
echo Then edit backend/.env and uncomment the SUPABASE_SERVICE_ROLE_KEY line.
echo.

(
echo # Supabase Configuration
echo SUPABASE_URL=https://zcgjlmdvztxakwubrjyg.supabase.co
echo.
echo # Service Role Key - ADD YOUR KEY HERE (bypasses RLS)
echo # Get it from: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api
echo # SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
echo.
echo # Anon Key (backup, if service role not available)
echo SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjZ2psbWR2enR4YWt3dWJyanlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NTY4MDMsImV4cCI6MjA3NzMzMjgwM30.A97auA0Ts-xSN_DVi0C7HIB0V5H9ZAjUc5zfEAvj5AE
) > .env

echo ✅ Created .env file!
echo.
echo Next steps:
echo 1. Open backend/.env in a text editor
echo 2. Go to Supabase Dashboard: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api
echo 3. Copy your service_role key
echo 4. Paste it in .env (uncomment the SUPABASE_SERVICE_ROLE_KEY line)
echo 5. Save the file
echo 6. Run: python test_add_record.py
echo.

:end
pause

