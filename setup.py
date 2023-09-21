import os
import requests
import json

github_base_url = 'https://github.com/ajaxorg/ace-builds/tree/480d8ed11f92390190cff8093c376dc5514b3db0/'
folder = 'src-min-noconflict'
github_raw_base_url = 'https://raw.githubusercontent.com/ajaxorg/ace-builds/master/'




for file in getGitHubFolderContents(github_base_url, folder):
    print(file)
    pullFile(github_raw_base_url + file, f'./WebInterface/static/{file}')


files = ['build_option_codes_en_US.csv','alarm_codes_en_US.csv', 'error_codes_en_US.csv', 'setting_codes_en_US.csv']
for file in files:
    r = requests.get(f"https://raw.githubusercontent.com/gnea/grbl/master/doc/csv/{file}")
    with open(f'./data/{file}', 'w') as file:
        file.write((r.content).decode())


r = requests.get("https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js")
with open(f'./WebInterface/static/js/SocketIo.js', 'w') as file:
        file.write((r.content).decode())



os.makedirs("./OperationFiles", exist_ok=True)