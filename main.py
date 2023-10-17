import threading
from app import app
from app import socketio
from app.routes import start_scanner


thread = threading.Thread(target=start_scanner)
thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)