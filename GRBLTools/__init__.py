import serial
import time
import threading
from ._receiveThread import GetData
from ._transmitThread import Async

class GRBLConection():
    def __init__(self, SendData, GRBL_COMMAND_BUFFER):
        self.connection = serial.Serial()
        self.GRBL_COMMAND_BUFFER = GRBL_COMMAND_BUFFER
        
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
        self.OperationETA = 0
        
        
    def connect(self, port, baudrate):
        self.connection.port = port
        self.connection.baudrate = baudrate
        self.connection.open()
        print('Opening Serial Port')
        self.connection.write(str.encode("\r\n\r\n")) # Wake up GRBL Connection
    
    def SendCommand(self, command, Class='systemsent'):
        
        if isinstance(command, bytes):
            self.SocketEmit('console', {'data': command.decode(encoding='unicode_escape'), 'class': Class})
            self.connection.write(command)
        else:
            self.SocketEmit('console', {'data': command, 'class': Class})
            self.connection.write(str.encode(f"{command}\n"))
        
        
    def GetGRBLSettings(self):
        self.SendCommand('$$')
                
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

    def LoadFile(self, file):
        self.loadedFile = file
        if self.loadedFile != None:
            with open(f'./OperationFiles/{file}') as file:
                file = file.readlines()
                self.fileLenght = len(file)
            self.SocketEmit('LoadedFileName', self.loadedFile)
            self.SocketEmit('LineNum', [0, self.fileLenght])
        else:
            self.fileLenght = 0
            self.OperationETA = 0
            self.SocketEmit('ETA', 0)
            self.SocketEmit('LoadedFileName', self.loadedFile)
            self.SocketEmit('LineNum', [0, self.fileLenght])
    
    def StartThreads(self):
        self.thread1 = threading.Thread(target=GetData, args=(self,), daemon=True)
        self.thread2 = threading.Thread(target=Async, args=(self, self.GRBL_COMMAND_BUFFER,), daemon=True)
        self.thread1.start()
        self.thread2.start()