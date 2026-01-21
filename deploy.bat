@echo off
REM Multi-Agent Framework Windows Deployment Script

SETLOCAL EnableDelayedExpansion

echo ==========================================
echo Multi-Agent Framework Deployment Script
echo ==========================================
echo.

REM Check if .env exists
if not exist "config\.env" (
    echo [WARNING] .env file not found. Creating from .env.example...
    if exist "config\.env.example" (
        copy "config\.env.example" "config\.env"
        echo [INFO] Please edit config\.env with your actual API keys
        pause
        exit /b 0
    ) else (
        echo [ERROR] .env.example not found
        pause
        exit /b 1
    )
)

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "output\generated_code" mkdir "output\generated_code"
if not exist "output\documentation" mkdir "output\documentation"
if not exist "output\tests" mkdir "output\tests"
if not exist "logs" mkdir "logs"

echo.
echo Select deployment option:
echo 1) Deploy locally (requires Python 3.10+)
echo 2) Run tests
echo 3) Launch Streamlit UI
echo 4) Exit
echo.
set /p option="Enter option (1-4): "

if "%option%"=="1" goto local_deploy
if "%option%"=="2" goto run_tests
if "%option%"=="3" goto launch_ui
if "%option%"=="4" goto exit_script
goto invalid_option

:local_deploy
echo.
echo [INFO] Setting up Python virtual environment...

REM Check if virtual environment exists
if not exist "genaivnv" (
    echo [INFO] Creating virtual environment...
    python -m venv genaivnv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call genaivnv\Scripts\activate.bat

echo [INFO] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [INFO] Starting Streamlit application...
echo ==========================================
echo Application starting at: http://localhost:8501
echo ==========================================
echo.

streamlit run ui\streamlit_app.py
goto end

:run_tests
echo.
echo [INFO] Running tests...

REM Activate virtual environment if it exists
if exist "genaivnv" (
    call genaivnv\Scripts\activate.bat
)

pytest tests\ -v

echo [INFO] Tests completed!
goto end

:launch_ui
echo.
echo [INFO] Launching Streamlit UI...

REM Activate virtual environment if it exists
if exist "genaivnv" (
    call genaivnv\Scripts\activate.bat
)

streamlit run ui\streamlit_app.py
goto end

:invalid_option
echo [ERROR] Invalid option
goto end

:exit_script
echo [INFO] Exiting...
goto end

:end
echo.
pause
