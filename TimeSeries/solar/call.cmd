@echo off

if "%1" == "" (set URL=127.0.0.1:9090/score) else (set URL=%1)
if "%2" == "" (set AUTH=@{}) else (set AUTH=@{"Authorization"='"Bearer %2"'})
if "%3" == "" (set IN_FILE=.\sample_input.csv) else (set IN_FILE=%3)

powershell $ProgressPreference = 'SilentlyContinue'; $hdrs = %AUTH%; Invoke-WebRequest -Verbose -Method POST -Headers $hdrs %URL% -InFile %IN_FILE% ^| Select-Object -ExpandProperty RawContent
echo.
