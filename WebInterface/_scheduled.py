import os
import time
from ._commons import app, scheduler, socketio, GRBL_COMMAND_BUFFER, GRBL, STATE

GRBL_COMMAND_BUFFER = []


@scheduler.task('interval', id='SlowUpdate', seconds=5, max_instances=1)
def SlowUpdate():
    OPERATIONS = os.listdir('./OperationFiles')
    socketio.emit('settings', GRBL.settings)
    socketio.emit('State', STATE.STATE)
    socketio.emit('operations', OPERATIONS)


@scheduler.task('interval', id='GetSettings', seconds=20, max_instances=1)
def UpdateSettings():
    if GRBL.status == 'Idle':
        GRBL_COMMAND_BUFFER.append(['GetGRBLSettings'])

@scheduler.task('interval', id='GetPos', seconds=0.3, max_instances=5)
def SendPositionData():
    mpos = []
    wpos = []
    for item in GRBL.Mpos:
        mpos.append(round(item, 3))
    for item in GRBL.Wpos:
        wpos.append(round(item, 3))
    socketio.emit('positionM', mpos)
    socketio.emit('positionW', wpos)
    if GRBL.status == 'Operating':
        socketio.emit('operationTime', time.time() - GRBL.operationStartTime)
    if GRBL.subStatus:
        socketio.emit('Machine Status', f'Status: {GRBL.Machinestatus}:{GRBL.subStatus}')
    else:
        socketio.emit('Machine Status', f'Status: {GRBL.Machinestatus}')
scheduler.start()
scheduler.pause()