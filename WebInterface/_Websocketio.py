from flask import request, jsonify
import time
import GRBLTools as grbl
import os
import helpers
from ._commons import app, STATE, scheduler, socketio, GRBL_COMMAND_BUFFER, GRBL

OPERATIONS = os.listdir('./OperationFiles')

@socketio.on('jog')
def Jog(data):
    GRBL_COMMAND_BUFFER.append(['Jog', [data['x'], data['y'], data['z'], data['f']]])
    
@socketio.on('zeroAxis')
def ZeroAxis(data):
    GRBL_COMMAND_BUFFER.append(['ZeroAxis', [data]])

@socketio.on('toggleMist')
def ToggleMist():
    GRBL_COMMAND_BUFFER.append(['ToggleMist', []])
    
@socketio.on('toggleFlood')
def ToggleFlood():
    GRBL_COMMAND_BUFFER.append(['ToggleFlood', []])

@socketio.on('sendconsole')
def sendconsole(data):
    GRBL_COMMAND_BUFFER.append(['SendCommand', [data]])
    
    
@socketio.on('home')
def homeAxis(data):
    GRBL_COMMAND_BUFFER.append(['Home', [data]])
    

@socketio.on('spindle')
def toggleSpindle(data):
    GRBL_COMMAND_BUFFER.append(['SpindleControl', [data]])
    
@socketio.on('move')
def Move(data):
    GRBL_COMMAND_BUFFER.append(['Move', [data]])
    
@socketio.on('spindleOveride')
def SpindleOveride(data):
    GRBL_COMMAND_BUFFER.append(['adjustSpindle', data])
    
@socketio.on('feedOveride')
def FeedOveride(data):
    GRBL_COMMAND_BUFFER.append(['adjustFeed', data])
    
@socketio.on('rapidOveride')
def RapidOveride(data):
    GRBL_COMMAND_BUFFER.append(['adjustRapid', data])

@socketio.on('GRBLconnect')
def Connect(data):
    GRBL.connect(data, 115200)
    scheduler.resume()
    STATE.STATE = 'Connected'
    GRBL.StartThreads()
    GRBL_COMMAND_BUFFER.append(['GetGRBLSettings'])
    
@socketio.on('GRBLdisconnect')
def Disconnect():
    GRBL.Async = False
    GRBL.connection.close()
    scheduler.pause()
    
    STATE.STATE = 'Disconnected'
    
@socketio.on('changeSetting')
def ChangeSetting(data):
    GRBL_COMMAND_BUFFER.append(['ChangeSetting', [data[0], data[1]]])
    
@socketio.on('connect')
def SendPorts():
    socketio.emit('USBPorts', helpers.getUSBPorts())
    socketio.emit('STATE', STATE.STATE)
    socketio.emit('operations', OPERATIONS)
    try:
        if GRBL.loadedFile != None:
            LoadFile(GRBL.loadedFile)
            socketio.emit('lineNum', [0, GRBL.fileLenght])
            socketio.emit('loadedFileName', GRBL.loadedFile)

        if GRBL.status == 'Operating':
            socketio.emit('operatingStartTime', GRBL.operationStartTime)
            socketio.emit('lineNum', [GRBL.linenum, GRBL.fileLenght])
            socketio.emit('operationTime', time.time() - GRBL.operationStartTime)
    except:
        socketio.emit('ETA', 0)
        socketio.emit('loadedFileName', None)
        socketio.emit('lineNum', [0, 0])
        socketio.emit('loadedFile', [''])
        socketio.emit('operationTime', 0)
        
@socketio.on('start')
def StartCycle(data):
    print(data)
    GRBL_COMMAND_BUFFER.append(['SendCommand', ['~']])
    if GRBL.status != 'Operating':
        GRBL_COMMAND_BUFFER.append(['StartOperation', data])

@socketio.on('loadFile')
def LoadFile(data):
    GRBL.LoadFile(data)
    with open(f'./OperationFiles/{data}') as file:
        socketio.emit('loadedFile', file.readlines())

@socketio.on('deleteFile')
def DeleteFile(data):
    os.remove(f'./OperationFiles/{data}')
    OPERATIONS = os.listdir('./OperationFiles')
    socketio.emit('operations', OPERATIONS)

@socketio.on('ESTOP')
def ESTOP():
    print('ESTOP!!!!')
    GRBL.SendCommand(b'\x18')

@socketio.on('unlockAlarm')
def Unlock():
    GRBL.SendCommand('$X')
    
@socketio.on('unloadStopOperation')
def UnloadStopOperation():
    GRBL.KILLOPERATION = True
    GRBL.LoadFile(None)
    socketio.emit('loadedFile', [''])
    GRBL.SendCommand('!')
    time.sleep(0.5)
    GRBL.SendCommand(b'\x18')
    GRBL.status = 'Idle'
    socketio.emit('operationTime', 0)
    
@socketio.on('holdOperation')
def HoldOperation():
    GRBL.SendCommand('!')
    
@socketio.on('pauseOperation')
def PauseOperation():
    GRBL.SendCommand('!')
    GRBL.SendCommand(b'\x9E')