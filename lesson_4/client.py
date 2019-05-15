import argparse
import time
from msgr_core import MsgrClient


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-a", "--address", type=str, help="server ip (default is 127.0.0.1)", default='127.0.0.1')
    parser.add_argument("-p", "--port", type=int, help="server port number (default is 7777)", default=7777)
    args = parser.parse_args()

    with MsgrClient(server=args.address, port=args.port) as client:
        while True:
            time.sleep(1)
            client.send(client.create_presence(account_name='user', status='Yep!'))
            response = client.receive()
            code, timestamp, alert = client.parse_response(response)
            print(timestamp, code, alert)
