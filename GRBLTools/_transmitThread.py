import time
import threading
from ._fileTransmission import SendFile

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
            prossesSend(self, buffer)
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
                    thread = threading.Thread(target=SendFile, args=(self, f'./OperationFiles/{command[1]}','Reliable', buffer), daemon=True)
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