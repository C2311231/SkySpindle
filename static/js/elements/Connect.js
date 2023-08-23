
// Vars 

const Disconect = document.getElementById('disconectBTN');
const Connect = document.getElementById('connectBTN');
const Port = document.getElementById('PortDropDown');
const Portlabel = document.getElementById('portLabel');
const GrblStatus = document.getElementById('GrblStatus');


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

window.socket.on('Machine Status', function (data) {
    GrblStatus.innerText = data;
});