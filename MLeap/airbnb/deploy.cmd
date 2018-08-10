@echo off

call download_model || goto :error
call build_scoring_model || goto :error

echo.
echo Creating Azure ML service (it takes a while)
echo.
echo on
az ml service create realtime --model-file model -f score.py -d app.py -d ui.html -n mleapairbnb -r spark-py

@goto :eof

:error
echo Failed with error %errorlevel%
exit /b %errorlevel%
