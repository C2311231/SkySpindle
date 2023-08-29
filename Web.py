from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import grblCom
from flask_apscheduler import APScheduler
import threading
import os
import yaml
import csv

SettingsData = []

with open("./data/setting_codes_en_US.csv", "r") as f:
    data = csv.DictReader(f)
    for item in data:
        SettingsData.append(item)

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

app = Flask(__name__)
app.secret_key = 'key123'
socketio = SocketIO(app)
State = 'Disconnected'


scheduler = APScheduler()
scheduler.init_app(app)

GRBL_COMMAND_BUFFER = []
OPERATIONS = []


@app.route('/')
def home():
    return render_template('layout.html', SettingsData=SettingsData)

@socketio.on('Jog')
def fil(data):
    GRBL_COMMAND_BUFFER.append(['Jog', [data['x'], data['y'], data['z'], data['f']]])
    
@socketio.on('ZeroAxis')
def ZeroAxis(data):
    GRBL_COMMAND_BUFFER.append(['ZeroAxis', [data]])

@socketio.on('ToggleMist')
def ToggleMist():
    GRBL_COMMAND_BUFFER.append(['ToggleMist', []])
    
@socketio.on('ToggleFlood')
def ZeroAxis():
    GRBL_COMMAND_BUFFER.append(['ToggleFlood', []])

@socketio.on('sendconsole')
def fili(data):
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
    
@scheduler.task('interval', id='SlowUpdate', seconds=5, max_instances=1)
def SlowUpdate():
    OPERATIONS = os.listdir('./OperationFiles')
    socketio.emit('settings', GRBL.settings)
    global State
    socketio.emit('State', State)
    socketio.emit('operations', OPERATIONS)


@scheduler.task('interval', id='GetSettings', seconds=20, max_instances=1)
def UpdateSettings():
    if GRBL.status == 'Idle':
        GRBL_COMMAND_BUFFER.append(['GetGRBLSettings'])

@scheduler.task('interval', id='GetPos', seconds=0.3, max_instances=5)
def SendPositionData():
    mpos = []
    wpos = []
    for item in GRBL.Mpos:
        mpos.append(round(item, 3))
    for item in GRBL.Wpos:
        wpos.append(round(item, 3))
    socketio.emit('positionM', mpos)
    socketio.emit('positionW', wpos)
    if GRBL.subStatus:
        socketio.emit('Machine Status', f'Status: {GRBL.Machinestatus}:{GRBL.subStatus}')
    else:
        socketio.emit('Machine Status', f'Status: {GRBL.Machinestatus}')
    
@socketio.on('SpindleOveride')
def filr(data):
    GRBL_COMMAND_BUFFER.append(['adjustSpindle', data])
    
@socketio.on('FeedOveride')
def filr(data):
    GRBL_COMMAND_BUFFER.append(['adjustFeed', data])
    
@socketio.on('RapidOveride')
def filr(data):
    GRBL_COMMAND_BUFFER.append(['adjustRapid', data])

@socketio.on('Connect')
def Connect(data):
    global GRBL
    global GRBLthread1
    global GRBLthread2
    GRBL = grblCom.GRBLConection(data, 115200, SendData)
    scheduler.resume()
    GRBLthread1 = threading.Thread(target=GRBL.Async, args=(GRBL_COMMAND_BUFFER,), daemon=True)
    GRBLthread2 = threading.Thread(target=GRBL.GetData, args=(), daemon=True)
    GRBLthread1.start()
    GRBLthread2.start()
    global State
    State = 'Connected'
    GRBL_COMMAND_BUFFER.append(['GetGRBLSettings'])
    
@socketio.on('Disconnect')
def Disconnect():
    GRBL.stop_thread()
    GRBL.connection.close()
    scheduler.pause()
    global State
    State = 'Disconnected'
    
@socketio.on('ChangeSetting')
def ChangeSetting(data):
    GRBL_COMMAND_BUFFER.append(['ChangeSetting', [data[0], data[1]]])
    
@socketio.on('connect')
def SendPorts(data):
    socketio.emit('USBPorts', grblCom.getUSBPorts())
    socketio.emit('State', State)
    socketio.emit('operation', {'filename': OPERATIONS})

@socketio.on('Start')
def StartCycle(data):
    print(data)
    GRBL_COMMAND_BUFFER.append(['StartOperation', data])

@socketio.on('LoadFile')
def LoadFile(data):
    with open(f'./OperationFiles/{data}') as file:
        socketio.emit('LoadedFile', file.readlines())

@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files)
    uploaded_file = request.files['file']
    if uploaded_file:
        filename = uploaded_file.filename
        uploaded_file.save(os.path.join('OperationFiles', filename))
        OPERATIONS = os.listdir('./OperationFiles')
        socketio.emit('operations', OPERATIONS)
        return jsonify(message='File uploaded successfully.')
    return jsonify(message='No file uploaded.'), 400


def SendData(Name, data):
    socketio.emit(Name, data)

@socketio.on('ESTOP')
def ESTOP():
    print('ESTOP!!!!')
    GRBL.SendCommand(b'\x18')

if __name__ == "__main__":
    scheduler.start()
    scheduler.pause()
    OPERATIONS = os.listdir('./OperationFiles')
    socketio.run(app, debug=True, use_reloader=False)
