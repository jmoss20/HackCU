import cv2
import numpy as np
# from net import Agent


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
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Resize
		img = cv2.resize(img, self.out_dims)

		return img

def main():
	c = Cam()
	while True:
		cv2.imshow('webcam', c.read_adjusted())
		cv2.imshow('webcamx4', cv2.resize(c.read_adjusted(), (192, 192)))
		

		if cv2.waitKey(1) == 27:
			break

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
