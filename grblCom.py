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
        self.Wpos = [0, 0, 0]
        self.SocketEmit = SendData
        self.okCount = 0
        self.receive = []
        self.settings = {}
        self.requested = 0
        self.status = 'Idle'
        self.subStatus = None
        self.Machinestatus = None
        self.linenum = 0
        
    def SendCommand(self, command, Class='systemsent'):
        
        if isinstance(command, bytes):
            self.SocketEmit('console', {'data': command.decode(encoding='unicode_escape'), 'class': Class})
            self.connection.write(command)
        else:
            self.SocketEmit('console', {'data': command, 'class': Class})
            self.connection.write(str.encode(f"{command}\n"))
        
        
    def GetGRBLSettings(self):
        self.SendCommand('$$')
        
    def processGRBLSettings(self, data):
        data = data.split('=') # Converts to a string then removes \r and confirmation from responses 
        
        self.settings[data[0]] = data[1]
        
    def StatusReportProcess(self, response):
        response = response.replace('<', '').replace('>', '').split('|')
        for item in response:
            if 'Idle' in item or 'Run' in item or 'Hold' in item or 'Jog' in item or 'Alarm' in item or 'Door' in item or 'Check' in item or 'Home' in item or 'Sleep' in item:
                if ':' in item:
                    self.Machinestatus, self.subStatus = item.split(':')
                    
                else:
                    self.Machinestatus = item
                    self.subStatus = None
            elif 'A' in item:
                self.accessoryState = list(item)                    #OPTIMIZE with .startswith()
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
                

                
    def Jog(self, disX, disY, disZ, feedrate):
        self.SendCommand(f'$J=G91 G21 X{disX} Y{disY} Z{disZ} F{feedrate}\n') 
        
        
    def adjustSpindle(self, desired):
        if desired == '100':
            self.SendCommand(b'\x99\n')
        elif str(self.Ov[2]) == desired:
            return
        elif int(self.Ov[2]) < int(desired):
            iterations = int(desired) - int(self.Ov[2])
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x9A\n')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x9C\n')
                time.sleep(0.02)
        else:
            iterations = int(self.Ov[2]) - int(desired)
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x9B\n')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x9D\n')
                time.sleep(0.02)
                
                
    def adjustFeed(self, desired):
        if desired == '100':
            self.SendCommand(b'\x90\n')
        elif str(self.Ov[0]) == desired:
            return
        elif int(self.Ov[0]) < int(desired):
            iterations = int(desired) - int(self.Ov[0])
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x91\n')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x93\n')
                time.sleep(0.02)
        else:
            iterations = int(self.Ov[0]) - int(desired)
            for i in range(0, int(iterations/10)):
                self.SendCommand(b'\x92\n')
                time.sleep(0.02)
            for i in range(0, int(iterations%10)):
                self.SendCommand(b'\x94\n')
                time.sleep(0.02)
                
                
    def adjustRapid(self, value):
        if value == '100':
            self.SendCommand(b'\x95\n')
        elif value == '50':
            self.SendCommand(b'\x96\n')
        else:
            self.SendCommand(b'\x97\n')
            
            
    def ChangeSetting(self, setting, value):
        print(f'{setting}={value}')
        self.SendCommand(f'{setting}={value}')
        
        

    def stop_thread(self):
        self.Async=False
        
        
    def SendFile(self, filePath, mode, buffer):
        self.status = 'Operating'
        file = open(filePath, 'r')
        file = file.readlines()
        self.linenum = 1
        self.fileLenght = len(file)
        if mode == 'Fast':               # NONFUNCTIONAL
            linesCharactorCounts = []
            RX_BUFFER_SIZE = 100
            GCodeCount = 0
            linesInBuffer = 0
            for line in file:
                self.Async = False
                line = re.sub(r'\s|\(.*?\)', '', line).upper().strip()
                line = line +f'N{self.linenum}'
                linesCharactorCounts.append(len(line)+1)
                print(f'charactorcount = {sum(linesCharactorCounts)}')
                while sum(linesCharactorCounts) >= RX_BUFFER_SIZE - 1 or self.connection.in_waiting:
                    returnData = self.connection.readline().decode()
                    print('recived ' + returnData)
                    returnData = returnData.strip()
                    if 'error' in returnData:
                        print(f'GRBL Reports Error on line {self.linenum-linesInBuffer}:   {returnData}')
                        return
                    elif 'echo' not in line:
                        GCodeCount +=1
                        linesInBuffer -= 1
                        if linesCharactorCounts:
                            del linesCharactorCounts[0]
                
                self.connection.write((line + '\n').encode())
                linesInBuffer += 1
                self.linenum += 1
                
                
        if mode == 'Reliable':
            self.notSending = False
            self.requested = 0
            self.okCount = 0
            for line in file:
                self.notSending = False
                l = line.strip() # Strip all EOL characters for consistency
                buffer.append(["FileCommand", (l + f' N{self.linenum}\n').encode()]) # Send g-code block to grbl
                self.requested += 1
                while self.requested > self.okCount:
                    self.notSending = True
                    time.sleep(0.3)
                self.linenum += 1
                self.SocketEmit('LineNum', [self.linenum, self.fileLenght])
        self.status = 'Idle'
    def Async(self, buffer):
        self.Async=True
        self.notSending = True
        self.lastPosTime = time.time()
        while self.Async:
            if self.Async == False:
                break
            if self.notSending:
                if time.time() - 0.3 > self.lastPosTime:
                    self.SendCommand(b'?', Class='status')
                    self.lastPosTime = time.time()
                self.prossesSend(buffer)
            time.sleep(0.2)
            
            
    def prossesSend(self, buffer):       
        if buffer != []:
            commands = buffer
            for command in commands:
                self.requested += 1
                if command[0] == 'adjustSpindle':
                    self.adjustSpindle(command[1])
                elif command[0] == 'FileCommand':
                    self.requested -= 1
                    self.SendCommand(command[1])
                elif command[0] == 'adjustFeed':
                    self.adjustFeed(command[1])
                elif command[0] == 'SendCommand':
                    self.SendCommand(command[1][0], 'userSent')
                elif command[0] == 'StatusReport':
                    self.requested -= 1
                    self.SendCommand(b'?', Class='status')
                elif command[0] == 'Jog':
                    self.Jog(command[1][0], command[1][1], command[1][2], command[1][3])
                elif command[0] == 'adjustRapid':
                    self.adjustRapid(command[1])
                elif command[0] == 'GetGRBLSettings':
                    if self.status == 'Idle':
                        self.requested -= 1
                        self.GetGRBLSettings()
                elif command[0] == 'ChangeSetting':
                    self.ChangeSetting(command[1][0], command[1][1])
                elif command[0] == 'StartOperation':
                    self.requested -= 1
                    if self.status == 'Idle':
                        thread = threading.Thread(target=self.SendFile, args=(f'./OperationFiles/{command[1]}','Reliable', buffer), daemon=True)
                        thread.start()
                elif command[0] == 'Home':
                     self.SendCommand(f'$H{command[1][0]}')
                elif command[0] == 'SpindleControl':
                     self.SendCommand(f'M03 S{command[1][0]}')
                elif command[0] == 'ZeroAxis':
                    axis = ''
                    for item in command[1][0]:
                        axis = axis + f'{item}0'
                    self.SendCommand(f'G10 L20 P1 {axis}')
                elif command[0] == 'ToggleMist':
                    self.SendCommand(b'\xA1\n')
                elif command[0] == 'ToggleFlood':
                    self.SendCommand(b'\xA0\n')
                elif command[0] == 'Move':
                    self.SendCommand(f'$J=G90 G21 {command[1][0]}\n')
                    
                buffer.remove(command)
        
    def GetData(self):
        while self.Async:
            line = self.connection.readline().decode().strip()
            if self.Async == False:
                break
            
            if line.startswith('<') and line.endswith('>'):
                self.StatusReportProcess(line)
                self.SocketEmit('console', {'data': line, 'class': 'status'})
                
            elif line.startswith('ok'):
                self.okCount += 1 
                self.SocketEmit('console', {'data': line, 'class': 'recive'})   
            
            elif line.startswith('$') and '=' in line:
                self.SocketEmit('console', {'data': line, 'class': 'recive'})   
                if 'N' not in line:
                    self.processGRBLSettings(line)
                else:
                    data = line.replace('$N', '').split('=')
                    self.startuplines[data[0]] = data[1]
                
            elif line.startswith('[') and line.endswith(']'):
                self.SocketEmit('console', {'data': line, 'class': 'recive'})   
                if 'MSG:' in line:
                    print(f'GRBL sent a message: {line}')
                    
                elif 'GC:' in line:
                    self.GcodeParserState = line.replace(']', '').replace('[GC:', '').split(' ')
                
                elif 'VER:' in line:
                    self.Version = line.replace(':]', '').replace('[VER:', '')
                elif 'OPT:' in line:
                    self.OPT = line.replace(']', '').replace('[OPT:', '')
                elif 'echo:' in line:
                    pass
                elif 'G54' in line or'G55' in line or'G56' in line or'G57' in line or'G58' in line or'G59' in line or'G28' in line or'G30' in line or'G92' in line or'TLO' in line or'PRB' in line:
                    self.SP[line.split(':')[0].replace(':', '').replace('[', '')] = line.split(':')[1].replace(']', '').split(',')
                    
            elif line.startswith('ALARM'):
                print(f'GRBL reports an alarm: {line}')
                self.SocketEmit('console', {'data': line, 'class': 'recive'})   
            elif line.startswith('>'):
                data = line.replace(">", '').split(':')
                if data[1] != 'ok':
                    print(f'Start line failed {data[0]}')
                self.SocketEmit('console', {'data': line, 'class': 'recive'})   
            elif line.startswith('Grbl'):
                self.SocketEmit('console', {'data': line, 'class': 'recive'})
            elif line.startswith('error'):
                self.SocketEmit('console', {'data': line, 'class': 'reciveError'})
                print(f'GRBL reports an error: {line}')
            if self.connection.in_waiting < 15:
                time.sleep(0.05)