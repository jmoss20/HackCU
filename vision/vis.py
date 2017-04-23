import cv2
import numpy as np
from net import *
import sys
import logging

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

from socketIO_client import SocketIO, LoggingNamespace

from DataLoader import LABELS

CASCADE_PATH = "data/haarcascade_frontalface_default.xml"

class Cam:
	def __init__(self, 
			flip=True,
			cam_id=0,
			out_dims=(48,48), 
			grayscale=True,
			margin=(15,100)):
		self.flip = flip
		self.out_dims = out_dims
		self.grayscale = grayscale
		self.cam_id = cam_id
		self.c = cv2.VideoCapture(self.cam_id)
		self.cascade = cv2.CascadeClassifier(CASCADE_PATH)
		self.margin = margin

	def read_raw(self):
		ret_val, img = self.c.read()
		return img

	def read_adjusted(self):
		img = self.read_raw()

		# Find a face
		rect = self.cascade.detectMultiScale(img, 1.3, 5)
		if len(rect) == 0:
			img = np.zeros((48,48,1))
			return img
		else:
			# Voodoo magic
			rect[:,2:] += rect[:,:2]

			# Cut out a face
			''' diagnostic
			painted = img.copy()
			for x1, y1, x2, y2 in rect:
				cv2.rectangle(painted, (x1, y1), (x2, y2), (255,0,0), 2)
			cv2.imshow('raw', painted)
			'''

			# pick biggest face
			big_face = rect[0]
			for face in rect:
				if (face[2] * face[3]) > (big_face[2] * big_face[3]):
					big_face = face
	
			img = img[big_face[1]-self.margin[1]:big_face[3]+self.margin[1], 
					big_face[0]-self.margin[0]:big_face[2]+self.margin[0]]

		# Flip
		if self.flip:
			img = cv2.flip(img, 1)

		# Grayscale
		if self.grayscale:
			# Do some shit here so it doesnt break sometimes
			try:
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			except:
				img = np.zeros((48,48,1))
				return

		# Resize
		img = cv2.resize(img, self.out_dims)

		return img

def main():
	uid = sys.argv[1]
	#if sys.argv[4] != "local":
	#	with SocketIO(sys.argv['4'], 3000, LoggingNamespace) as socketIO:

	c = Cam()

	n = Net(sys.argv[2], sys.argv[3])
	n.build()
	n.load_model()

	socketIO = SocketIO(sys.argv[4], 80, LoggingNamespace)
	print "Loaded Socket"

	last_emoji = 0;

	while True:
		try:
			cv2.imshow('webcam', c.read_adjusted())
		except:
			pass
		#cv2.imshow('webcamx4', cv2.resize(c.read_adjusted(), (192, 192)))
		try:
			m = n.ff(np.asarray(c.read_adjusted()).reshape(1,48,48,1))
		except:
			m = [[1,0,0,0,0,0,0]]		

		m = m[0]
		conf = max(m)
		emo = m.index(max(m))
		print LABELS[emo], conf

		if sys.argv[4] != "local" and last_emoji != emo:
			socketIO.emit('emojis',{"user_id": uid, "emoji": emo, "confidence": conf})
			print "emitted"

		last_emoji = emo

		if cv2.waitKey(1) == 27:
			break

	#if sys.argv[4] != "local":
	#	ws.send({"user_id": uid, "emoji": -1, "confidence": conf})
	#	ws.close()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
