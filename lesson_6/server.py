import argparse
from config import HTTPResponseCode
from msgr_core import MsgrListener

from logger import srv_logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-a", "--address", type=str, help="client's ip-address (all IP by default)", default='')
    parser.add_argument("-p", "--port", type=int, help="listener tcp-port number (default is 7777)", default=7777)
    parser.add_argument("-b", "--backlog", type=int, help="maximum connections (default is 10)", default=10)
    args = parser.parse_args()
    with MsgrListener(listen=args.address, port=args.port, backlog=args.backlog) as listener:
        srv_logger.info(f'Server started at {args.port} port.')
        while True:
            with listener.accept_connection() as srv_connection:
                data = srv_connection.receive()
                srv_logger.info(f'Client {srv_connection.address} connected')
                while data:
                    srv_logger.info(data)
                    srv_connection.send(srv_connection.create_response(code=HTTPResponseCode.OK))
                    data = srv_connection.receive()
