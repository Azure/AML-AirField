@echo off

call download_model.cmd || goto :error

echo.
echo Creating Azure ML service (it takes a while)
echo.
echo on
az ml service create realtime --model-file model -f score.py -d app.py -d ui.html -n inceptionv3 -r python -p requirements.txt

@goto :eof

:error
echo Failed with error %errorlevel%
exit /b %errorlevel%
