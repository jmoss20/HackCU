# [HackCU III](https://2017.hackcu.org/)
Over 24 hours, we designed a web-based system for predicting representative emoji's from client's facial expressions (via their webcam feeds), and provided a web interface to view these emoji's in real time.  ([Devpost](https://devpost.com/software/super-emoji-face))

#### CV Client
Python script grabs camera frames (OpenCV), detects faces and their bounding boxes (Haar Cascades), selects largest face by area, downsamples and grayscales (OpenCV), feeds resulting pixel matrix into a 5-layer Convolutional Neural Network (Tensorflow/TF-Learn, LeNet-style architecture, [*]), yielding a predicted emoji sent to the server via SocketIO.

[*]: Heavily based on previous work [here](https://github.com/isseu/emotion-recognition-neural-networks), pending future improvements (hopefully) from insight [here](https://arxiv.org/pdf/1509.05371.pdf).

#### Web Server
Node.js / Express server (running on an EC2 instance for HackCU), utilizing SocketIO for communication between Python clients and browser clients.  Maintained state of all clients, and responsible for pushing new state updates to web client.

#### Web Client
Rendered predicted emoji's in the browser, receiving updates from the server via SocketIO.

## Dependencies
#### Python Client:
```
python-socketio
cv2
scipy
pandas
numpy
tensorflow
tflearn
h5py
```

#### Server:
```
(see package.json)
```
