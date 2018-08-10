set -e

./download_model.sh

echo ''
echo "Creating Azure ML service (it takes a while)"
echo ''
set -x
az ml service create realtime --model-file model --model-file torchmoji --model-file data -f score.py -d app.py -d ui.html -c conda_dependencies.yml -n deepmoji -r python
