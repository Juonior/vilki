import threading
from app import app
from app import socketio
from app.routes import get_info
import time, socket


def get_additional_ips():
    additional_ips = []
    hostname = socket.gethostname()
    try:
        ips = socket.gethostbyname_ex(hostname)
        # Индекс 2 в возвращаемом кортеже содержит список дополнительных IP-адресов
        additional_ips = ips[2]
    except socket.gaierror as e:
        print(f"Ошибка: {e}")
    
    return additional_ips

additional_ips = get_additional_ips()
# additional_ips = ["192.168.2.211", "192.168.2.211", "192.168.2.211","192.168.2.211"]
def start_scanner():
    print("[STATUS] Scanner started.")
    i = 0
    while True:
        # t = threading.Thread(target=get_info,args=(proxies[i],))
        # t.daemon = True  # Помечаем поток как демон, чтобы он завершился при завершении главного потока.
        # t.start()
        # time.sleep(2)
        try:
            get_info(additional_ips[i])
        except Exception as ex:
            print(ex)
        # print(proxies[i])
        i = (i + 1) % len(additional_ips)
        # time.sleep(0.5)



if __name__ == '__main__':
    thread = threading.Thread(target=start_scanner).start()
    socketio.run(app,host="0.0.0.0", allow_unsafe_werkzeug=True)
