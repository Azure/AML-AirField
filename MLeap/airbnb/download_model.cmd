@echo off

if not exist .\model\airbnb.model.lr.zip goto download
if not exist .\model\airbnb.model.rf.zip goto download

exit /b 0

:download

echo.
echo Downloading Model
echo.

powershell -executionpolicy bypass -File .\download_model.ps1

type legal.notice
echo.
pause
