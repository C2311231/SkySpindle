from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
import helpers
import grblCom

SETTINGCODES = helpers.getCSVData('setting_codes_en_US.csv')
STATE = 'Disconnected'
app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
socketio = SocketIO(app)

GRBL = grblCom.GRBLConection(socketio.emit)

GRBL_COMMAND_BUFFER = []