import serial
import serial.tools.list_ports
import time
import datetime
import threading
def getUSBPorts():
    comPorts = serial.tools.list_ports.comports()
    ports = []
    for port in comPorts:
        ports.append(port.device)
    return ports


class GRBLConection():
    
    def __init__(self, port, baudrate):
        self.connection = serial.Serial(port, baudrate, timeout = 0.5)
        print('Opening Serial Port')
        self.connection.write(str.encode("\r\n\r\n")) # Wake up GRBL Connection
        time.sleep(2) # Wait for GRBL to respond
        print(self.connection.read_until(expected=b'ok\r\n').decode('utf-8'))
        # Default Values
        self.WCO = [0,0,0]
        self.Ov = [100, 100, 100]
        self.RealFeed = 0
        self.RealSpindle = 0
        self.triggeredPins = None
        self.accessoryState = None

        
    def SendCommand(self, command, socketio, htmlclass):
        if isinstance(command, bytes):
            self.connection.write(command)
            self.connection.write(str.encode('\n'))
        else:
            self.connection.write(str.encode(f"{command}\n"))
        socketio.emit('console', {"timestamp": datetime.datetime.now().strftime("%H:%M:%S"), 'command': command, 'class': htmlclass})
        response = self.connection.read_until(expected=b'ok\r\n').decode('utf-8')
        if htmlclass == 'systemquery':
            socketio.emit('console', {"timestamp": datetime.datetime.now().strftime("%H:%M:%S"), 'command': response, 'class': 'systemquery'})
        else:
            socketio.emit('console', {"timestamp": datetime.datetime.now().strftime("%H:%M:%S"), 'command': response, 'class': 'recive'})
        return response
        
    def GetGRBLSettings(self, socketio):
        self.settings = self.SendCommand('$$', socketio, 'systemsent')
        self.settings = self.settings.replace('\r', '').replace('ok\n', '') # Converts to a string then removes \r and confirmation from responses 
        self.settings = [i for i in self.settings.split('\n') if i]       # Removes Empty Strings from list after seperating newlines to a list (Due to the final \n at the end of the list it creates a empty string)
        
        # Convert list to dictionary
        self.settings = [parameter.split('=') for parameter in self.settings] # Split each string in settings floato a list containing the setting and its value
        self.settings = dict(self.settings)   # Convert to a dictionary
        return self.settings
    
    def StatusReport(self, socketio):

        response = self.SendCommand('?', socketio, 'systemquery').replace('<', '').replace('>\r\n', '').replace('ok\r\n', '').split('|')
        itemDict = {}
        for item in response:
            key_value_pair  = item.split(':')
            if key_value_pair[0] in ['Idle', 'Run', 'Hold', 'Jog', 'Alarm', 'Door', 'Check', 'Home', 'Sleep']:
                if len(key_value_pair) == 2:
                    self.status = key_value_pair[0]
                    self.subStatus = key_value_pair[1]
                    
                else:
                    self.status = key_value_pair[0]
                    self.subStatus = None
                    
            elif key_value_pair[0] == 'WPos':
                self.Wpos = list(map(float, key_value_pair[1].split(',')))
                self.Mpos = [self.Wpos[0] + self.WCO[0], self.Wpos[1] + self.WCO[1], self.Wpos[2] + self.WCO[2]]
                
            elif key_value_pair[0] == 'MPos':
                self.Mpos = list(map(float, key_value_pair[1].split(',')))
                self.Wpos = [self.Mpos[0] - self.WCO[0], self.Mpos[1] - self.WCO[1], self.Mpos[2] - self.WCO[2]]
                
            elif key_value_pair[0] == 'WCO':
                self.WCO = list(map(float, key_value_pair[1].split(',')))
                
            elif key_value_pair[0] == 'Ov':
                self.Ov = list(map(float, key_value_pair[1].split(',')))
                
            elif key_value_pair[0] == 'F':
                self.RealFeed = float(key_value_pair[1])
                
            elif key_value_pair[0] == 'FS':
                FS = key_value_pair[1].split(',')
                self.RealFeed = float(FS[0])
                self.RealSpindle = float(FS[1])
                
            elif key_value_pair[0] == 'Ln':
                self.LineNum = float(key_value_pair[1])

            elif key_value_pair[0] == 'Pn':
                self.triggeredPins = list(key_value_pair[1])
            
            elif key_value_pair[0] == 'A':
                self.accessoryState = list(key_value_pair[1])

        itemDict['Status'] = self.status
        itemDict['SubStatus'] = self.subStatus
        itemDict['WPos'] = self.Wpos
        itemDict['MPos'] = self.Mpos
        itemDict['WCO'] = self.WCO
        itemDict['Ov'] = self.Ov
        itemDict['RealFeed'] = self.RealFeed
        itemDict['Pn'] = self.triggeredPins
        itemDict['A'] = self.accessoryState
        itemDict['RealSpindle'] = self.RealSpindle
        return itemDict

    def Jog(self, socketio, disX, disY, disZ, feedrate):
        junk = self.SendCommand(f'$J=G91 G21 X{disX} Y{disY} Z{disZ} F{feedrate}', socketio, 'systemsent') 
        
    def adjustSpindle(self, socketio, desired):
        
        self.StatusReport(socketio)
        if desired == '100':
            self.SendCommand(b'\x99', socketio, 'systemsent')
        
        elif str(self.Ov[2]) == desired:
            return
        
        elif str(self.Ov[2]) < desired:
            iterations = int(desired) - int(self.Ov[2])
            for i in range(0, iterations):
                self.SendCommand(b'\x9C', socketio, 'systemsent')
                time.sleep(0.02)
            
        else:
            iterations = int(self.Ov[2]) - int(desired)
            for i in range(0, iterations):
                self.SendCommand(b'\x9D', socketio, 'systemsent')
                time.sleep(0.02)
                
    def Async(self, socketio, buffer):
        while True:
            if buffer != []:
                for command in buffer:
                    if command[0] == 'adjustSpindle':
                        self.adjustSpindle(socketio, command[1])
                    elif command[0] == 'SendCommand':
                        self.SendCommand(command[1], socketio, command[2])
                    elif command[0] == 'Jog':
                        self.Jog(socketio, command[1], command[2], command[3], command[4])
                    elif command[0] == 'StatusReport':
                        self.StatusReport(socketio)
                    buffer.remove(command)