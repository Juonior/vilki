from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

events_flask = []

@app.route('/', methods=['GET'])
def show_events():
    return render_template('index.html', events=events_flask)

@socketio.on('new_event')
def addNewEvent(new_event):
    events_flask.append(new_event)
    emit('update_event', new_event, broadcast=True,namespace="/")
