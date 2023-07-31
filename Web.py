from flask import Flask, render_template
from flask_socketio import SocketIO
import grblCom

app = Flask(__name__)
app.secret_key = 'key123'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('layout.html')



@socketio.on('Jog')
def fil(data):
    print(data)

socketio.run(app, debug=True)