set -e

SOURCE=${1:-../../local_debugging/*}

cp -n -r $SOURCE ./

sudo apt-get install jq
./download_model.sh

# Setup Conda enviornment
if ! conda env list | grep -q deepmojienv; then
    conda env create -f conda_dependencies.yml
fi

# Activate Conda enviornment
source activate deepmojienv
pip install -I gunicorn json-logging-py flask applicationinsights azure-ml-api-sdk
source deactivate
