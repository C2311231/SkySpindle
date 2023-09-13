app = Flask(__name__)
app.secret_key = 'key123'
socketio = SocketIO(app)
State = 'Disconnected'




GRBL_COMMAND_BUFFER = []
OPERATIONS = []


if __name__ == "__main__":
    scheduler.start()
    scheduler.pause()
    
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')
