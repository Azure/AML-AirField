if [ ! -f model/libdarknet.so ]; then
    echo ''
    echo Building Model
    echo ''

    sed -i '/^OPENMP=0$/c OPENMP=1' ./darknet/Makefile
    pushd ./darknet ; make ; popd

    # Copy model related files over to the model directory
    mkdir -p data/labels
    cp -a ./darknet/data/labels/. ./data/labels/
    cp ./darknet/data/coco.names ./data/
    cp ./darknet/data/coco9k.map ./data/
    cp ./darknet/libdarknet.so ./model/
    cp ./darknet/cfg/coco.data ./model/
    cp ./darknet/cfg/yolov3.cfg ./model/
    cp ./darknet/LICENSE* ./model/
fi
