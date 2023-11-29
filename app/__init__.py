import os, sys, requests
from engineio.async_drivers import gevent
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit


def session_for_src_addr(addr: str) -> requests.Session:
    """
    Create `Session` which will bind to the specified local address
    rather than auto-selecting it.
    """
    session = requests.Session()
    for prefix in ('http://', 'https://'):
        session.get_adapter(prefix).init_poolmanager(
            # those are default values from HTTPAdapter's constructor
            connections=requests.adapters.DEFAULT_POOLSIZE,
            maxsize=requests.adapters.DEFAULT_POOLSIZE,
            # This should be a tuple of (address, port). Port 0 means auto-selection.
            source_address=(addr, 0),
        )

    return session

base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)
app = Flask(__name__,static_folder=os.path.join(base_dir, 'static'), template_folder=os.path.join(base_dir, 'templates'))
# app = Flask(__name__,static_folder='static')
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app,async_mode='gevent')

events_flask = []

@app.route('/', methods=['GET'])
def show_events():
    return render_template('index.html', events=events_flask)

@socketio.on('new_event')
def UpdateEvents(events_flask):
    emit('update_events', {'events_flask': events_flask}, broadcast=True,namespace="/")