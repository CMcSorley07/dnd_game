@echo off
title Activating Virtual environment
cd dnd_game
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.
echo Virtual environment activated!
echo You can now run: python main.py
echo.
cmd /k