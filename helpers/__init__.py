import serial.tools.list_ports
import csv
import requests

def seconds_to_mixed_units(seconds):
    # Calculate the number of days, hours, minutes, and remaining seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{round(days)}:{round(hours)}:{round(minutes)}:{round(seconds)}"

def getUSBPorts():
    comPorts = serial.tools.list_ports.comports()
    ports = []
    for port in comPorts:
        ports.append(port.device)
    return ports

def getCSVData(filename):
    Data = []
    with open(f"./data/{filename}", "r") as f:
        data = csv.DictReader(f)
        for item in data:
            Data.append(item)
    return Data

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