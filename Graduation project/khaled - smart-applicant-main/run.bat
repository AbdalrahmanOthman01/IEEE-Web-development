@echo off
chcp 65001 > nul
title Smart Applicant - AI Resume Matcher (مشروع التخرج)

echo =====================================================================
echo          Smart Applicant - AI Resume & Job Matcher
echo                  مشروع التخرج - Graduation Project
echo =====================================================================
echo.

cd /d "%~dp0"

:: Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    set "PY_BIN=.venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_BIN=python"
    ) else (
        echo [ERROR] Python not detected. Please make sure Python or the virtual environment is set up.
        pause
        exit /b 1
    )
)

echo [*] Starting Smart Applicant Web Server...
echo [*] Access the dashboard at: http://127.0.0.1:5000
echo.

:: Open default browser after 2 seconds
start "" timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000

"%PY_BIN%" app.py

pause
