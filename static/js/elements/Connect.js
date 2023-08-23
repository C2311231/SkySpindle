
// Vars 

var Disconect = document.getElementById('disconectBTN');
var Connect = document.getElementById('connectBTN');
var Port = document.getElementById('PortDropDown');
var Portlabel = document.getElementById('portLabel');

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

//Connection Commands
Connect.addEventListener('click', function () {
    window.socket.emit('Connect', Port.value)
    ConnectUpdate();
})
Disconect.addEventListener('click', function () {
    window.socket.emit('Disconnect')
    DisconnectUpdate();
})

window.socket.on('USBPorts', function (data) {
    Port.innerHTML = '';
    for (var i = 0; i < data.length; i++) {
        Port.innerHTML += `<option value="${data[i]}">${data[i]}</option>`
    }
})

window.socket.on('State', function (data) {
    if (data == 'Disconnected'){
        DisconnectUpdate();
    }
    else if (data == 'Connected') {
        ConnectUpdate();
    }
});