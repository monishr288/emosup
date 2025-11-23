@echo off
TITLE EmoSupport - AI Therapy Companion Setup
color 0B

echo.
echo ========================================
echo    EmoSupport - AI Therapy Companion
echo ========================================
echo.
echo Checking setup...
echo.

REM Check if .env file exists
if exist .env (
    echo [OK] Configuration found
    goto START_SERVER
)

echo First time setup...
echo.
echo ========================================
echo     Optional: Groq API Key Setup
echo ========================================
echo.
echo For the BEST AI responses, get a FREE Groq API key:
echo 1. Visit: https://console.groq.com/keys
echo 2. Sign up (FREE, no credit card!)
echo 3. Create API key
echo 4. Paste it below
echo.
echo Or press ENTER to skip (app will use built-in responses)
echo.
set /p GROQ_KEY="Enter your Groq API key (or press ENTER to skip): "

if "%GROQ_KEY%"=="" (
    echo.
    echo [OK] Using built-in AI responses (works offline!)
    echo # EmoSupport Configuration > .env
    echo # App works without this - add Groq key later for better AI >> .env
    echo GROQ_API_KEY= >> .env
) else (
    echo.
    echo [OK] Groq API key saved!
    echo # EmoSupport Configuration > .env
    echo GROQ_API_KEY=%GROQ_KEY% >> .env
)

echo NEXT_PUBLIC_API_BASE_URL=http://localhost:5000 >> .env

echo.
echo ========================================
echo     Installing Dependencies...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.10+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Install Python dependencies
echo Installing Python packages...
pip install -r requirements.txt --quiet

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Node.js not found - skipping frontend build
    echo You can install it later from: https://nodejs.org/
    echo.
    echo The API server will still work!
    goto START_SERVER
)

REM Install Node dependencies and build
if exist package.json (
    echo Installing Node.js packages...
    call npm install --silent
    echo Building frontend...
    call npm run build --silent
)

:START_SERVER
echo.
echo ========================================
echo     Starting EmoSupport Server...
echo ========================================
echo.

REM Kill any existing server
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *api_server*" >nul 2>&1

REM Start API server in background
start "EmoSupport API Server" /MIN python api_server.py

REM Wait for server to start
timeout /t 3 /nobreak >nul

echo [OK] Server started!
echo.
echo ========================================
echo     Opening EmoSupport...
echo ========================================
echo.

REM Try to open the therapy page
start http://localhost:3000/therapy >nul 2>&1
if errorlevel 1 (
    REM If Next.js not running, open API docs
    start http://localhost:5000/api/health
)

echo.
echo EmoSupport is running!
echo.
echo   Web Interface: http://localhost:3000/therapy
echo   API Server:    http://localhost:5000
echo.
echo Keep this window open while using the app.
echo Press Ctrl+C to stop the server.
echo.

REM Keep window open
pause
