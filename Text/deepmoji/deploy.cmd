@echo off

call download_model || goto :error

echo.
echo Creating Azure ML service (it takes a while)
echo.
echo on
az ml service create realtime --model-file model --model-file torchmoji --model-file data -f score.py -d app.py -d ui.html -c conda_dependencies.yml -n deepmoji -r python

@goto :eof

:error
echo Failed with error %errorlevel%
exit /b %errorlevel%
