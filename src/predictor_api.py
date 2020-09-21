#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '11423'
__mtime__ = '2020/5/23'
"""
import os

import numpy as np
import torch.optim.lr_scheduler
from torch.autograd import Variable
from torchvision import transforms

from src.net import AlexNetPlusLatent

model = None
bits = None
imgrecord = []

def load_model():
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)
	global model
	# 48bit
	model = AlexNetPlusLatent(48)
	model.load_state_dict(torch.load('../model/90.42'))


def load_bitdoc():
	"""
	# Load the bits doc
	"""
	global bits
	global imgrecord

	if os.path.exists("../code/bits.npy") and os.path.exists("../code/imgrecord.txt"):
		bits = np.load("../code/bits.npy")
	imgrecord = []
	with open('../code/imgrecord.txt', 'r') as f:
		for line in f:
			# result = line.strip('\n').split(',')
			# imgrecord.append(list(result[0]))
			imgrecord.append(list(line.strip('\n').split(',')))


# Load the bits doc

if os.path.exists("../code/bits.npy") and os.path.exists("../code/imgrecord.txt"):
	bits = np.load("../code/bits.npy")
	imgrecord = []
	with open('../code/imgrecord.txt', 'r') as f:
		for line in f:
			# result = line.strip('\n').split(',')
			# imgrecord.append(list(result[0]))
			imgrecord.append(list(line.strip('\n').split(',')))


def load_model():
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)
	global model
	# 48bit
	model = AlexNetPlusLatent(48)
	model.load_state_dict(torch.load('../model/90.42'))


def binary_output(query, bit_num=48):
	model.eval()
	transform = transforms.Compose(
		[transforms.Resize(227), transforms.ToTensor(),
		 transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))])
	input = transform(query)
	with torch.no_grad():
		input = Variable(input)
	outputs, _ = model(torch.unsqueeze(input, 0))
	return torch.round(outputs.data)


def hammingDis(B, b, num):
	# hammingDists
	hamming = []
	for bitemp in B:
		smstr = np.nonzero(b - bitemp)
		sm = np.shape(smstr[0])[0]
		hamming.append(sm)
	# minNum
	minNum = []
	for i in range(num):
		minind = hamming.index(min(hamming))
		minNum.append(minind)
		hamming[minind] = max(hamming)
	return minNum


def ImageSearch(image, bit_num):
	binary = binary_output(image, bit_num)
	query_bit = binary.numpy()
	minHamming = hammingDis(bits, query_bit, 10)
	predictions = []
	for ind in minHamming:
		img_path = imgrecord[ind][0]
		predictions.append(img_path)
	return {"predictions": predictions}


if __name__ == '__main__':
	import matplotlib.pyplot as plt
	from PIL import Image

	load_model()
	load_bitdoc()

	image_path = './static/images/1.jpg'
	image = Image.open('./static/images/1.jpg').convert('RGB')
	res = ImageSearch(image, bit_num=48)
	res_list = res['predictions']
	plt.figure()
	plt.subplot(3, 5, 3)
	plt.imshow(image)
	plt.xticks([])
	plt.yticks([])
	count = 5
	for i in range(res_list.__len__()):
		count += 1
		img = Image.open(res_list[i])
		plt.subplot(3, 5, count)
		plt.imshow(img)
		plt.xticks([])
		plt.yticks([])
		print(res_list[i])
	plt.show()
