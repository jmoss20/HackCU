import pandas as pd
import numpy as np

import cv2
from PIL import Image

LABELS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']

def one_hot(i):
	r = np.zeros(len(LABELS))
	r[i] = 1
	return r

def to_img(x):
	img = np.fromstring(str(x), dtype=np.uint8, sep=' ').reshape((48,48))
	img = Image.fromarray(img).convert('RGB')
	img = np.array(img)[:,:,::-1].copy()
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Probably should do the same thing to these we do to ours...
	return img

class Data:
	def __init__(self, X, y):
		self.X = X
		self.y = y
		self.split()
	
	def split(self):
		D = zip(self.X, self.y)
		np.random.shuffle(D)
		l = len(D)
		D_train, D_validate, D_test = D[:int(l/3)], D[int(l/3):int(l/3 + l/3)], D[int(l/3) + int(l/3):]
		self.X_train, self.y_train = zip(*D_train)
		self.X_validate, self.y_validate = zip(*D_validate)
		self.X_test, self.y_test = zip(*D_test)
		
		self.X_train = np.asarray(self.data.X_train).reshape(len(self.data.X_train), 48, 48, 1)
		self.X_validate = np.asarray(self.data.X_validate).reshape(len(self.data.X_validate), 48, 48, 1)
		self.X_test = np.asarray(self.data.X_test).reshape(len(self.data.X_test), 48, 48, 1)
		self.y_train = np.asarray(self.data.y_train).reshape(len(self.data.y_train), 7)
		self.y_tune = np.asarray(self.data.y_tune).reshape(len(self.data.y_tune), 7)
		self.y_test = np.asarray(self.data.y_test).reshape(len(self.data.y_test), 7)

class FER_2013:
	@staticmethod
	def import_data(data_path):
		print ">> Importing data"
		data = pd.read_csv(data_path)
		X = []
		y = []
		for i, c in data.iterrows():
			label = one_hot(c['emotion'])
			x = to_img(c['pixels'])
			if x is not None:
				X.append([x])
				y.append(label)
			else:
				print "!! Malformed data item, attempting to continue"
		return Data(X, y)
