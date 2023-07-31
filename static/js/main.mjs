import '/static/js/SocketIo.js';

window.socket = io()


// Slider Handlers

var Jogslider = document.getElementById("Jogdistance");
var JogDis = document.getElementById("JogDisLabel");
var Feed = document.getElementById("JogFeed");
var FeedLabel = document.getElementById("JogFeedLabel");
var Spindle = document.getElementById("JogSpindle");
var SpindleLabel = document.getElementById("JogSpindleLabel");
FeedLabel.value = Feed.value;
FeedLabel.value = Feed.value;
JogDis.value = 10;
Jogslider.oninput = function () {
    if (this.value < 10)
        JogDis.value = Math.round((this.value * 0.1) * 10) / 10;
    else if (this.value < 20)
        JogDis.value = Math.round((this.value - 9) * 10) / 10;
    else if (this.value < 24)
        JogDis.value = Math.round((10 + (this.value - 19) * 5) * 10) / 10;
    else if (this.value < 51)
        JogDis.value = Math.round((30 + (this.value - 23) * 10) * 10) / 10;
}
Feed.oninput = function () {
    FeedLabel.value = this.value;
}
Spindle.oninput = function () {
    SpindleLabel.value = this.value;
}




// Receive data handlers

var Xpos = document.getElementById('Xpos');
var Ypos = document.getElementById('Ypos');
var Zpos = document.getElementById('Zpos');

var machineAccelerationX = document.getElementById('machineAccelerationX');
var machineAccelerationY = document.getElementById('machineAccelerationY');
var machineAccelerationZ = document.getElementById('machineAccelerationZ');

var machineMaxRateX = document.getElementById('machineMaxRateX');
var machineMaxRateY = document.getElementById('machineMaxRateY');
var machineMaxRateZ = document.getElementById('machineMaxRateZ');

var Feedrate = document.getElementById('Feedrate');
var Spindle = document.getElementById('Spindle');

var operations = document.getElementById('operations');
var grblconsole = document.getElementById('Consolelist');


window.socket.on('connect', function () {
    console.log('I\'m connected!');
});

window.socket.on('position', function (data) {
    Xpos.value = data[0]
    Ypos.value = data[1]
    Zpos.value = data[2]
});
// window.socket.on('settings', function (data) {
//     data.
// });
window.socket.on('console', function (data) {
    grblconsole.innerHTML = ```        
    <div class="consoleitem ${data.class}">
        <h5>${data.timestamp} -- ${data.command}</h5>
    </div>
    <hr>
    ``` + grblconsole.innerHTML;
});
window.socket.on('machine', function (data) {
    machineAccelerationX.value = data.machineAccelerationX;
    machineAccelerationY.value = data.machineAccelerationY;
    machineAccelerationZ.value = data.machineAccelerationZ;

    machineMaxRateX.value = data.machineMaxRateX;
    machineMaxRateY.value = data.machineMaxRateY;
    machineMaxRateZ.value = data.machineMaxRateZ;

    Feedrate.value = data.Feedrate;
    Spindle.value = data.Spindle;
});

window.socket.on('operation', function (data) {
    operations.innerHTML += ```        
    <div class="listItem">
        ${data.filename} < button class="CycleStart" onClick=(function(){window.socket.emit('Start', ${data.filename}}))>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" class="bi bi-play-fill" viewBox="0 0 16 16">
                <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z" />
            </svg>
        </button >
    </div >
    <hr>```;
});


// Send data


var JogLeft = document.getElementsByClassName('JogBtnL');
var JogRight = document.getElementsByClassName('JogBtnR');
var JogUp = document.getElementsByClassName('JogBtnU');
var JogDown = document.getElementsByClassName('JogBtnD');
var JogVUp = document.getElementsByClassName('JogBtnUp');
var JogVDown = document.getElementsByClassName('JogBtnDown');
for (var i = 0; i < JogLeft.length; i++) {
    JogLeft[i].addEventListener("click", SendJogLeft);
}
for (var i = 0; i < JogRight.length; i++) {
    JogRight[i].addEventListener("click", SendJogRight);
}
for (var i = 0; i < JogUp.length; i++) {
    JogUp[i].addEventListener("click", SendJogUp);
}
for (var i = 0; i < JogDown.length; i++) {
    JogDown[i].addEventListener("click", SendJogDown);
}
for (var i = 0; i < JogVUp.length; i++) {
    JogVUp[i].addEventListener("click", SendJogVerticalUp);
}
for (var i = 0; i < JogVDown.length; i++) {
    JogVDown[i].addEventListener("click", SendJogVerticalDown);
}

//Send Jog command
function SendJogLeft(){
    window.socket.emit('Jog', {x: -(JogDis.value), y: 0, z: 0});
};

function SendJogRight(){
    window.socket.emit('Jog', {x: JogDis.value, y: 0, z: 0});
};

function SendJogUp(){
    window.socket.emit('Jog', {x: 0, y: JogDis.value, z: 0});
};

function SendJogDown(){
    window.socket.emit('Jog', {x: 0, y: -(JogDis.value), z: 0});
};

function SendJogVerticalUp(){
    window.socket.emit('Jog', {x: 0, y: 0, z: JogDis.value});
};

function SendJogVerticalDown(){
    window.socket.emit('Jog', {x: 0, y: 0, z: -(JogDis.value)});
};