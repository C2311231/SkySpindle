import serial
import serial.tools.list_ports
import time
import datetime
import threading
import re


def getUSBPorts():
    comPorts = serial.tools.list_ports.comports()
    ports = []
    for port in comPorts:
        ports.append(port.device)
    return ports

class GRBLConection():
    def __init__(self, port, baudrate, SendData):
        self.connection = serial.Serial(port, baudrate)
        print('Opening Serial Port')
        self.connection.write(str.encode("\r\n\r\n")) # Wake up GRBL Connection
        
        # Default Values
        self.WCO = [0,0,0]
        self.Ov = [100, 100, 100]
        self.RealFeed = 0
        self.RealSpindle = 0
        self.triggeredPins = None
        self.accessoryState = None
        self.Mpos = [0, 0, 0]
        self.SocketEmit = SendData
        self.okCount = 0
        self.receive = []
        self.settings = {}
        self.requested = 0
        self.allowtransmit = True
        
    def SendCommand(self, command):
        if isinstance(command, bytes):
            self.connection.write(command)
            self.connection.write(str.encode('\n'))
        else:
            self.connection.write(str.encode(f"{command}\n"))
        
        
    def GetGRBLSettings(self):
        self.SendCommand('$$')
        
    def processGRBLSettings(self, data):
        data = data.split('=') # Converts to a string then removes \r and confirmation from responses 
        if data[0] not in self.settings:
            self.settings[data[0]] = data[1]
        
    def StatusReportProcess(self, response):
        response = response.replace('<', '').replace('>', '').split('|')
        for item in response:
            if 'Idle' in item or 'Run' in item or 'Hold' in item or 'Jog' in item or 'Alarm' in item or 'Door' in item or 'Check' in item or 'Home' in item or 'Sleep' in item:
                if ':' in item:
                    self.status, self.subStatus = item.split(':')
                    
                else:
                    self.status = item
                    self.subStatus = None
                    
            elif 'FS' in item:
                FS = item.replace('FS:', '').split(',')
                self.RealFeed = float(FS[0])
                self.RealSpindle = float(FS[1])
                
            elif 'F' in item:
                self.RealFeed = float(item.replace('F:', ''))
                
            elif 'WPos' in item:
                value = item.replace('WPos:', '')
                self.Wpos = list(map(float, value.split(',')))
                self.Mpos = [self.Wpos[0] + self.WCO[0], self.Wpos[1] + self.WCO[1], self.Wpos[2] + self.WCO[2]]
                
            elif 'MPos' in item:
                value = item.replace('MPos:', '')
                self.Mpos = list(map(float, value.split(',')))
                self.Wpos = [self.Mpos[0] - self.WCO[0], self.Mpos[1] - self.WCO[1], self.Mpos[2] - self.WCO[2]]
                
            elif 'WCO' in item:
                value = item.replace('WCO:', '')
                self.WCO = list(map(float, value.split(',')))
                
            elif 'Ov' in item:
                value = item.replace('Ov:', '')
                self.Ov = list(map(float, value.split(',')))
                self.SocketEmit('Overides', self.Ov)
                
            elif 'Ln' in item:
                self.LineNum = int(item)
                
            elif 'Pn' in item:
                self.triggeredPins = list(item)
                
            elif 'A' in item:
                self.accessoryState = list(item)
                
    def Jog(self, disX, disY, disZ, feedrate):
        self.SendCommand(f'$J=G91 G21 X{disX} Y{disY} Z{disZ} F{feedrate}\n') 
        
        
    def adjustSpindle(self, desired):
        if desired == '100':
            self.SendCommand(b'\x99')
        elif str(self.Ov[2]) == desired:
            return
        elif int(self.Ov[2]) < int(desired):
            iterations = int(desired) - int(self.Ov[2])
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x9A')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x9C')
                time.sleep(0.02)
        else:
            iterations = int(self.Ov[2]) - int(desired)
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x9B')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x9D')
                time.sleep(0.02)
                
                
    def adjustFeed(self, desired):
        if desired == '100':
            self.SendCommand(b'\x90')
        elif str(self.Ov[0]) == desired:
            return
        elif int(self.Ov[0]) < int(desired):
            iterations = int(desired) - int(self.Ov[0])
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x91')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x93')
                time.sleep(0.02)
        else:
            iterations = int(self.Ov[0]) - int(desired)
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x92')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x94')
                time.sleep(0.02)
                
                
    def adjustRapid(self, value):
        if value == '100':
            self.SendCommand(b'\x95')
        elif value == '50':
            self.SendCommand(b'\x96')
        else:
            self.SendCommand(b'\x97')
            
            
    def ChangeSetting(self, setting, value):
        self.SendCommand(f'{setting}={value}')
        
        

    def stop_thread(self):
        self.Async=False
        
        
    def SendFile(self, filePath, mode):
        time.sleep(0.5)
        file = open(filePath, 'r')
        i = 0
        if mode == 'Fast':               # NONFUNCTIONAL
            linesCharactorCounts = []
            RX_BUFFER_SIZE = 128
            GCodeCount = 0
            linesInBuffer = 0
            for line in file:
                
                line = re.sub(r'\s|\(.*?\)', '', line).upper().strip()
                print(line)
                linesCharactorCounts.append(len(line)+1)
                print(f'charactorcount = {sum(linesCharactorCounts)}')
                while sum(linesCharactorCounts) >= RX_BUFFER_SIZE - 1 or self.connection.in_waiting:
                    returnData = self.connection.readline().strip()
                    print(returnData)
                    if b'error' in returnData:
                        print(f'GRBL Reports Error on line {i-linesInBuffer}:   {returnData}')
                        return
                    else:
                        GCodeCount +=1
                        linesInBuffer -= 1
                        print(linesCharactorCounts)
                        if linesCharactorCounts:
                            del linesCharactorCounts[0]
                i += 1
                self.SendCommand((line + '\n').encode())
                linesInBuffer += 1
                
                
        if mode == 'Reliable':
            self.requested = 0
            self.receiveCounter = 0
            for line in file:
                self.allowtransmit = False
                print(line)
                l = line.strip() # Strip all EOL characters for consistency
                self.SendCommand(l + f' N{i}\n') # Send g-code block to grbl
                self.requested += 1
                while self.requested > self.receiveCounter:
                    self.allowtransmit = True
                    time.sleep(0.03)
                i += 1
    
    def Async(self, buffer):
        self.Async=True
        while self.Async:
            if buffer != [] and self.allowtransmit:
                commands = buffer
                
                for command in commands:
                    self.requested += 1
                    if command[0] == 'adjustSpindle':
                        self.adjustSpindle(command[1])
                    elif command[0] == 'adjustFeed':
                        self.adjustFeed(command[1])
                    elif command[0] == 'SendCommand':
                        self.connection.write(command[1])
                    elif command[0] == 'StatusReport':
                        self.SendCommand(b'?\n')
                    elif command[0] == 'Jog':
                        self.Jog(command[1][0], command[1][1], command[1][2], command[1][3])
                    elif command[0] == 'adjustRapid':
                        self.adjustRapid(command[1])
                    elif command[0] == 'GetGRBLSettings':
                        self.requested += 33
                        self.GetGRBLSettings()
                    elif command[0] == 'ChangeSetting':
                        self.ChangeSetting(command[1][0], command[1][1])
                    elif command[0] == 'StartOperation':
                        self.status = 'Operating'
                        self.filethread = threading.Thread(target=self.SendFile, args=(f'./OperationFiles/{command[1]}','Reliable'), daemon=True).start()
                    buffer.remove(command)
            time.sleep(0.2)
            
        
    def GetData(self):
        self.receiveCounter = 0
        while self.Async:
            line = self.connection.readline().decode().strip()
            if self.Async == False:
                break
            
            self.SocketEmit('console', line)
            self.receiveCounter += 1
            if line.startswith('<') and line.endswith('>'):

                self.StatusReportProcess(line)
                
            elif line.startswith('ok'):
                self.okCount += 1 
            
            elif line.startswith('$') and '=' in line:
                if 'N' not in line:
                    self.processGRBLSettings(line)
                else:
                    data = line.replace('$N', '').split('=')
                    self.startuplines[data[0]] = data[1]

            elif line.startswith('error'):
                print(f'GRBL reports an error: {line}')
                
            elif line.startswith('[') and line.endswith(']'):
                
                if 'MSG:' in line:
                    self.receiveCounter -= 1
                    print(f'GRBL sent a message: {line}')
                    
                elif 'GC:' in line:
                    self.GcodeParserState = line.replace(']', '').replace('[GC:', '').split(' ')
                
                elif 'VER:' in line:
                    self.Version = line.replace(':]', '').replace('[VER:', '')
                elif 'OPT:' in line:
                    self.OPT = line.replace(']', '').replace('[OPT:', '')
                elif 'echo:' in line:
                    self.receiveCounter -= 1
                elif 'G54' in line or'G55' in line or'G56' in line or'G57' in line or'G58' in line or'G59' in line or'G28' in line or'G30' in line or'G92' in line or'TLO' in line or'PRB' in line:
                    self.SP[line.split(':')[0].replace(':', '').replace('[', '')] = line.split(':')[1].replace(']', '').split(',')
                    
            elif line.startswith('ALARM'):
                print(f'GRBL reports an alarm: {line}')
                
            elif line.startswith('>'):
                self.receiveCounter -= 1
                data = line.replace(">", '').split(':')
                if data[1] != 'ok':
                    print(f'Start line failed {data[0]}')
                
            elif line.startswith('Grbl'):
                self.receiveCounter -= 1
            if self.connection.in_waiting < 15:
                time.sleep(0.05)