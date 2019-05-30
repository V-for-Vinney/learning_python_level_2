import argparse
import random
import threading
import time
from msgr_core import MsgrClientConnection
from logger import cli_logger, log_and_print


class Listener(threading.Thread):
    def __init__(self, check_interval: int, is_daemon=False):
        super().__init__()
        self.daemon = is_daemon
        self.check_interval = check_interval

    def run(self):
        global client
        while True:
            try:
                data = client.receive()
                msg = client.parse_message(data)
                log_and_print(cli_logger.info, msg)
                time.sleep(self.check_interval)
            except Exception as ex:
                log_and_print(cli_logger.error, f"Exception: {ex}")


def mainloop():
    global client
    addressee = input('--> Enter user name or chat to connect (like #all):')
    listener = Listener(check_interval=1, is_daemon=False)
    listener.start()
    while True:
        try:
            msg = input()
            cli_logger.info(msg=msg)
            client.send_message(msg, addressee)
        except Exception as ex:
            log_and_print(cli_logger.error, f"Exception: {ex}")


if __name__ == '__main__':
    rnd = str(random.randint(10, 100))
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-a", "--address", type=str, help="server ip (default=127.0.0.1)", default='127.0.0.1')
    parser.add_argument("-p", "--port", type=int, help="server port number (default=7777)", default=7777)
    parser.add_argument("-u", "--user", type=str, help="username (default=\"anonymous\")", default=f'anonymous_{rnd}')
    args = parser.parse_args()

    with MsgrClientConnection(server=args.address, port=args.port, account=args.user, new_status='Yep!') as client:
        log_and_print(cli_logger.info, f'User:\t\t{client.account}\nStatus:\t\t\"{client.status}\"')
        client.connect_or_update_status()
        mainloop()
