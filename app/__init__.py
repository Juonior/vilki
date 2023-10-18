import os, sys
from engineio.async_drivers import gevent
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit

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