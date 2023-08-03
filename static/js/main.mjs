import '/static/js/SocketIo.js';

window.socket = io()
var timeoutId;


var UPDATESETTINGS = true;
//Vars
var Jogslider = document.getElementById("Jogdistance");
var JogDis = document.getElementById("JogDisLabel");

var Feed = document.getElementById("JogFeed");
var FeedLabel = document.getElementById("JogFeedLabel");

var SpindleOveride = document.getElementById("JogSpindle");
var SpindleLabel = document.getElementById("JogSpindleLabel");

var RapidOveride = document.getElementById("JogRapid");
var RapidOverideLabel = document.getElementById("JogRapidLabel");

var Disconect = document.getElementById('disconectBTN');
var Connect = document.getElementById('connectBTN');
var Port = document.getElementById('PortDropDown');
var Portlabel = document.getElementById('portLabel');

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

var HomeAll = document.getElementById('HomeAll');
var HomeXY = document.getElementById('HomeXY');

var HomeX = document.getElementById('HomeX');
var HomeY = document.getElementById('HomeY');
var HomeZ = document.getElementById('HomeZ');

var JogLeft = document.getElementsByClassName('JogBtnL');
var JogRight = document.getElementsByClassName('JogBtnR');
var JogUp = document.getElementsByClassName('JogBtnU');
var JogDown = document.getElementsByClassName('JogBtnD');
var JogVUp = document.getElementsByClassName('JogBtnUp');
var JogVDown = document.getElementsByClassName('JogBtnDown');

var SpindleOn = document.getElementById('SpindleOn');
var SpindleOff = document.getElementById('SpindleOff');
var SpindleSpeed = document.getElementById('Spindle');

var SendConsole = document.getElementById('consolesend')
var ConsoleInput = document.getElementById('consoleinput')

var machineOptions = document.getElementsByClassName('machineOption')

// Slider Handlers

FeedLabel.value = Feed.value;
SpindleLabel.value = SpindleOveride.value;
RapidOverideLabel.value = 100;
RapidOveride.value = 3;
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
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function () {
    FeedLabel.value = Feed.value;
    window.socket.emit('FeedOveride', Feed.value);
    }, 500)
}

FeedLabel.oninput = function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function () {
    if (FeedLabel.value > 200){
        FeedLabel.value = 200;
    }
    if (FeedLabel.value < 1){
        FeedLabel.value = 1;
    }
    Feed.value = FeedLabel.value;
    window.socket.emit('FeedOveride', FeedLabel.value);
    }, 500)
}
SpindleOveride.oninput = function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function () {
    SpindleLabel.value = SpindleOveride.value;
    window.socket.emit('SpindleOveride', SpindleOveride.value);
    }, 500)
}

SpindleLabel.oninput = function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function () {
    if (SpindleLabel.value > 200){
        SpindleLabel.value = 200;
    }
    if (SpindleLabel.value < 1){
        SpindleLabel.value = 1;
    }
    SpindleOveride.value = SpindleLabel.value;
    window.socket.emit('SpindleOveride', SpindleLabel.value);
    }, 500)
}

RapidOveride.oninput = function () {
    if (this.value == 1) {
        RapidOverideLabel.value = 25;
        window.socket.emit('RapidOveride', RapidOverideLabel.value);
    }

    else if (this.value == 2) {
        RapidOverideLabel.value = 50;
        window.socket.emit('RapidOveride', RapidOverideLabel.value);
    }
    else {
        RapidOverideLabel.value = 100;
        window.socket.emit('RapidOveride', RapidOverideLabel.value);
    }
}

RapidOverideLabel.oninput = function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function () {
        if (RapidOverideLabel.value <= 37) {
            RapidOverideLabel.value = 25;
            RapidOveride.value = 1;
        } else if (RapidOverideLabel.value < 75) {
            RapidOverideLabel.value = 50;
            RapidOveride.value = 2;
        } else {
            RapidOverideLabel.value = 100;
            RapidOveride.value = 3;
        }
    }, 500);
};





// Receive data handlers
window.socket.on('connect', function () {
    console.log('I\'m connected!');
});

window.socket.on('State', function (data) {
    if (data == 'Disconnected'){
        DisconnectUpdate();
    }
    else if (data == 'Connected') {
        ConnectUpdate();
    }
});

window.socket.on('Overides', function (data) {
    Feed.value = data[0];
    FeedLabel.value = data[0];
    if (data[1]/25 == 4){
        RapidOveride.value = 3;
    }
    else {
        RapidOveride.value = data[1]/25;
    }
    RapidOverideLabel.value = data[1];
    SpindleOveride.value = data[2];
    SpindleLabel.value = data[2];
});

window.socket.on('position', function (data) {
    Xpos.value = data[0]
    Ypos.value = data[1]
    Zpos.value = data[2]
});
window.socket.on('settings', function (data) {
    if (UPDATESETTINGS){
    document.getElementById('machineMaxRateX').value = data.$110
    document.getElementById('machineMaxRateY').value = data.$111
    document.getElementById('machineMaxRateZ').value = data.$112

    document.getElementById('machineAccelerationX').value = data.$120
    document.getElementById('machineAccelerationY').value = data.$121
    document.getElementById('machineAccelerationZ').value = data.$122

    document.getElementById('machineStepsX').value = data.$100
    document.getElementById('machineStepsY').value = data.$101
    document.getElementById('machineStepsZ').value = data.$102

    document.getElementById('machineMaxTravelX').value = data.$130
    document.getElementById('machineMaxTravelY').value = data.$131
    document.getElementById('machineMaxTravelZ').value = data.$132

    document.getElementById('SpindleMin').value = data.$31
    document.getElementById('SpindleMax').value = data.$30

    document.getElementById('machineStepPulse').value = data.$0
    document.getElementById('machineStepDelay').value = data.$1
    document.getElementById('machineStepPortInvert').value = data.$2

    document.getElementById('DirectionInvert').value = data.$3
    document.getElementById('StepEnableInvert').value = data.$4
    document.getElementById('LimitPinsInvert').value = data.$5

    document.getElementById('ProbePinInvert').value = data.$6
    document.getElementById('StatusReportMode').value = data.$10
    document.getElementById('JunctionDeviation').value = data.$11

    document.getElementById('ArcTolerance').value = data.$12
    document.getElementById('Inches').value = data.$13
    document.getElementById('Softlimits').value = data.$20

    document.getElementById('HardLimit').value = data.$21
    document.getElementById('HomingCycle').value = data.$22
    document.getElementById('InvertHomeDir').value = data.$23
    
    document.getElementById('HomingFeed').value = data.$24
    document.getElementById('HomingSeek').value = data.$25
    document.getElementById('HomingDebounce').value = data.$26

    document.getElementById('HomingPull-off').value = data.$27
    document.getElementById('LaserMode').value = data.$32
    }
});
window.socket.on('console', function (data) {
    if (data.class == 'systemquery') {
        return
    }
    grblconsole.innerHTML = `        
    <div class="consoleitem ${data.class}">
        <h5>${data.timestamp} -- ${htmlEscape(data.command)}</h5>
    </div>
    <hr>
    ` + grblconsole.innerHTML;
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
window.socket.on('USBPorts', function (data) {
    Port.innerHTML = '';
    for (var i = 0; i < data.length; i++) {
        Port.innerHTML += `<option value="${data[i]}">${data[i]}</option>`
    }
})

// Send data

for (let i = 0; i < machineOptions.length; i++) {
    let inputElement = machineOptions[i].getElementsByTagName('input')[0];
    inputElement.oninput = function () {
        clearTimeout(timeoutId);
        var inputData = this; // Use 'this' to refer to the current inputElement
        timeoutId = setTimeout(function () {
            window.socket.emit('ChangeSetting', [inputData.dataset.send, inputData.value]);
        }, 500);
    };
}




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
function SendJogLeft() {
    window.socket.emit('Jog', { x: -(JogDis.value), y: 0, z: 0 });
};

function SendJogRight() {
    window.socket.emit('Jog', { x: JogDis.value, y: 0, z: 0 });
};

function SendJogUp() {
    window.socket.emit('Jog', { x: 0, y: JogDis.value, z: 0 });
};

function SendJogDown() {
    window.socket.emit('Jog', { x: 0, y: -(JogDis.value), z: 0 });
};

function SendJogVerticalUp() {
    window.socket.emit('Jog', { x: 0, y: 0, z: JogDis.value });
};

function SendJogVerticalDown() {
    window.socket.emit('Jog', { x: 0, y: 0, z: -(JogDis.value) });
};



SendConsole.addEventListener("click", SendConsoleInput);

function SendConsoleInput() {
    window.socket.emit('sendconsole', ConsoleInput.value);
    ConsoleInput.value = '';
}
//Homing Commands

HomeAll.addEventListener('click', function () { window.socket.emit('home', 'XYZ') });
HomeXY.addEventListener('click', function () { window.socket.emit('home', 'XY') });
HomeX.addEventListener('click', function () { window.socket.emit('home', 'X') });
HomeY.addEventListener('click', function () { window.socket.emit('home', 'Y') });
HomeZ.addEventListener('click', function () { window.socket.emit('home', 'Z') });

//Spindle Commands



SpindleOff.addEventListener('click', function () { window.socket.emit('spindle', '0') });
SpindleOn.addEventListener('click', function () { window.socket.emit('spindle', SpindleSpeed.value) });

//Connection Commands
Connect.addEventListener('click', function () {
    window.socket.emit('Connect', Port.value)
    ConnectUpdate();
})
Disconect.addEventListener('click', function () {
    window.socket.emit('Disconnect')
    DisconnectUpdate();
})


function ConnectUpdate() {
    Connect.style.display = 'none';
    Port.style.display = 'none';
    Portlabel.style.display = 'none';
    Disconect.style.display = 'inline';
}
function DisconnectUpdate() {
    Connect.style.display = 'inline';
    Port.style.display = 'inline';
    Disconect.style.display = 'none';
}






// Extra Functions
function htmlEscape(str) {
    str = String(str);
    return str.replace(/[&<>"']/g, function (match) {
        switch (match) {
            case '&':
                return '&amp;';
            case '<':
                return '&lt;';
            case '>':
                return '&gt;';
            case '"':
                return '&quot;';
            case "'":
                return '&apos;';
            default:
                return match;
        }
    });
}
