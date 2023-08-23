// Receive data handlers
window.socket.on('connect', function () {
    console.log('I\'m connected!');
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