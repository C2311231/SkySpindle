from flask import Flask, render_template
from flask_socketio import SocketIO
import grblCom

app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('layout.html')





socketio.run(app, debug=True)