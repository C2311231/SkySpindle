const ALARMWindow = document.getElementById('ALARMMenu')
const ALARMOverlay = document.getElementById('overlay2')
const ALARMUnlock = document.getElementById('ALARMUnlock')
function UpdateAlarm(data) {
    if (data.startsWith('Status: Alarm')){
        console.log(data)
        ALARMOverlay.style.display = 'block'
        ALARMWindow.style.display = 'block'
    }
    else {
        ALARMOverlay.style.display = 'none'
        ALARMWindow.style.display = 'none'
    }
};

ALARMUnlock.onclick = function(){
    window.socket.emit('UNLOCKALARM')
}