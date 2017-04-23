import numpy as np
import os
import sys

from DataLoader import FER_2013, Data

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
from tflearn.layers.merge_ops import merge
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

class Net:
	
	def __init__(self, data_path, model_path):
		self.data = FER_2013.import_data(data_path)
		self.model_path = model_path

	def build(self):
		''' 	
		Current architecture
		In -> Conv -> Pool -> Conv -> Pool -> Conv -> Dropout -> FC -> FC	
		'''
		self.network = input_data(shape = [None, 48, 48, 1])
		self.network = conv_2d(self.network, 64, 5, activation = 'relu')
		#self.network = local_response_normalization(self.network)
		self.network = max_pool_2d(self.network, 3, strides = 2)
		self.network = conv_2d(self.network, 64, 5, activation = 'relu')
		self.network = max_pool_2d(self.network, 3, strides = 2)
		self.network = conv_2d(self.network, 128, 4, activation = 'relu')
		self.network = dropout(self.network, 0.3)
		self.network = fully_connected(self.network, 3072, activation = 'relu')
		self.network = fully_connected(self.network, 7, activation = 'softmax') # 7 = len(LABELS)
		self.network = regression(self.network,
			optimizer = 'momentum',
			loss = 'categorical_crossentropy')
		self.model = tflearn.DNN(
			self.network,
			checkpoint_path = 'model/',
			max_checkpoints = 1,
			tensorboard_verbose = 2)

	def train(self):
		# Make sure it's built
		self.build()
		
		# Train
		print '>> Training model on training set'
		print len(self.data.X_train), np.asarray(self.data.y_train).shape
		self.model.fit(
			np.asarray(self.data.X_train).reshape(len(self.data.X_train), 48, 48, 1), 
			np.asarray(self.data.y_train).reshape(len(self.data.y_train), 7),
			validation_set = (self.data.X_validate, self.data.y_validate),
			n_epoch = 100,
			batch_size = 30,
			shuffle = True,
			show_metric = True,
			snapshot_step = 200,
			snapshot_epoch = True,
			run_id = 'net net'
		)
		print ">> Training finished"

	def test(self):
		print ">> Testing model on test set"
		correct = 0.0
		for (x, y) in zip(data.X_test, data.y_test):
			if ff(x) is y:
				correct += 1.0
		print ">> " + correct / len(data.x_test) + "% accuracy on test set"

	def ff(self, x):
		if x.shape is not (48,48,1):
			print "!! Cannot feed forward, input img is wrong dimension"
		return self.model.predict(x)

	def save_model(self):
		self.model.save(self.model_path)
		print ">> Model saved to " + self.model_path

	def load_model(self):
		self.model.load(self.model_path)
		print ">> Model loaded from " + self.model_path

def show_help():
	print "Usage: net.py {train | test} <data> <model name>"

if __name__ == "__main__":
	if len(sys.argv) < 4:
		show_help()
		exit()

	dp = sys.argv[2]
	mp = sys.argv[3]
	n = Net(dp, mp)

	if (sys.argv[1] == 'train'):
		n.train()
		n.save_model()

	elif (sys.argv[1] == 'test'):
		n.load_model()
		n.test()

	else:
		show_help()
		exit()
