import socket
import json
import time
import datetime


class MsgrBase:
    def __init__(self, sock, address):
        self._sock = sock
        self._address = address

    def send(self, message):
        data = json.dumps(message).encode()
        self._sock.send(data)

    def receive(self):
        data = self._sock.recv(1024)
        message_json = data.decode()
        if message_json:
            return json.loads(message_json)
        else:
            return ''


class MsgrConnection(MsgrBase):
    def __init__(self, sock, address, is_client=True):
        self._is_client = is_client
        super().__init__(sock, address)

    def __enter__(self):
        if self._is_client:
            self._sock.connect(self._address)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sock.close()


class MsgrListener(MsgrBase):
    def __init__(self, listen, port, backlog):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        self._backlog = backlog
        super().__init__(sock=sock, address=(listen, port))

    def __enter__(self):
        self._sock.bind(self._address)
        self._sock.listen(self._backlog)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sock.close()

    def accept_connection(self):
        sock, address = self._sock.accept()
        return MsgrServer(sock=sock, address=address)


class MsgrServer(MsgrConnection):
    def __init__(self, sock, address):
        super().__init__(sock=sock, address=address, is_client=False)

    def generate_response(self, code: int):
        response = {
            "response": code,
            "time": time.time(),
            "alert": "OK"
        }
        return response


class MsgrClient(MsgrConnection):
    def __init__(self, server, port):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        super().__init__(sock=sock, address=(server, port))

    def parse_response(self, response):
        response = dict(response)
        code = response['response']
        f_time = datetime.datetime.fromtimestamp(float(response['time'])).strftime('%d.%m.%Y-%H:%M:%S')
        alert = response['alert']
        return code, f_time, alert

    def generate_message(self):
        presence_msg = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": "someAccount",
                "status": "Yep, I am here!"
            }
        }
        return presence_msg
