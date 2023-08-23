var SendConsole = document.getElementById('consolesend')
var ConsoleInput = document.getElementById('consoleinput')
var grblconsole = document.getElementById('Consolelist');



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

SendConsole.addEventListener("click", SendConsoleInput);

function SendConsoleInput() {
    window.socket.emit('sendconsole', ConsoleInput.value);
    ConsoleInput.value = '';
}

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
