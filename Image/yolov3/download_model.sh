if [ ! -f model/yolov3.weights ]; then
    echo ''
    echo Downloading Yolov3
    echo ''

    # Clone Darknet repo
    git clone https://github.com/pjreddie/darknet
    
    # Download model weights
    wget -nc -P model/ https://pjreddie.com/media/files/yolov3.weights
    
    echo ""
    cat legal.notice
    echo ""
    read -n1 -s -r -p "Press any key to continue . . ."
    echo ""
fi
