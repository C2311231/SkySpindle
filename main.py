import helpers
import os
import requests

if os.path.exists('./data/setting_codes_en_US.csv') == False:
    print("Downloading Setting Codes")
    os.makedirs("./data", exist_ok=True)
    with open(f'./data/setting_codes_en_US.csv', 'w') as file:
        file.write((requests.get(f"https://raw.githubusercontent.com/gnea/grbl/master/doc/csv/setting_codes_en_US.csv").content).decode())
    print("Done")

if os.path.exists('./WebInterface/static/src-min-noconflict/ace.js') == False:
    print("Downloading ACE         (May take a while)")
    for file in helpers.getGitHubFolderContents('https://api.github.com/repos/ajaxorg/ace-builds/contents/src-min-noconflict?ref=480d8ed11f92390190cff8093c376dc5514b3db0'):
        helpers.pullFile('https://raw.githubusercontent.com/ajaxorg/ace-builds/master/' + file, f'./WebInterface/static/{file}')
    print("Done")

if os.path.exists('./WebInterface/static/js/SocketIo.js') == False:
    print("Downloading SocketIO")
    with open(f'./WebInterface/static/js/SocketIo.js', 'w') as file:
            file.write((requests.get("https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js").content).decode())
    print("Done")

os.makedirs("./OperationFiles", exist_ok=True)


from WebInterface import app, socketio

socketio.run(app, debug=True, host='0.0.0.0')