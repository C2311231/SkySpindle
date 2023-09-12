from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
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




GRBL_COMMAND_BUFFER = []
OPERATIONS = []


@app.route('/')
def home():
    return render_template('layout.html', SettingsData=SettingsData)
    



def SendData(Name, data):
    socketio.emit(Name, data)


if __name__ == "__main__":
    scheduler.start()
    scheduler.pause()
    OPERATIONS = os.listdir('./OperationFiles')
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')
