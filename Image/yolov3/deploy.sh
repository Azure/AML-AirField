echo ''
echo Downloading Yolov3
echo ''
./download_model.sh

echo ''
echo Building Model
echo ''
./build_model.sh

echo ''
echo Creating Azure ML service (it takes a while)
echo ''

az ml service create realtime --model-file model --model-file data -f score.py -d app.py -d ui.html -n yolov3 -r python
