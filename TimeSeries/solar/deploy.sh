set -e

if [ ! -f legal.notice.shown  ]; then
    echo ""
    cat legal.notice
    echo ""
    read -n1 -s -r -p "Press any key to continue . . ."
    echo ""
    touch legal.notice.shown
fi

echo ''
echo "Creating Azure ML service (it takes a while)"
echo ''
set -x
az ml service create realtime --model-file model -f score.py -d app.py -d ui.html -n solar -r python -p requirements.txt
