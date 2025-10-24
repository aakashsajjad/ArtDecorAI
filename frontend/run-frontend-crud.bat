@echo off
echo 🎨 ArtDecorAI - Frontend CRUD Operations
echo ================================================

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 18 or higher
    pause
    exit /b 1
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not available
    pause
    exit /b 1
)

echo ✅ Node.js and npm are available

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo 📦 Installing dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)

REM Start the development server
echo 🚀 Starting Next.js development server...
echo.
echo 📱 Frontend will be available at: http://localhost:3000
echo 🎨 Artwork CRUD Demo: http://localhost:3000/artwork-demo
echo 🔧 Artwork CRUD (with API): http://localhost:3000/artwork-crud
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev
