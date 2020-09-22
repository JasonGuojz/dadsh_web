#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '11423'
__mtime__ = '2020/5/23'
"""
import io
import os

import flask
import requests
import yaml
import numpy as np
import torch.optim.lr_scheduler
from PIL import Image
from flask import request, jsonify
from torch.autograd import Variable
from torchvision import transforms
from src.net import AlexNetPlusLatent

with open("./src/config.yaml", 'r') as stream:
	APP_CONFIG = yaml.full_load(stream)

app = flask.Flask(__name__)
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
	model.load_state_dict(torch.load('./model/90.42'))


def load_bitdoc():
	"""
	# Load the bits doc
	"""
	global bits
	global imgrecord

	if os.path.exists("./code/bits.npy") and os.path.exists("./code/imgrecord.txt"):
		bits = np.load("./code/bits.npy")
	imgrecord = []
	with open('./code/imgrecord.txt', 'r') as f:
		for line in f:
			# result = line.strip('\n').split(',')
			# imgrecord.append(list(result[0]))
			imgrecord.append(list(line.strip('\n').split(',')))


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


@app.after_request
def add_header(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"

	response.cache_control.max_age = 0
	return response


@app.route('/<path:path>')
def static_file(path):
	if ".js" in path or ".css" in path:
		return app.send_static_file(path)
	else:
		return app.send_static_file('index.html')


@app.route('/config')
def config():
	return flask.jsonify(APP_CONFIG)


# 访问首页时的调用函数
@app.route('/')
def index_page():  # flask库要求'web_page.html'必须在templates文件夹下
	return app.send_static_file('index.html')


# 获取用户输入
@app.route('/predict', methods=['POST', 'GET'])
def upload_file():
	if flask.request.method == 'GET':
		url = flask.request.args.get("url")
		response = requests.get(url, verify=False)
		img = Image.open(io.BytesIO(response.content))
	else:
		img_bytes = request.files['file'].read()
		img = Image.open(io.BytesIO(img_bytes))
	res = ImageSearch(img, bit_num=48)
	return jsonify(res)


def before_request():
	app.jinja_env.cache = {}


if __name__ == '__main__':
	app.debug = False
	# 设置开启web服务后，如果更新html文件，可以使更新立即生效
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	load_model()
	load_bitdoc()
	app.run()  # use your local IPv4 address to replace 0.0.0.0
