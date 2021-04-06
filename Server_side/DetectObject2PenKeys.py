import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
from collections import Counter
# Define and parse input arguments

def detectPenKey(img):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
    #                     default='models\\model_objDetec\\penKeyModel')
    # parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
    #                     default='model-9020516539576614912_tflite_2021-04-01T07_44_31.691148Z_model.tflite')
    # parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
    #                     default='labels.txt')
    # parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
    #                     default=0.5)
    # parser.add_argument('--image', help='Name of the single image to perform detection on. To run detection on multiple images, use --imagedir',
    #                     default=None)
    # parser.add_argument('--imagedir', help='Name of the folder containing images to perform detection on. Folder must contain only images.',
    #                     default=None)
    # parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
    #                     action='store_true')
    # 
    # args = parser.parse_args()
    listOfObjDetec = []
    MODEL_NAME = "models\\model_objDetec\\penKeyModel"
    GRAPH_NAME = "model-9020516539576614912_tflite_2021-04-01T07_44_31.691148Z_model.tflite"
    LABELMAP_NAME = "labels.txt"
    min_conf_threshold = float(0.5)
    use_TPU = False

    # # Parse input image name and directory.
    # IM_NAME = args.image
    # IM_DIR = args.imagedir
    # 
    # # If both an image AND a folder are specified, throw an error
    # if (IM_NAME and IM_DIR):
    #     print('Error! Please only use the --image argument or the --imagedir argument, not both. Issue "python TFLite_detection_image.py -h" for help.')
    #     sys.exit()
    # 
    # # If neither an image or a folder are specified, default to using 'test1.jpg' for image name
    # if (not IM_NAME and not IM_DIR):
    #     IM_NAME = 'keys11.jpg'
    # 
    # Import TensorFlow libraries
    # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
    # If using Coral Edge TPU, import the load_delegate library
    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter
        if use_TPU:
            from tflite_runtime.interpreter import load_delegate
    else:
        from tensorflow.lite.python.interpreter import Interpreter
        if use_TPU:
            from tensorflow.lite.python.interpreter import load_delegate

    # If using Edge TPU, assign filename for Edge TPU model
    if use_TPU:
        # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
        if (GRAPH_NAME == 'detect.tflite'):
            GRAPH_NAME = 'edgetpu.tflite'


    # Get path to current working directory
    CWD_PATH = os.getcwd()

    # Define path to images and grab all image filenames
    # if IM_DIR:
    #     PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_DIR)
    #     images = glob.glob(PATH_TO_IMAGES + '/*')
    # 
    # elif IM_NAME:
    #     PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_NAME)
    #     images = glob.glob(PATH_TO_IMAGES)

    # Path to .tflite file, which contains the model that is used for object detection
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

    # Load the label map
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Have to do a weird fix for label map if using the COCO "starter model" from
    # https://www.tensorflow.org/lite/models/object_detection/overview
    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    # Load the Tensorflow Lite model.
    # If using Edge TPU, use special load_delegate argument
    if use_TPU:
        interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                  experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        print(PATH_TO_CKPT)
    else:
        interpreter = Interpreter(model_path=PATH_TO_CKPT)

    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Loop over every image and perform detection
    # for image_path in images:

        # Load image and resize to expected shape [1xHxWx3]
    image = img
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        print("hello")
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
    #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
            # getting label/class
            object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index

            print("detected:", object_name, ":", int(scores[i] * 100))
            listOfObjDetec.append(object_name)

            # debug
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))

            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

            # Draw label
            # object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class
            label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
            cv2.rectangle(img, (xmin, label_ymin - labelSize[1] - 10),
                          (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255),
                          cv2.FILLED)  # Draw white box to put label text in
            cv2.putText(img, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                        2)  # Draw label text
    if listOfObjDetec:
        print(listOfObjDetec)
        objDict = dict(Counter(listOfObjDetec))
        print(objDict)
        strg = ""
        for i in objDict:
            print(i)
            strg += "Detected " + str(objDict[i]) + " " + i + "\n"
            print(strg)
            # All the results have been drawn on the image, now display the image
        cv2.imshow('Object detector', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Press any key to continue to next image, or press 'q' to quit
        return strg
    else:
        return "No Objects Detected"
    # Press any key to continue to next image, or press 'q' to quit
    # if cv2.waitKey(0) == ord('q'):
    #     break

    # Clean up
