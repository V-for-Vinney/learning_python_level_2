import argparse
import time
from msgr_core import MsgrClient

from logger import cli_logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-a", "--address", type=str, help="server ip (default is 127.0.0.1)", default='127.0.0.1')
    parser.add_argument("-p", "--port", type=int, help="server port number (default is 7777)", default=7777)
    args = parser.parse_args()

    while True:
        try:
            with MsgrClient(server=args.address, port=args.port) as client:
                while True:
                    time.sleep(1)
                    try:
                        client.send(client.create_presence(account_name='user', status='Yep!'))
                        response = client.receive()
                        code, timestamp, alert = client.parse_response(response)
                        log_lst = map(lambda x: str(x), [code, timestamp, alert])
                        cli_logger.info(','.join(log_lst))
                    except TypeError:
                        cli_logger.error(f"Raised type error on payload: {response}")
        except ConnectionRefusedError:
            cli_logger.error(f"Server {args.address}:{args.port} seems unavailable. Trying again...")
            time.sleep(1)
