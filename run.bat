@echo off
REM Quick launcher for Multi-Agent Framework Streamlit UI

echo ==========================================
echo Multi-Agent Framework - Quick Launcher
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "genaivnv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run deploy.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call genaivnv\Scripts\activate.bat

REM Check if .env file exists
if not exist "config\.env" (
    echo [WARNING] Configuration file not found!
    echo.
    echo Creating config\.env from template...
    copy config\.env.example config\.env
    echo.
    echo IMPORTANT: Please edit config\.env and add your OpenAI API key
    echo Then run this script again.
    echo.
    pause
    exit /b 0
)

REM Launch Streamlit
echo Starting Streamlit application...
echo.
echo ==========================================
echo Application will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

streamlit run ui\streamlit_app.py

pause
