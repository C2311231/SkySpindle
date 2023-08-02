from flask import Flask, render_template
from flask_socketio import SocketIO
import grblCom
from flask_apscheduler import APScheduler
import threading

app = Flask(__name__)
app.secret_key = 'key123'
socketio = SocketIO(app)
running = False

scheduler = APScheduler()
scheduler.init_app(app)

GRBL_COMMAND_BUFFER = []

@app.route('/')
def home():
    return render_template('layout.html')



@socketio.on('Jog')
def fil(data):
    GRBL_COMMAND_BUFFER.append(['Jog', data['x'], data['y'], data['z'], 1000])
    
    
@socketio.on('sendconsole')
def fili(data):
    GRBL_COMMAND_BUFFER.append(['SendCommand', data, 'user'])
    
    
@socketio.on('home')
def file(data):
    GRBL_COMMAND_BUFFER.append(['SendCommand', f'$H{data}', 'systemsent'])
    

@socketio.on('spindle')
def filr(data):
    GRBL_COMMAND_BUFFER.append(['SendCommand', f'M03 S{data}', 'systemsent'])
    

@scheduler.task('interval', id='GetPos', seconds=0.3, max_instances=5)
def SendPositionData():
    GRBL_COMMAND_BUFFER.append(['StatusReport'])
    socketio.emit('position', GRBL.Mpos)
    
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
    global GRBLthread
    GRBL = grblCom.GRBLConection(data, 115200)
    scheduler.resume()
    GRBLthread = GRBLthread = threading.Thread(target=GRBL.Async, args=(socketio, GRBL_COMMAND_BUFFER), daemon=True)
    GRBLthread.start()
@socketio.on('Disconnect')
def Disconnect():
    GRBL.stop_thread()
    GRBLthread.join()
    GRBL.connection.close()
    scheduler.pause()
    
    
@socketio.on('connect')
def SendPorts(data):
    socketio.emit('USBPorts', grblCom.getUSBPorts())

if __name__ == "__main__":
    scheduler.start()
    scheduler.pause()
    socketio.run(app, debug=True, use_reloader=False)
