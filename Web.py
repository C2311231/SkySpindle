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
    GRBL_COMMAND_BUFFER.append(['Jog', [data['x'], data['y'], data['z'], 1000]])
    
    
@socketio.on('sendconsole')
def fili(data):
    GRBL_COMMAND_BUFFER.append(['SendCommand', [data, 'user']])
    
    
@socketio.on('home')
def file(data):
    GRBL_COMMAND_BUFFER.append(['SendCommand', [f'$H{data}', 'systemsent']])
    

@socketio.on('spindle')
def filr(data):
    GRBL_COMMAND_BUFFER.append(['SendCommand', [f'M03 S{data}', 'systemsent']])
    
@scheduler.task('interval', id='GetSettings', seconds=5, max_instances=5)
def SendPositionData():
    OPERATIONS = os.listdir('./OperationFiles')
    if GRBL.status == 'Idle':
        GRBL_COMMAND_BUFFER.append(['GetGRBLSettings'])
    socketio.emit('settings', GRBL.settings)
    socketio.emit('State', State)
    socketio.emit('operations', OPERATIONS)


@scheduler.task('interval', id='GetPos', seconds=0.3, max_instances=5)
def SendPositionData():
    socketio.emit('positionM', GRBL.Mpos)
    socketio.emit('positionW', GRBL.Wpos)
    
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
    GRBLthread1.join()
    GRBLthread2.join()
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
    GRBL_COMMAND_BUFFER.append(['StartOperation', data])



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


def SendData(Name, data):
    socketio.emit(Name, data)





if __name__ == "__main__":
    scheduler.start()
    scheduler.pause()
    OPERATIONS = os.listdir('./OperationFiles')
    socketio.run(app, debug=True, use_reloader=False)
