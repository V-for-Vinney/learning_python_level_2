import argparse
import random
from msgr_core import MsgrClientConnection
from logger import cli_logger, log_and_print


def mainloop(client, receiver):
    group = '#all'
    try:
        while True:
            if receiver == 'yes':
                data = client.receive()
                msg = client.parse_message(data)
                log_and_print(cli_logger.info, msg)
            else:
                msg = input(f'>> [{group}]: ')
                cli_logger.info(msg=msg)
                client.send_message(msg, group)
    except Exception as ex:
        log_and_print(cli_logger.error, f"Exception: {ex}")


if __name__ == '__main__':
    rnd = str(random.randint(10, 100))
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-a", "--address", type=str, help="server ip (default=127.0.0.1)", default='127.0.0.1')
    parser.add_argument("-p", "--port", type=int, help="server port number (default=7777)", default=7777)
    parser.add_argument("-u", "--user", type=str, help="username (default=\"anonymous\")", default=f'anonymous_{rnd}')
    parser.add_argument("-r", "--receiver", type=str, help="for receiver mode type \"y\"", default='y')
    args = parser.parse_args()

    with MsgrClientConnection(server=args.address, port=args.port, account=args.user, new_status='Yep!') as client:
        log_and_print(cli_logger.info, f'User:\t\t{client.account}\nStatus:\t\t\"{client.status}\"')
        client.connect_or_update_status()
        mainloop(client, args.receiver)
