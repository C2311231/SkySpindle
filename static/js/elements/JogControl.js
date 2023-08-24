
//      vars

const Jogslider = document.getElementById("Jogdistance");
const JogDis = document.getElementById("JogDisLabel");

const Feed = document.getElementById("JogFeed");
const FeedLabel = document.getElementById("JogFeedLabel");

const SpindleOveride = document.getElementById("JogSpindle");
const SpindleLabel = document.getElementById("JogSpindleLabel");

const RapidOveride = document.getElementById("JogRapid");
const RapidOverideLabel = document.getElementById("JogRapidLabel");

const HomeAll = document.getElementById('HomeAll');
const HomeXY = document.getElementById('HomeXY');

const HomeX = document.getElementById('HomeX');
const HomeY = document.getElementById('HomeY');
const HomeZ = document.getElementById('HomeZ');

const JogLeft = document.getElementsByClassName('JogBtnL');
const JogRight = document.getElementsByClassName('JogBtnR');
const JogUp = document.getElementsByClassName('JogBtnU');
const JogDown = document.getElementsByClassName('JogBtnD');
const JogVUp = document.getElementsByClassName('JogBtnUp');
const JogVDown = document.getElementsByClassName('JogBtnDown');

const SpindleOn = document.getElementById('SpindleOn');
const SpindleOff = document.getElementById('SpindleOff');


const MXpos = document.getElementById('MXpos');
const MYpos = document.getElementById('MYpos');
const MZpos = document.getElementById('MZpos');

const Xpos = document.getElementById('Xpos');
const Ypos = document.getElementById('Ypos');
const Zpos = document.getElementById('Zpos');

const ResetZero = document.getElementById('ResetZero');
const ToggleMist = document.getElementById('ToggleMist');
const ToggleFlood = document.getElementById('ToggleFlood');

var timeoutId;


// Slider Handlers

MXpos.addEventListener("click", function () {
    window.socket.emit('ZeroAxis', ['X']);
});
MYpos.addEventListener("click", function () {
    window.socket.emit('ZeroAxis', ['Y']);
});
MZpos.addEventListener("click", function () {
    window.socket.emit('ZeroAxis', ['Z']);
});

ResetZero.addEventListener("click", function () {
    window.socket.emit('ZeroAxis', ['X', 'Y', 'Z']);
});

ToggleMist.addEventListener("click", function () {
    window.socket.emit('ToggleMist');
});

ToggleFlood.addEventListener("click", function () {
    window.socket.emit('ToggleFlood');
});

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
    Xpos.value = data[0];
    Ypos.value = data[1];
    Zpos.value = data[2];
});
window.socket.on('positionM', function (data) {
    MXpos.innerHTML = `X |${data[0]}|`;
    MYpos.innerHTML = `Y |${data[1]}|`;
    MZpos.innerHTML = `Z |${data[2]}|`;
});

for (var i = 0; i < JogLeft.length; i++) {
    JogLeft[i].addEventListener("click", function () {
        window.socket.emit('Jog', { x: -(JogDis.value), y: 0, z: 0, f: window.feedrate});
    });
}
for (var i = 0; i < JogRight.length; i++) {
    JogRight[i].addEventListener("click", function () {
        window.socket.emit('Jog', { x: JogDis.value, y: 0, z: 0, f: (window.feedrate)});
    });
}
for (var i = 0; i < JogUp.length; i++) {
    JogUp[i].addEventListener("click", function () {
        window.socket.emit('Jog', { x: 0, y: JogDis.value, z: 0, f: (window.feedrate)});
    });
}
for (var i = 0; i < JogDown.length; i++) {
    JogDown[i].addEventListener("click", function () {
        window.socket.emit('Jog', { x: 0, y: -(JogDis.value), z: 0, f: (window.feedrate)});
    });
}
for (var i = 0; i < JogVUp.length; i++) {
    JogVUp[i].addEventListener("click", function () {
        window.socket.emit('Jog', { x: 0, y: 0, z: JogDis.value, f: (window.feedrate)});
    });
}
for (var i = 0; i < JogVDown.length; i++) {
    JogVDown[i].addEventListener("click", function () {
        window.socket.emit('Jog', { x: 0, y: 0, z: -(JogDis.value), f: (window.feedrate)});
    });
}


HomeAll.addEventListener('click', function () { window.socket.emit('home', 'XYZ') });
HomeXY.addEventListener('click', function () { window.socket.emit('home', 'XY') });
HomeX.addEventListener('click', function () { window.socket.emit('home', 'X') });
HomeY.addEventListener('click', function () { window.socket.emit('home', 'Y') });
HomeZ.addEventListener('click', function () { window.socket.emit('home', 'Z') });


SpindleOff.addEventListener('click', function () { window.socket.emit('spindle', '0') });
SpindleOn.addEventListener('click', function () { window.socket.emit('spindle', window.spindlespeed) });
