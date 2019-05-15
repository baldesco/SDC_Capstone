if [ ! -d "../yolo_model" ]; then
    echo "Creating folder directory"
    mkdir ../yolo_model
fi

cd ../yolo_model

if [ ! -f "yolov3.weights" ]; then
    echo "Downloading weights file"
    wget https://pjreddie.com/media/files/yolov3.weights
fi

if [ ! -f "yolov3.cfg" ]; then
    echo "Downloading config file"
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
fi
