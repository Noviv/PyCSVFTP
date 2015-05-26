@echo off

:LOOP
cls
python gui.py
if errorlevel 5 GOTO LOOP