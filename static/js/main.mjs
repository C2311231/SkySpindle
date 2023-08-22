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

var machineSetting = document.getElementsByClassName('machineSetting')


var CloseMachineSettings = document.getElementById('CloseMachineSettings');
var MachineSettings = document.getElementById('MachineSettings');
var OpenMachineSettings = document.getElementById('OpenMachineSettings');
var overlay = document.getElementById('overlay');


var MXpos = document.getElementById('MXpos');
var MYpos = document.getElementById('MYpos');
var MZpos = document.getElementById('MZpos');


//UI Logic
CloseMachineSettings.onclick = function () {
    MachineSettings.style = 'display: none'
    overlay.style = 'display: none'
}
OpenMachineSettings.onclick = function () {
    MachineSettings.style = 'display: block'
    overlay.style = 'display: block'
}




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

window.socket.on('positionW', function (data) {
    Xpos.value = data[0]
    Ypos.value = data[1]
    Zpos.value = data[2]
});
window.socket.on('positionM', function (data) {
    MXpos.innerHTML = `X |${data[0]}|`
    MYpos.innerHTML = `Y |${data[1]}|`
    MZpos.innerHTML = `Z |${data[2]}|`
});

window.socket.on('settings', function (data) {
    if (UPDATESETTINGS){
        document.getElementById('110').value = data.$110
        document.getElementById('111').value = data.$111
        document.getElementById('112').value = data.$112

        document.getElementById('120').value = data.$120
        document.getElementById('121').value = data.$121
        document.getElementById('122').value = data.$122

        document.getElementById('100').value = data.$100
        document.getElementById('101').value = data.$101
        document.getElementById('102').value = data.$102

        document.getElementById('130').value = data.$130
        document.getElementById('131').value = data.$131
        document.getElementById('132').value = data.$132

        document.getElementById('31').value = data.$31
        document.getElementById('30').value = data.$30

        document.getElementById('0').value = data.$0
        document.getElementById('1').value = data.$1
        document.getElementById('2').value = data.$2

        document.getElementById('3').value = data.$3
        document.getElementById('4').value = data.$4
        document.getElementById('5').value = data.$5

        document.getElementById('6').value = data.$6
        document.getElementById('10').value = data.$10
        document.getElementById('11').value = data.$11

        document.getElementById('12').value = data.$12
        document.getElementById('13').value = data.$13
        document.getElementById('20').value = data.$20

        document.getElementById('21').value = data.$21
        document.getElementById('22').value = data.$22
        document.getElementById('23').value = data.$23
        
        document.getElementById('24').value = data.$24
        document.getElementById('25').value = data.$25
        document.getElementById('26').value = data.$26

        document.getElementById('27').value = data.$27
        document.getElementById('32').value = data.$32
    }
});
const maxConsoleItems = 500; // Set the maximum number of console items

window.socket.on('console', function (data) {    
    // Create a new console item
    const consoleItem = document.createElement('div');
    consoleItem.classList.add('consoleitem');
    consoleItem.innerHTML = `<h5>${htmlEscape(data)}</h5>`;
    
    // Insert the new console item at the beginning of the container
    grblconsole.insertBefore(consoleItem, grblconsole.firstChild);
    
    // Remove excess console items if the limit is exceeded
    const consoleItems = grblconsole.getElementsByClassName('consoleitem');
    if (consoleItems.length > maxConsoleItems) {
        while (consoleItems.length > maxConsoleItems) {
            grblconsole.removeChild(consoleItems[maxConsoleItems]);
        }
    }
});
// <h5>${data.timestamp} -- ${htmlEscape(data.command)}</h5>    ${data.class}
window.socket.on('operations', function (data) {
    operations.innerHTML = `<h2>Saved cycles:</h2><hr>`;
    data.forEach(element => {
        operations.innerHTML += `        
        <div class="listItem">
            ${element} <button class="CycleStart" onClick="window.socket.emit('Start', '${element}');">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" class="bi bi-play-fill" viewBox="0 0 16 16">
                    <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z" />
                </svg>
            </button >
        </div >
        <hr>`;  
    });

});
window.socket.on('USBPorts', function (data) {
    Port.innerHTML = '';
    for (var i = 0; i < data.length; i++) {
        Port.innerHTML += `<option value="${data[i]}">${data[i]}</option>`
    }
})

// Send data

for (let i = 0; i < machineSetting.length; i++) {
    machineSetting[i].oninput = function () {
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
const dropArea = document.getElementsByTagName('body')[0];

// Prevent default behavior when a file is dragged over the drop area
dropArea.addEventListener('dragover', event => {
    event.preventDefault();
    dropArea.style.border = '2px dashed blue';
});

// Handle file drop
dropArea.addEventListener('drop', event => {
    event.preventDefault();
    dropArea.style.border = '2px dashed #ccc';

    const files = event.dataTransfer.files;
    for (var i = 0; i < files.length; i++) {
        if (files[i]) {
            const formData = new FormData();
            formData.append('file', files[i]);
    
            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log('File uploaded:', data);
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
        }
    }

});



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
