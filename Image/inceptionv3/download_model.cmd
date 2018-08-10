@echo off

if not exist model\classify_image_graph_def.pb (
    echo.
    echo Downloading Model
    echo.

    powershell -executionpolicy bypass -File .\download_model.ps1

    type legal.notice
    echo.
    pause
) else (
   exit /b 0
)
