import serial
import time
import re
import threading
import random
from alive_progress import alive_bar

value1 = 0
value2 = 0

for run in range(0,50):
    connection = serial.Serial('COM5', 115200)
    print('Opening Serial Port')
    connection.write(str.encode("\r\n\r\n")) # Wake up GRBL Connection
    time.sleep(5)
    i = 1
    global count
    count = 0
    requestedcount = 0
    global read
    read = True
    def reader():
        global count
        global read
        while True:
            line = connection.readline().decode().strip()
            if line.startswith('<') and line.endswith('>'):
                pass
            elif 'echo:' in line:
                pass
            elif 'ok' in line:
                count += 1
            time.sleep(0.05)

    stop_threads = False
    thread = threading.Thread(target=reader, daemon=True)
    thread.start()
    with open('./OperationFiles/HelloWorld.nc', 'r') as file:
        file = file.readlines()
        with alive_bar(len(file)) as bar:
            for line in file:
                l = line.strip() # Strip all EOL characters for consistency
                connection.write((l + f' N{i}\n').encode()) # Send g-code block to grbl
                requestedcount += 1
                if random.randint(0, 20) == 10:
                    connection.write((b'?\n')) # Send g-code block to grbl
                    requestedcount += 1
                while requestedcount > count:
                    time.sleep(0.1)
                i += 1
                bar()
    stop_threads = True
    time.sleep(5)
    print("Completed test", requestedcount, '', count)
    value1 = requestedcount
    value2 = count
    connection.close()
    time.sleep(10)

print("Done", value1, '', value2)