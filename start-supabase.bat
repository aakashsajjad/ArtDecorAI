@echo off
REM Start Supabase locally using Docker
echo Starting Supabase local development environment...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running. Please start Docker Desktop.
    exit /b 1
)

REM Download and start Supabase using the official method
echo Installing Supabase CLI prerequisites...
echo Note: If Supabase CLI installation fails due to Node version, we'll use Docker directly.

REM Try to start PostgreSQL container first as a fallback
echo Starting PostgreSQL container...
docker run --name supabase-db-artdecorai ^
    -e POSTGRES_PASSWORD=postgres ^
    -e POSTGRES_USER=postgres ^
    -e POSTGRES_DB=postgres ^
    -p 54322:5432 ^
    -d postgres:15-alpine

if %errorlevel% neq 0 (
    echo ERROR: Failed to start PostgreSQL container
    echo Trying to remove existing container and retry...
    docker rm -f supabase-db-artdecorai 2>nul
    docker run --name supabase-db-artdecorai ^
        -e POSTGRES_PASSWORD=postgres ^
        -e POSTGRES_USER=postgres ^
        -e POSTGRES_DB=postgres ^
        -p 54322:5432 ^
        -d postgres:15-alpine
)

echo.
echo Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak >nul

echo.
echo ============================================================
echo PostgreSQL is starting on port 54322
echo Note: Full Supabase stack requires Supabase CLI or cloud instance
echo For now, PostgreSQL container is running but API gateway is not available
echo ============================================================
echo.
echo Next steps:
echo 1. Apply database schema: Run supabase/migrations/20240101000000_initial_schema.sql
echo 2. Or use a cloud Supabase instance and update backend/.env with credentials
echo.
pause


