import serial.tools.list_ports
import csv
import requests
import json
import os

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
         
def getGitHubFolderContents(api_url):
    result = requests.get(api_url)
    data = result.json()  # safer than json.loads(result.text)
    fileNames = []

    for item in data:
        if item["type"] == "dir":
            # Recursive call for subdirectories
            sub_url = item["url"]
            fileNames.extend(getGitHubFolderContents(sub_url))
        else:
            fileNames.append(item["path"])

    return fileNames
