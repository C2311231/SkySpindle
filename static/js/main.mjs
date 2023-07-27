import '/static/js/SocketIo.js';

var socket = io()
socket.on('connect', function() {
    console.log('I\'m connected!');
});