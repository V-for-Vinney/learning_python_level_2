import socket
import json
import time
import datetime
from config import Common

from logger import log_func_call


class MsgrBase:
    @log_func_call
    def __init__(self, sock, address, buffer=Common.BUFFER_SIZE, encoding=Common.DEFAULT_ENCODING):
        self._sock = sock
        self._address = address
        self._buffer = buffer
        self._encoding = encoding

    @log_func_call
    def send(self, message):
        data = json.dumps(message).encode()
        self._sock.send(data)

    @log_func_call
    def receive(self):
        data = self._sock.recv(self._buffer)
        message_json = data.decode()
        return json.loads(message_json)


class MsgrConnection(MsgrBase):
    @log_func_call
    def __init__(self, sock, address, is_client=True):
        self._is_client = is_client
        self.address = address
        super().__init__(sock, address)

    @log_func_call
    def __enter__(self):
        if self._is_client:
            self._sock.connect(self._address)
        return self

    @log_func_call
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sock.close()


class MsgrListener(MsgrBase):
    @log_func_call
    def __init__(self, listen, port, backlog):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        self._backlog = backlog
        super().__init__(sock=sock, address=(listen, port))

    @log_func_call
    def __enter__(self):
        self._sock.bind(self._address)
        self._sock.listen(self._backlog)
        return self

    @log_func_call
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sock.close()

    @log_func_call
    def accept_connection(self):
        sock, address = self._sock.accept()
        return MsgrServer(sock=sock, address=address)


class MsgrServer(MsgrConnection):
    @log_func_call
    def __init__(self, sock, address):
        super().__init__(sock=sock, address=address, is_client=False)

    @log_func_call
    def create_response(self, code: int, msg=''):
        response = {
            Common.RESPONSE: code,
            Common.TIME: time.time(),
        }
        if 200 <= code < 300:
            response[Common.ALERT] = msg
        return response


class MsgrClient(MsgrConnection):
    @log_func_call
    def __init__(self, server, port):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        super().__init__(sock=sock, address=(server, port))

    @log_func_call
    def parse_response(self, response):
        try:
            response = dict(response)
            code = response[Common.RESPONSE]
            f_time = datetime.datetime.fromtimestamp(float(response[Common.TIME])).strftime(Common.DATETIME_FORMAT)
            alert = response[Common.ALERT]
            return code, f_time, alert
        except Exception:
            raise ValueError

    @log_func_call
    def create_presence(self, account_name, status):
        presence_msg = {
            Common.ACTION: Common.PRESENCE,
            Common.TIME: time.time(),
            Common.TYPE: Common.STATUS,
            Common.USER: {
                Common.ACCOUNT: account_name,
                Common.STATUS: status
            }
        }
        return presence_msg
