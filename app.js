var app = require('express')();
var server = require('http').Server(app).listen(3000);
var io = require('socket.io')(server);

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/hackcuwebpage.html');
});

app.get('/emoji', function (req, res) {
  res.sendFile(__dirname + '/popup.html');
});

io.on('connection', function (socket) {
	socket.emit('emojis',obj);
	socket.emit('emojis',obj2);
	socket.emit('emojis',obj3);
	socket.emit('emojis',obj4);
});

obj = {
	user_id: 'sam',
	emoji: "1",
	confidence: ""
}
obj2 = {
	user_id: 'connor',
	emoji: "2",
	confidence: ""
}
obj3 = {
	user_id: 'barrett',
	emoji: "3",
	confidence: ""
}
obj4 = {
	user_id: 'connor',
	emoji: "4",
	confidence: ""
}
