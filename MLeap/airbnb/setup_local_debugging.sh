set -e

SOURCE=${1:-../../local_debugging/*}

cp -n -r $SOURCE ./

sudo apt-get install python3.6 python3-pip gunicorn3 jq

pip3 install json-logging-py flask applicationinsights azure-ml-api-sdk pyspark

if ! grep -q "mleap-airbnb-assembly-0.0.1.jar" "./main.py"; then
    echo "$(cat append_to_main.txt main.py)" > main.py
fi

./download_model.sh
./build_scoring_model.sh



