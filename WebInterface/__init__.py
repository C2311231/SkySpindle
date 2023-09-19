from flask import render_template
from ._commons import app, SETTINGCODES

@app.route('/')
def home():
    return render_template('main.html', SettingsData=SETTINGCODES)

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

from ._Websocketio import *
from ._scheduled import *