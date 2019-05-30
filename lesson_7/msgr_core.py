import socket
import json
import time
import datetime
from config import Common, JIM, HTTPResponseCode

from logger import log_func_call, dbg_logger, srv_logger, cli_logger, log_and_print


class MsgrBase:
    @log_func_call(dbg_logger)
    def __init__(self, sock, address, buffer=Common.BUFFER_SIZE, encoding=Common.DEFAULT_ENCODING):
        self._sock = sock
        self._address = address
        self._buffer = buffer
        self._encoding = encoding

    @log_func_call(dbg_logger)
    def send(self, message):
        data = json.dumps(message).encode()
        self._sock.send(data)

    @log_func_call(dbg_logger)
    def receive(self):
        data = self._sock.recv(self._buffer)
        message_json = data.decode()
        return json.loads(message_json)


class MsgrListener(MsgrBase):
    @log_func_call(dbg_logger)
    def __init__(self, listen: str, port: int, backlog: int, timeout: float):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        self._backlog = backlog
        self._timeout = timeout
        super().__init__(sock=sock, address=(listen, port))

    @log_func_call(dbg_logger)
    def __enter__(self):
        self._sock.bind(self._address)
        self._sock.listen(self._backlog)
        self._sock.settimeout(self._timeout)
        return self

    @log_func_call(dbg_logger)
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sock.close()

    def accept_connection(self):
        sock, address = self._sock.accept()
        return MsgrServerConnection(sock=sock, address=address)


class MsgrConnection(MsgrBase):
    @log_func_call(dbg_logger)
    def __init__(self, sock, address, is_client=True):
        self._is_client = is_client
        self.address = address
        super().__init__(sock, address)

    @log_func_call(dbg_logger)
    def __enter__(self):
        if self._is_client:
            while True:
                try:
                    self._sock.connect(self._address)
                except ConnectionRefusedError:
                    log_and_print(cli_logger.error,
                                  f"Server {':'.join(map(str, self.address))} unavailable. Retrying...")
                    time.sleep(2)
                else:
                    log_and_print(cli_logger.info, f'Successfully connected to {self.address}.')
                    break
            return self

    @log_func_call(dbg_logger)
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sock.close()

    def fileno(self):
        return self._sock.fileno()


class MsgrServerConnection(MsgrConnection):
    @log_func_call(srv_logger)
    def __init__(self, sock, address):
        super().__init__(sock=sock, address=address, is_client=False)

    @log_func_call(srv_logger)
    def create_response(self, code: int, msg=''):
        response = {
            JIM.ACTION: JIM.RESPONSE,
            JIM.RESPONSE: code,
            JIM.TIME: time.time(),
        }
        if HTTPResponseCode.OK[0] <= code < HTTPResponseCode.RESERVED[0]:
            response[JIM.ALERT] = msg
        return response

    @log_func_call(srv_logger)
    def close(self):
        self._sock.close()


class MsgrClientConnection(MsgrConnection):
    status = ''
    account = ''

    @log_func_call(cli_logger)
    def __init__(self, server, port, account, new_status=''):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        self.account = account
        if new_status:
            self.status = new_status
        super().__init__(sock=sock, address=(server, port))

    @log_func_call(cli_logger)
    def connect_or_update_status(self, status=Common.DEFAULT_CLIENT_STATUS):
        presence_msg = {
            JIM.ACTION: JIM.PRESENCE,
            JIM.TIME: time.time(),
            JIM.TYPE: JIM.STATUS,
            JIM.USER: {
                JIM.ACCOUNT: self.account,
                JIM.STATUS: status
            }
        }
        self.send(presence_msg)

    @log_func_call(cli_logger)
    def send_message(self, msg_text: str, addressee: str):
        message = {
            JIM.ACTION: JIM.MSG,
            JIM.TIME: time.time(),
            JIM.TO: addressee,
            JIM.FROM: self.account,
            JIM.ENCODING: Common.DEFAULT_ENCODING,
            JIM.MSG: msg_text
        }
        self.send(message)

    @log_func_call(cli_logger)
    def parse_message(self, message):
        try:
            result = ''
            message = dict(message)
            f_time = datetime.datetime.fromtimestamp(float(message[JIM.TIME])).strftime(Common.DATETIME_FORMAT)
            if message[JIM.ACTION] == JIM.RESPONSE:
                code = message[JIM.RESPONSE]
                alert = message[JIM.ALERT]
                result = f'{str(f_time)}:{code}'
                if alert:
                    result += f', {alert}'
            elif JIM.MSG in message.keys():
                sender = message[JIM.FROM]
                msg = message[JIM.MSG]
                result = f'{str(f_time)} [{sender}]: {msg}'
            return result
        except Exception:
            raise ValueError
