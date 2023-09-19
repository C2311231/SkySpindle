const operations = document.getElementById('operations');
const StatusCircle = document.getElementById('StatusCircle');
const StatusText = document.getElementById('StatusText');
const OperationTime = document.getElementById('OperationTime');
const OperationLineNum = document.getElementById('OperationLineNum');
const OperationETA = document.getElementById('OperationETA');
const LoadedFileName = document.getElementById('LoadedFileName');

window.loadedfile = ''
const OperationCancel = document.getElementById('OperationCancel');
const OperationHold = document.getElementById('OperationHold');
const OperationPause = document.getElementById('OperationPause');
const OperationStart = document.getElementById('OperationStart');

const JobStatus = document.getElementById('JobStatus');
const OperationList = document.getElementById('OperationList');

window.socket.on('operations', function (data) {
  operations.innerHTML = ''
  data.forEach(element => {
    operations.innerHTML += `        
        <div class="listItem">
            ${element}
            <button class="Btn" title="Load File" onClick="loadFile('${element}')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="lightblue" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
                    <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
                </svg>
            </button >
            <button class="Btn" onClick="deleteFile('${element}')">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#972b2b" class="bi bi-trash3" viewBox="0 0 16 16">
                    <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z"/>
                </svg>
            </button>
        </div >
        <hr>`;
  });

});

function loadFile(element) {
  window.socket.emit('loadFile', element);
  window.loadedfilename = element
}

document.getElementById('uploadButton').addEventListener('click', function () {
  document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function (event) {
  const file = event.target.files[0];
  if (file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        // Handle the JSON response data here
        console.log(data); // Replace with your desired behavior
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
});

var StartTime = Date.now()

window.socket.on('operationTime', function (data) {
  var diff = data*1000;
  var days = diff / 86400000 | 0;
  diff -= days * 86400000;
  var hours = diff / 3600000 | 0;
  diff -= hours * 3600000;
  var minutes = diff / 60000 | 0;
  diff -= minutes * 60000;
  var seconds = diff / 1000 | 0;
  OperationTime.innerHTML = `Time: ${days}:${hours}:${minutes}:${seconds}`;
});

window.socket.on('ETA', function (data) {
  OperationETA.innerHTML = `ETA: ${data}`
});

window.socket.on('lineNum', function (data) {
  OperationLineNum.innerHTML = `Line Number: ${data[0]}/${data[1]}`
  var completionfull = (data[0]/data[1])*100
  if(completionfull>=10){
    var completion = completionfull.toFixed(0)
  }
  else{
    var completion = completionfull.toFixed(1)
  }
  if (completion.toString().length == 3) {
    StatusText.setAttribute("x", '37px');
  }
  else if (completion.toString().length == 2) {
    StatusText.setAttribute("x", '51px')
  }
  else {
    StatusText.setAttribute("x", '65px')
  }
  var dashOffset = 565 - (completionfull * (565 / 100));
  StatusCircle.setAttribute('stroke-dashoffset', `${dashOffset}px`);
  StatusText.innerHTML = `${completion}%`;
  document.title = `SkySpindle - ${completion}%`
  if(completionfull>=100){
    document.title = `SkySpindle - Done`
  }
});
window.socket.on('loadedFileName', function (data) {
  LoadedFileName.innerHTML = data
});

OperationCancel.onclick = function(){
  window.socket.emit('unloadStopOperation')
}
OperationHold.onclick = function(){
  window.socket.emit('holdOperation')
}
OperationPause.onclick = function(){
  window.socket.emit('pauseOperation')
}
OperationStart.onclick = function(){
  window.socket.emit('start', LoadedFileName.innerHTML)
}
function CheckForLoad(){
  if (window.loadedfile != ''){
    OperationList.style.display = 'none'
    JobStatus.style.display = 'block'
  }
  else{
    OperationList.style.display = 'block'
    JobStatus.style.display = 'none'
  }
}
setInterval(CheckForLoad, 500)

function deleteFile(element){
  window.socket.emit('deleteFile', element);
}