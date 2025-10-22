@echo off
title D&D Game Launcher
cd dnd_game

REM Check if virtual environment is already activated
if defined VIRTUAL_ENV (
    echo Virtual environment already activate
    echo.
) else (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo Virtual environment activated!
    echo.
)

echo Starting D&D Game...
echo.
python main.py

echo.
echo Game ended.
pause