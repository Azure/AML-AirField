set -e

if [ ! -f model/mleap-airbnb-assembly-0.0.1.jar ]; then
    echo ''
    echo Building Model
    echo ''

    pushd ./scoringmodel
    sbt clean
    sbt assembly
    popd

    mkdir -p model
    cp ./scoringmodel/mleap-airbnb-assembly-0.0.1.jar ./model/
fi
