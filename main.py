import threading
from app import app
from app import socketio
from app.routes import get_info
import time

proxies = [
    "http://gR8bNG1g:jknP4TJU@194.156.122.187:64290",
    "http://gR8bNG1g:jknP4TJU@45.152.226.38:61950",
    "http://gR8bNG1g:jknP4TJU@194.61.77.242:64644",
    "http://gR8bNG1g:jknP4TJU@195.19.168.209:62036",
    "http://gR8bNG1g:jknP4TJU@109.94.211.231:61930"
]
def start_scanner():
    print("[STATUS] Scanner started.")
    i = 0
    while True:
        # t = threading.Thread(target=get_info,args=(proxies[i],))
        # t.daemon = True  # Помечаем поток как демон, чтобы он завершился при завершении главного потока.
        # t.start()
        # time.sleep(2)
        get_info(proxies[i])
        # print(proxies[i])
        i = (i + 1) % len(proxies)
        # time.sleep(0.5)



if __name__ == '__main__':
    thread = threading.Thread(target=start_scanner).start()
    socketio.run(app,host="0.0.0.0", allow_unsafe_werkzeug=True)
