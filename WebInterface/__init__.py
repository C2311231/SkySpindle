from flask import render_template, request, jsonify
from ._commons import app, SETTINGCODES
import requests
import json

@app.route('/')
def home():
    notifications = requests.get("https://raw.githubusercontent.com/C2311231/SkySpindle/main/version.json")
    if notifications.status_code == 200:
        notifications = json.loads(notifications.content)
        
        with open('./version.json') as version:
            print(version)
            version = json.load(version)
        if version == notifications:
            notifications = None
    else:
        notifications = None
    return render_template('main.html', SettingsData=SETTINGCODES, notifications=notifications)

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