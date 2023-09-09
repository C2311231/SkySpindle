const ConnectionIndicater = document.getElementById('ConnectionIndicater')

// Receive data handlers
window.socket.on('connect', function () {
    console.log('I\'m connected!');
    ConnectionIndicater.getElementsByTagName('title')[0].innerHTML = 'Connected to Server'
    ConnectionIndicater.style.color = 'green'
});

window.socket.on('disconnect', function () {
    console.log('I\'m not connected!');
    ConnectionIndicater.getElementsByTagName('title')[0].innerHTML = 'Disconnected from Server'
    ConnectionIndicater.style.color = 'red'
});



const dropArea = document.getElementsByTagName('body')[0];

// Prevent default behavior when a file is dragged over the drop area
dropArea.addEventListener('dragover', event => {
    event.preventDefault();
    dropArea.style.border = '2px dashed blue';
});

// Handle file drop
dropArea.addEventListener('drop', event => {
    event.preventDefault();
    dropArea.style.border = 'none';

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