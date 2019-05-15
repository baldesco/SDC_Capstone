# Import libraries
from styx_msgs.msg import TrafficLight
import numpy as np
import cv2
import os

class TLClassifier(object):
    # This function and the next one are adapted from the code given in https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
    def __init__(self, confidence, yolo_path):
        self.confidence = confidence

        # Path to YOLO's weights and config files
        self.weigthsPath = os.path.sep.join([yolo_path,'yolov3.weights'])
        self.configPath = os.path.sep.join([yolo_path,'yolov3.cfg'])

        # Load YOLO V3 model trained on COCO dataset (80 classes)
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weigthsPath)

        # Determine the out layers that we need from the model
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        
        # This parameter is used in the classification of the traffic lights
        self.intensity_threshold = 40

    def locate_traffic_light(self,image):
        """
        Locates traffic lights in the image, and returns the cuted images of these traffic lights.
        """

        # Ensure that the image is a numpy array
        img = np.asarray(image)
        # Get the image dimensions
        (H, W) = image.shape[:2] # height and width

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416,416), swapRB=True, crop=False)
        self.net.setInput(blob)

        layerOutputs = self.net.forward(self.ln)

        # Initialize a list to store the images contained in the bounding boxes (traffic lights)
        boxes = []
        
        # Loop over the layers detected by the YOLO model
        for output in layerOutputs:
            # Loop through the detections
            for detection in output:
                # Get the predicted class and probability
                scores = detection[5:]
                obj_class = np.argmax(scores)
                confidence = scores[obj_class]
                
                # Proceed if the predicted class is traffic light (9) and its probability is greater than the coinfidence parameter
                if confidence >= self.confidence and obj_class == 9:
                    # scale the bounding box coordinates back relative to the
        			# size of the image, keeping in mind that YOLO actually
        			# returns the center (x, y)-coordinates of the bounding
        			# box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype('int')
                    # use the center (x, y)-coordinates to derive the top and
        			# and left corner of the bounding box
                    x = int(centerX - (width/2))
                    y = int(centerY - (height/2))
                    # Get only the traffic lights
                    h = int(height)
                    w = int(width)
                    img = image[y:y+h, x:x+w]
                    # if the image has values, append it to the boxes list
                    if img.size > 0:
                        boxes.append(img)

        return boxes

    # This function and the next one are taken/adapted from https://qtmbits.com/traffic-light-classifier-using-python-and-opencv/
    def slice_image(self, image):
        """
        Takes in the image of a traffic light and slices it vertically in 3 equally sized images
        """
        img = image.copy()
        slice = img.shape[0]//3
        
        upper = img[0:slice, :, :]
        middle = img[slice:2*slice, :, :]
        lower = img[2*slice:, :, :]
        return upper, middle, lower
    
    def get_avg_v(self, bgr_image):
        """
        Determines the color intensity of a sliced image
        """
        hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        # calculate image area
        area = hsv.shape[0] * hsv.shape[1]
        # Add up all the pixel values in the V channel
        sum_v = np.sum(hsv[:, :, 2])
        avg_v = sum_v / area
     
        return avg_v
    
    def get_classification(self,image):
        """Determines the color of the traffic light in the image
        Args:
            image (cv::Mat): image containing the traffic light
        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)
        """
        boxes = self.locate_traffic_light(image)
        if len(boxes) == 0:
            return TrafficLight.UNKNOWN
        
        # Loop through all the found traffic lights
        for img in boxes:
            slices = self.slice_image(img)
            if len(slices) == 3:
                intensities = [self.get_avg_v(i) for i in slices]
                # If at least 1 red traffic light is found, return red.
                if (np.argmax(intensities) == 0) and (intensities[0] > self.intensity_threshold):
                    return TrafficLight.RED
        
        return TrafficLight.UNKNOWN
            
        
