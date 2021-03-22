import cv2  # 4.1.0
import numpy as np  # 1.16.4
import os
import argparse
import sys
import glob
import importlib.util
from tflite_runtime.interpreter import Interpreter
from collections import Counter


class DetectObject():
    def __init__(self):
        print("init")
        # self.MODEL_NAME = "D:\\TP_PROGS\\Projects\\TeProjSahara\\model_objDetec\\modelStart"
        self.MODEL_NAME = "D:\\TP_PROGS\\Projects\\TeProjSahara\\model_objDetec\\finalObjDet\\new\\new"
        # self.GRAPH_NAME = "detect.tflite"
        self.GRAPH_NAME = "ssd_mobilenet_v1_1_metadata_1.tflite"
        # self.LABELMAP_NAME = "labelmap.txt"
        self.LABELMAP_NAME = "label.txt"
        self.min_conf_threshold = 0.5
        # use_TPU = args.edgetpu
        self.listOfObjDetec = []

        # Path to label map file
        self.PATH_TO_LABELS = os.path.join(self.MODEL_NAME, self.LABELMAP_NAME)
        print(self.PATH_TO_LABELS)
        # Path to .tflite file, which contains the model that is used for object detection
        self.PATH_TO_CKPT = os.path.join(self.MODEL_NAME, self.GRAPH_NAME)

        # Load the label map
        with open(self.PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is '???', which has to be removed.
        if self.labels[0] == '???':
            del (self.labels[0])

        # Load the Tensorflow Lite model.
        self.interpreter = Interpreter(model_path=self.PATH_TO_CKPT)
        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

    def objDetect(self, img):
        cv2.imshow('Object detector', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # clearing list of prev objs
        self.listOfObjDetec.clear()
        imH, imW, _ = img.shape
        image_resized = cv2.resize(img, (self.width, self.height))
        input_data = np.expand_dims(image_resized, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        # results
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]  # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # Class index of detected objects
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]  # Confidence of detected objects
        for i in range(len(scores)):
            if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0)):
                # getting label/class
                object_name = self.labels[int(classes[i])]  # Look up object name from "labels" array using class index

                print("detected:", object_name, ":", int(scores[i] * 100))
                self.listOfObjDetec.append(object_name)

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
        if self.listOfObjDetec:
            print(self.listOfObjDetec)
            objDict = dict(Counter(self.listOfObjDetec))
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
