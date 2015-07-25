#importing all necessary modules

import cv2
import matplotlib.pyplot as plt    

from utils import *
from darknet import Darknet


# defining path and name of the cfg file which contains descreption of model
cfg_file = 'yolov3.cfg'

# Set path and name of the pre-trained weights file
weight_file = 'yolov3.weights'

# Set the location and name of the COCO object classes file
names = 'coco.names'


# Load the network architecture
model = Darknet(cfg_file)

# Load the pre-trained weights
model.load_weights(weight_file)

# Load the COCO object classes
class_names = load_class_names(names)

nms_thresh = 0.6    # Set the NMS threshold

iou_thresh = 0.4     # Set the IOU threshold

#making list of vehicles as we only need to count no of vehicles
list_of_vehicles = ["car","bus","motorbike","truck","bicycle"]


# method  for preprocessesing the images 
def preprocess(img, visualization=False):
    
    # Set the custom figure size
    plt.rcParams['figure.figsize'] = [24.0, 14.0]
    
    # Resize the image to the input width and height of the first layer of the network.    
    resized_image = cv2.resize(img, (model.width, model.height))
    
    if(visualization):
        plt.subplot(121)
        plt.title('Original Image')
        plt.imshow(img)
        plt.subplot(122)
        plt.title('Resized Image')
        plt.imshow(resized_image)
        plt.show()
    
    return resized_image

def detect_vehicles(img, visualization=False):
    #pre-processing the input 
    resized_image = preprocess(img) 
    boxes = detect_objects(model, resized_image, iou_thresh, nms_thresh)
    
     # making visualization of image with bounding box optional as it makes program slower
    if(visualization):
        plt.rcParams['figure.figsize'] = [24.0, 14.0]
        plot_boxes(img, boxes, class_names, plot_labels = True)
    return get_vehicle_count(boxes,class_names)

def get_vehicle_count(boxes, class_names):
  total_vehicle_count=0 # total vechiles present in the image
  dict_vehicle_count = {} # dictionary with count of each distinct vehicles detected
  
  # examine each detected bounding boxes 
  for i in range(len(boxes)): 
    box = boxes[i] 
    if (len(box) >=7 and class_names): # validation
      class_id = box[6]
      class_name = class_names[class_id]
      if( class_name in list_of_vehicles):
        total_vehicle_count += 1
        dict_vehicle_count[class_name] = dict_vehicle_count.get(class_name,0) + 1
  
  return total_vehicle_count, dict_vehicle_count
  
    
def control_lights(image):
    total_vehicles, each_vehicle = detect_vehicles(image)
    print("Total vehicles in image", total_vehicles)
    print("Each vehicles count in image", each_vehicle)
    if(total_vehicles>=15):
        v_density="High"
    elif(total_vehicles>=5 and total_vehicles<15):
        v_density="Medium"
    else:  
        v_density="Low"
    print(v_density)  
    ser.write(str.encode(v_density)) 
    dic={"High":10, "Medium":8, "Low": 5}
    time.sleep(dic[v_density])
    return total_vehicles, each_vehicle

        

    
    