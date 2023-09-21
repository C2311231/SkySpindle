import os
import requests
import json

github_base_url = 'https://github.com/ajaxorg/ace-builds/tree/480d8ed11f92390190cff8093c376dc5514b3db0/'
folder = 'src-min-noconflict'
github_raw_base_url = 'https://raw.githubusercontent.com/ajaxorg/ace-builds/master/'

def pullFile(source, target):
    r = requests.get(source)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w') as file:
         file.write((r.content).decode())
         
def getGitHubFolderContents(base_url, folder):
    result = requests.get(base_url + folder)
    data = json.loads(result.text)
    fileNames = []
    for item in data["payload"]["tree"]["items"]:
        if item["contentType"] == "directory":
            fileNames = fileNames + getGitHubFolderContents(base_url, item["path"])
        else:
            fileNames.append(item["path"])
    return fileNames


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