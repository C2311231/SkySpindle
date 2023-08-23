
// Vars

var machineSetting = document.getElementsByClassName('machineSetting')
var CloseMachineSettings = document.getElementById('CloseMachineSettings');
var MachineSettings = document.getElementById('MachineSettings');
var OpenMachineSettings = document.getElementById('OpenMachineSettings');
var overlay = document.getElementById('overlay');

//UI Logic
CloseMachineSettings.onclick = function () {
    MachineSettings.style = 'display: none'
    overlay.style = 'display: none'
}
OpenMachineSettings.onclick = function () {
    MachineSettings.style = 'display: block'
    overlay.style = 'display: block'
}


window.socket.on('settings', function (data) {
    document.getElementById('110').value = data.$110;
    document.getElementById('111').value = data.$111;
    document.getElementById('112').value = data.$112;

    document.getElementById('120').value = data.$120;
    document.getElementById('121').value = data.$121;
    document.getElementById('122').value = data.$122;

    document.getElementById('100').value = data.$100;
    document.getElementById('101').value = data.$101;
    document.getElementById('102').value = data.$102;

    document.getElementById('130').value = data.$130;
    document.getElementById('131').value = data.$131;
    document.getElementById('132').value = data.$132;

    document.getElementById('31').value = data.$31;
    document.getElementById('30').value = data.$30;

    document.getElementById('0').value = data.$0;
    document.getElementById('1').value = data.$1;
    document.getElementById('2').value = data.$2;

    document.getElementById('3').value = data.$3;
    document.getElementById('4').value = data.$4;
    document.getElementById('5').value = data.$5;

    document.getElementById('6').value = data.$6;
    document.getElementById('10').value = data.$10;
    document.getElementById('11').value = data.$11;

    document.getElementById('12').value = data.$12;
    document.getElementById('13').value = data.$13;
    document.getElementById('20').value = data.$20;

    document.getElementById('21').value = data.$21;
    document.getElementById('22').value = data.$22;
    document.getElementById('23').value = data.$23;
    
    document.getElementById('24').value = data.$24;
    document.getElementById('25').value = data.$25;
    document.getElementById('26').value = data.$26;

    document.getElementById('27').value = data.$27;
    document.getElementById('32').value = data.$32;
});

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