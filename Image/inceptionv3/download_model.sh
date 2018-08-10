if [ ! -f model/classify_image_graph_def.pb ]; then
    echo ""
    echo Downloading Model
    echo ""

    wget -nc -P model/ http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz
    tar xvzf model/inception-2015-12-05.tgz -C model/
    rm model/cropped_panda.jpg
    rm model/inception-2015-12-05.tgz
    
    echo ""
    cat legal.notice
    echo ""
    read -n1 -s -r -p "Press any key to continue . . ."
    echo ""
fi
