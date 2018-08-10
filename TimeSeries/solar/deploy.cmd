@echo off

if not exist legal.notice.shown (
    echo.
    type legal.notice
    echo.
    pause
    copy nul legal.notice.shown >nul
)

echo.
echo Creating Azure ML service (it takes a while)
echo.
echo on
az ml service create realtime --model-file model -f score.py -d app.py -d ui.html -n solar -r python -p requirements.txt
