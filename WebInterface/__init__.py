from flask import render_template
from ._commons import app, SETTINGCODES

@app.route('/')
def home():
    return render_template('layout.html', SettingsData=SETTINGCODES)

from ._Websocketio import *
from ._scheduled import *