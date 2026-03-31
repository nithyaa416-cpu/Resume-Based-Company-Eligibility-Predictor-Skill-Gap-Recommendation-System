@echo off
echo ========================================
echo   AI Resume Analyzer - Frontend Setup
echo ========================================
echo.

echo Installing dependencies...
call npm install

if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install dependencies
    echo Please check your Node.js installation
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.
echo Starting development server...
echo.
echo 🚀 Frontend will be available at: http://localhost:3000
echo 🔗 Make sure your backend is running at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm start