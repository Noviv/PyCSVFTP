@echo off

:LOOP
cls
python gui.py
echo %errorlevel%
if errorlevel 5 {
	GOTO LOOP
}