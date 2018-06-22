if [ ! -f model/yolov3.weights ]; then
    # Clone Darknet repo
    git clone https://github.com/pjreddie/darknet
    
    # Download model weights
    wget -nc -P model/ https://pjreddie.com/media/files/yolov3.weights
    
    echo ''
    echo 'You have downloaded Darknet and YOLO v3. Darknet and YOLO v3 is licensed separately.'
    echo 'See the LICENSE files in the darknet folder for license information. By using Darknet and YOLO v3, you agree to those licenses.'
    echo ''
fi
