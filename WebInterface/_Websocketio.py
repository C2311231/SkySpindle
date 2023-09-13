from flask import request, jsonify
import time
import GRBLTools as grbl
import os
import helpers
from ._commons import app, STATE, scheduler, socketio, GRBL_COMMAND_BUFFER, GRBL

OPERATIONS = os.listdir('./OperationFiles')

@socketio.on('Jog')
def Jog(data):
    GRBL_COMMAND_BUFFER.append(['Jog', [data['x'], data['y'], data['z'], data['f']]])
    
@socketio.on('ZeroAxis')
def ZeroAxis(data):
    GRBL_COMMAND_BUFFER.append(['ZeroAxis', [data]])

@socketio.on('ToggleMist')
def ToggleMist():
    GRBL_COMMAND_BUFFER.append(['ToggleMist', []])
    
@socketio.on('ToggleFlood')
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
    
@socketio.on('Move')
def Move(data):
    GRBL_COMMAND_BUFFER.append(['Move', [data]])
    
@socketio.on('SpindleOveride')
def SpindleOveride(data):
    GRBL_COMMAND_BUFFER.append(['adjustSpindle', data])
    
@socketio.on('FeedOveride')
def FeedOveride(data):
    GRBL_COMMAND_BUFFER.append(['adjustFeed', data])
    
@socketio.on('RapidOveride')
def RapidOveride(data):
    GRBL_COMMAND_BUFFER.append(['adjustRapid', data])

@socketio.on('Connect')
def Connect(data):
    GRBL.connect(data, 115200)
    scheduler.resume()
    STATE.STATE = 'Connected'
    GRBL.StartThreads()
    GRBL_COMMAND_BUFFER.append(['GetGRBLSettings'])
    
@socketio.on('Disconnect')
def Disconnect():
    GRBL.Async = False
    GRBL.connection.close()
    scheduler.pause()
    
    STATE.STATE = 'Disconnected'
    
@socketio.on('ChangeSetting')
def ChangeSetting(data):
    GRBL_COMMAND_BUFFER.append(['ChangeSetting', [data[0], data[1]]])
    
@socketio.on('connect')
def SendPorts():
    socketio.emit('USBPorts', helpers.getUSBPorts())
    
    socketio.emit('STATE', STATE.STATE)
    socketio.emit('operations', OPERATIONS)
    try:
        if GRBL.loadedFile != None:
            socketio.emit('ETA', GRBL.OperationETA)
            LoadFile(GRBL.loadedFile)
            socketio.emit('LineNum', [0, GRBL.fileLenght])
            socketio.emit('LoadedFileName', GRBL.loadedFile)

        if GRBL.status == 'Operating':
            socketio.emit('OperatingStartTime', GRBL.operationStartTime)
            socketio.emit('LineNum', [GRBL.linenum, GRBL.fileLenght])
            socketio.emit('operationTime', time.time() - GRBL.operationStartTime)
    except:
        socketio.emit('ETA', 0)
        socketio.emit('LoadedFileName', None)
        socketio.emit('LineNum', [0, 0])
        socketio.emit('LoadedFile', [''])
        socketio.emit('operationTime', 0)
        
@socketio.on('Start')
def StartCycle(data):
    print(data)
    GRBL_COMMAND_BUFFER.append(['SendCommand', ['~']])
    if GRBL.status != 'Operating':
        GRBL_COMMAND_BUFFER.append(['StartOperation', data])

@socketio.on('LoadFile')
def LoadFile(data):
    GRBL.LoadFile(data)
    with open(f'./OperationFiles/{data}') as file:
        socketio.emit('LoadedFile', file.readlines())

@socketio.on('DeleteFile')
def DeleteFile(data):
    os.remove(f'./OperationFiles/{data}')
    OPERATIONS = os.listdir('./OperationFiles')
    socketio.emit('operations', OPERATIONS)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file:
        filename = uploaded_file.filename
        uploaded_file.save(os.path.join('OperationFiles', filename))
        OPERATIONS = os.listdir('./OperationFiles')
        socketio.emit('operations', OPERATIONS)
        return jsonify(message='File uploaded successfully.')
    return jsonify(message='No file uploaded.'), 400

@socketio.on('ESTOP')
def ESTOP():
    print('ESTOP!!!!')
    GRBL.SendCommand(b'\x18')

@socketio.on('UNLOCKALARM')
def Unlock():
    GRBL.SendCommand('$X')
    
@socketio.on('unloadStopOperation')
def UnloadStopOperation():
    GRBL.KILLOPERATION = True
    GRBL.LoadFile(None)
    socketio.emit('LoadedFile', [''])
    GRBL.SendCommand('!')
    time.sleep(0.5)
    GRBL.SendCommand(b'\x18')
    GRBL.status = 'Idle'
    socketio.emit('operationTime', 0)
    
@socketio.on('HoldOperation')
def HoldOperation():
    GRBL.SendCommand('!')
    
@socketio.on('PauseOperation')
def PauseOperation():
    GRBL.SendCommand('!')
    GRBL.SendCommand(b'\x9E')