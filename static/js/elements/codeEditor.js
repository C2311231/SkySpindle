const SaveFileBtn = document.getElementById('SaveFileBtn')

FileEditor = ace.edit("FileEditor", {
    theme: "ace/theme/twilight",
    mode: "ace/mode/gcode",
    value: ``
});


SaveFileBtn.addEventListener('click', function () {
        var blob = new Blob([FileEditor.getValue()], { type: 'text/plain' });
        var file = new File([blob], window.loadedfilename, { type: 'text/plain' });
        var formData = new FormData();
        formData.append('file', file);
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
)

window.socket.on('LoadedFile', function (data) {
    window.loadedfile = ''
    data.forEach(element => {
        window.loadedfile += element;
    });
    FileEditor.session.setValue(window.loadedfile);
});