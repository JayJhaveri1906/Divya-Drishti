from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2  # 4.1.0
import numpy as np  # 1.16.4
from DetectObject import DetectObject
import time
from matplotlib import cm

import argparse
import time

# import numpy as np
from PIL import Image
# import tensorflow as tf # TF2
import tflite_runtime.interpreter as tflite

class CurrencyRecognizer():

	def __init__(self):
		print("init")

	def load_labels(filename):
		with open(filename, 'r') as f:
			return [line.strip() for line in f.readlines()]

	def readCurr(self, imge):
		# loaded model
		model_file = 'D:\\TP_PROGS\\Projects\\TeProjSahara\\model_currencyDetec\\model\\model-export_icn_tflite-Currency_detector_20210125103903-2021-01-25T08_23_23.101746Z_model.tflite'
		interpreter = tflite.Interpreter(
			model_path=model_file, num_threads=None)
		interpreter.allocate_tensors()

		# loading labels
		label_file = 'D:\\TP_PROGS\\Projects\\TeProjSahara\\model_currencyDetec\\model\\model-export_icn_tflite-Currency_detector_20210125103903-2021-01-25T08_23_23.101746Z_dict.txt'
		# labels = load_labels(label_file)
		with open(label_file, 'r') as f:
			labels = [line.strip() for line in f.readlines()]

		### getting outputs:
		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()

		# check the type of the input tensor
		floating_model = input_details[0]['dtype'] == np.float32
		print("floating model: ", floating_model)

		# NxHxWxC, H:1, W:2
		height = input_details[0]['shape'][1]
		width = input_details[0]['shape'][2]
		# img = Image.open(img).resize((width, height))
		# print(imge)
		# print(type(imge))
		img = Image.fromarray(imge).resize((width, height))
		# print(type(img))
		# img.show()
		# img = imge.resize((width, height))

		# add N dim
		input_data = np.expand_dims(img, axis=0)
		# print(input_data)
		# input_data = input_data[:, [0, 1, 2]]

		if floating_model:
			input_data = (np.float32(input_data) - 127.5) / 127.5

		interpreter.set_tensor(input_details[0]['index'], input_data)

		# start_time = time.time()
		interpreter.invoke()
		# stop_time = time.time()

		output_data = interpreter.get_tensor(output_details[0]['index'])
		results = np.squeeze(output_data)

		top_k = results.argsort()[-5:][
				::-1]  # sorts, then stores the index of the sorted array in the new var in asc order.
		# labels = load_labels(args.label_file)
		print(results, "\n", results.argsort(), "\n top:", top_k, "\n", labels)
		# for i in top_k:
		# 	if floating_model:
		# 		print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
		# 	else:
		# 		print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))

		ans = top_k[0]
		probability = results[ans]/255.0
		labelOfAns = labels[ans]
		print(probability, labelOfAns)
		# print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))
		print("identified successfully")
		# img.show()
		if probability >= 0.85:
			if labelOfAns == "200":
				return "Successfully detected a 200 rupee note.", 200
			elif labelOfAns == "2000":
				return "Successfully detected a 2000 rupee note.", 2000
			elif labelOfAns == "500":
				return "Successfully detected a 500 rupee note.", 500
			elif labelOfAns == "100-old" or labelOfAns == "100-new":
				return "Successfully detected a 100 rupee note.", 100
			elif labelOfAns == "50-old" or labelOfAns == "50-new":
				return "Successfully detected a 50 rupee note.", 50
			elif labelOfAns == "20-old" or labelOfAns == "20-new":
				return "Successfully detected a 20 rupee note.", 20
			elif labelOfAns == "10-old" or labelOfAns == "10-new":
				return "Successfully detected a 10 rupee note.", 10
			else:
				return "error occured", 0
		else:
			return "Couldn't find a note, rescan", 0
		# return "identified successfully"



	if __name__ == '__main__':
		parser = argparse.ArgumentParser()
		parser.add_argument(
			'-i',
			'--image',
			default='D:\\TP_PROGS\\Projects\\TeProjSahara\\samplePhotos\\20.jpeg',
			help='image to be classified')
		parser.add_argument(
			'-m',
			'--model_file',
			default='D:\\TP_PROGS\\Projects\\TeProjSahara\\model_currencyDetec\\model\\model-export_icn_tflite-Currency_detector_20210125103903-2021-01-25T08_23_23.101746Z_model.tflite',
			help='.tflite model to be executed')
		parser.add_argument(
			'-l',
			'--label_file',
			default='D:\\TP_PROGS\\Projects\\TeProjSahara\\model_currencyDetec\\model\\model-export_icn_tflite-Currency_detector_20210125103903-2021-01-25T08_23_23.101746Z_dict.txt',
			help='name of file containing labels')
		parser.add_argument(
			'--input_mean',
			default=127.5, type=float,
			help='input_mean')
		parser.add_argument(
			'--input_std',
			default=127.5, type=float,
			help='input standard deviation')
		parser.add_argument(
			'--num_threads', default=None, type=int, help='number of threads')
		args = parser.parse_args()

		interpreter = tflite.Interpreter(
			model_path=args.model_file, num_threads=args.num_threads)
		interpreter.allocate_tensors()

		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()

		# check the type of the input tensor
		floating_model = input_details[0]['dtype'] == np.float32
		print("floating model: ", floating_model)

		# NxHxWxC, H:1, W:2
		height = input_details[0]['shape'][1]
		width = input_details[0]['shape'][2]
		img = Image.open(args.image).resize((width, height))

		# add N dim
		input_data = np.expand_dims(img, axis=0)

		if floating_model:
			input_data = (np.float32(input_data) - args.input_mean) / args.input_std

		interpreter.set_tensor(input_details[0]['index'], input_data)

		start_time = time.time()
		interpreter.invoke()
		stop_time = time.time()

		output_data = interpreter.get_tensor(output_details[0]['index'])
		results = np.squeeze(output_data)

		top_k = results.argsort()[-5:][
				::-1]  # sorts, then stores the index of the sorted array in the new var in asc order.
		labels = load_labels(args.label_file)
		print(results, "\n", results.argsort(), "\n top:", top_k, "\n", labels)
		for i in top_k:
			if floating_model:
				print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
			else:
				print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))

		print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))


