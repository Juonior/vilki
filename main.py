import threading
from app import app
from app.routes import start_scanner


thread = threading.Thread(target=start_scanner)
thread.start()

if __name__ == '__main__':
    app.run(debug=True)
