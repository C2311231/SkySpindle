from flask import Flask, render_template
from flask_socketio import SocketIO
import helpers

SETTINGCODES = helpers.getCSVData('setting_codes_en_US.csv')
STATE = 'Disconnected'

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('layout.html', SettingsData=SETTINGCODES)

import _socket.py