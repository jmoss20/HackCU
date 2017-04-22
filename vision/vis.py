import cv2
import numpy as np

CASCADE_PATH = "data/haarcascade_frontalface_default.xml"

class Cam:
	def __init__(self, flip=True, cam_id=0):
		self.flip = flip
		self.cam_id = cam_id
		self.c = cv2.VideoCapture(self.cam_id)

	def read_raw(self):
		ret_val, img = self.c.read()
		return img

	def read_adjusted(self):
		img = self.read_raw()
		img = cv2.flip(img, 1)

		return img

def main():
	c = Cam(flip=True, cam_id=0)
	while True:
		print c.read_adjusted()
		cv2.imshow('webcam', c.read_adjusted())

		if cv2.waitKey(1) == 27:
			break

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
