@echo off
echo Opening Supabase API Settings...
echo.
start https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api
echo.
echo ========================================
echo STEPS TO FIX:
echo ========================================
echo.
echo 1. On the page that just opened, find:
echo    - "anon" key (public)
echo    - "service_role" key (secret - recommended)
echo.
echo 2. Click "Copy" next to the key you want
echo.
echo 3. Open backend/.env in a text editor
echo.
echo 4. Replace the old key or add:
echo    SUPABASE_ANON_KEY=paste-key-here
echo    SUPABASE_SERVICE_ROLE_KEY=paste-key-here
echo.
echo 5. Save the file
echo.
echo 6. Run: python test_add_record.py
echo.
echo ========================================
pause

