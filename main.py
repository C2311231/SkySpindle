import yaml
from WebInterface import app, socketio

with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')