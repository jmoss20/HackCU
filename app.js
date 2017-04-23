var app = require('express')();
var server = require('http').Server(app).listen(3000);
var io = require('socket.io')(server);
console.log('server started')

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function (socket) {
	console.log("A user is connected")
	socket.on('message', function(data) {
		console.log('Received: ' + data);
		socket.emit('sendres', data);
	});
	socket.on('disconnect', function () {
    	console.log("A user is disconnected");
	});
});