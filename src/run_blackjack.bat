@echo off
cd /d "%~dp0"

echo Installing required packages...
py -m pip install customtkinter >nul 2>&1

echo Starting Blackjack GUI...
echo.

py blackjack_gui.py

pause