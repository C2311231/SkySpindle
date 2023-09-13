from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
import helpers
from GRBLTools import GRBLConection

SETTINGCODES = helpers.getCSVData('setting_codes_en_US.csv')
class StateTracker():
    def __init__(self, STATE):
        self.STATE = STATE

STATE = StateTracker('Disconnected')

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
socketio = SocketIO(app)
GRBL_COMMAND_BUFFER = []

GRBL = GRBLConection(socketio.emit, GRBL_COMMAND_BUFFER)