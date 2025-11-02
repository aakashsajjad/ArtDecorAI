@echo off
REM Start Supabase locally - Complete setup script
echo ============================================================
echo Starting Supabase Local Development Environment
echo ============================================================
echo.

REM Check if Docker is running
echo [1/5] Checking Docker...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo ✓ Docker is running
echo.

REM Check Node.js version
echo [2/5] Checking Node.js version...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo Current Node.js version: %NODE_VERSION%
echo.

REM Check if Node.js version is 18+
echo [3/5] Verifying Node.js version...
node -e "process.exit(parseInt(process.version.slice(1)) >= 18 ? 0 : 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Node.js version is below 18!
    echo Supabase CLI requires Node.js 18 or higher.
    echo.
    echo Options:
    echo 1. Upgrade Node.js from https://nodejs.org/
    echo 2. Use nvm to switch to Node 18+
    echo 3. Use cloud Supabase instead (recommended)
    echo.
    pause
    exit /b 1
)
echo ✓ Node.js version is compatible
echo.

REM Check if Supabase CLI is installed
echo [4/5] Checking Supabase CLI...
supabase --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Supabase CLI not found. Installing...
    echo This may take a few minutes...
    npm install -g supabase
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Supabase CLI
        echo Please try manually: npm install -g supabase
        pause
        exit /b 1
    )
    echo ✓ Supabase CLI installed
) else (
    for /f "tokens=*" %%i in ('supabase --version') do set SUPABASE_VERSION=%%i
    echo ✓ Supabase CLI is installed: %SUPABASE_VERSION%
)
echo.

REM Navigate to project root
echo [5/5] Starting Supabase...
cd /d "%~dp0"
echo Current directory: %CD%
echo.

REM Check if supabase folder exists
if not exist "supabase" (
    echo WARNING: supabase folder not found
    echo This might be okay if you're starting fresh
)

REM Start Supabase
echo Starting Supabase services...
echo This will download Docker images on first run (may take a few minutes)
echo.
supabase start

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo ✓ Supabase started successfully!
    echo ============================================================
    echo.
    echo Access your services:
    echo   - API URL: http://localhost:54321
    echo   - Studio: http://localhost:54323
    echo   - Database: localhost:54322
    echo.
    echo Now you can run:
    echo   cd backend
    echo   python examples\artwork_examples.py
    echo.
) else (
    echo.
    echo ============================================================
    echo ERROR: Failed to start Supabase
    echo ============================================================
    echo.
    echo Troubleshooting:
    echo 1. Check Docker Desktop is running
    echo 2. Check ports 54321-54324 are not in use
    echo 3. Try: supabase stop (then retry)
    echo 4. Check: supabase status
    echo.
)

pause





