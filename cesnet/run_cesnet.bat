@echo off
setlocal enabledelayedexpansion

rem Check if Selenium is installed
python -c "import selenium" 2>nul
if %errorlevel% neq 0 (
    echo Selenium not installed. Installing...
    pip install selenium
    if %errorlevel% neq 0 (
        echo Failed to install Selenium. Exiting...
        exit /b 1
    )
    echo Selenium installed successfully.
)

REM Run the Python script
python run_cesnet.py
