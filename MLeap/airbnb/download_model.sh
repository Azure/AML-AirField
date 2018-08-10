set -e

if [ ! -f model/airbnb.model.lr.zip ] || [ ! -f model/airbnb.model.rf.zip ]; then
    echo ""
    echo Downloading Model
    echo ""

    wget -nc -P model/ https://github.com/combust/mleap/raw/master/LICENSE
    wget -nc -P model/ https://github.com/combust/mleap/raw/master/mleap-benchmark/src/main/resources/models/airbnb.model.lr.zip
    wget -nc -P model/ https://github.com/combust/mleap/raw/master/mleap-benchmark/src/main/resources/models/airbnb.model.rf.zip

    echo ""
    cat legal.notice
    echo ""
    read -n1 -s -r -p "Press any key to continue . . ."
    echo ""
fi
