@echo off

if not exist .\model\mleap-airbnb-assembly-0.0.1.jar (
    echo.
    echo Building Model
    echo.

    pushd .\scoringmodel
    call sbt clean
    call sbt assembly
    popd

    if not exist .\model\ mkdir model
    copy .\scoringmodel\mleap-airbnb-assembly-0.0.1.jar .\model\
)
