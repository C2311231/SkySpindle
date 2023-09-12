import serial.tools.list_ports
import csv

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