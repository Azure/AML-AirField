SOURCE=${1:-../../local_debugging/*}

cp -n -r $SOURCE ./

sudo apt-get install python3.6 python3-pip gunicorn3 jq

pip3 install json-logging-py flask applicationinsights azure-ml-api-sdk

./download_model.sh

