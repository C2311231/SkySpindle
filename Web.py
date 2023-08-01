from flask import Flask, render_template
from flask_socketio import SocketIO
import grblCom
from flask_apscheduler import APScheduler
app = Flask(__name__)
app.secret_key = 'key123'
socketio = SocketIO(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route('/')
def home():
    return render_template('layout.html')



@socketio.on('Jog')
def fil(data):
    scheduler.pause()
    GRBL.Jog(socketio, data['x'], data['y'], data['z'], 1000)
    scheduler.resume()
    
@socketio.on('sendconsole')
def fili(data):
    scheduler.pause()
    GRBL.SendCommand(data, socketio, 'user')
    scheduler.resume()
    
@socketio.on('home')
def file(data):
    scheduler.pause()
    GRBL.SendCommand(f'$H{data}', socketio, 'systemsent')
    scheduler.resume()

@socketio.on('spindle')
def filr(data):
    scheduler.pause()
    GRBL.SendCommand(f'M03 S{data}', socketio, 'systemsent')
    scheduler.resume()

@scheduler.task('interval', id='GetPos', seconds=0.3, max_instances=5)
def SendPositionData():
    GRBL.StatusReport(socketio)
    socketio.emit('position', GRBL.Mpos)
    
@socketio.on('SpindleOveride')
def filr(data):
    scheduler.pause()
    print(data)
    GRBL.adjustSpindle(socketio, data)
    scheduler.resume()
    
if __name__ == "__main__":
    scheduler.pause()
    GRBL = grblCom.GRBLConection('COM5', 115200)
    scheduler.resume()
    socketio.run(app, debug=True, use_reloader=False)