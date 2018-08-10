set -e

./download_model.sh
./build_scoring_model.sh

echo ''
echo "Creating Azure ML service (it takes a while)"
echo ''
set -x
az ml service create realtime --model-file model -f score.py -d app.py -d ui.html -n mleapairbnb -r spark-py
