import argparse
from typing import List
from select import select
# from config import HTTPResponseCode
from msgr_core import MsgrListener, MsgrServerConnection
from logger import srv_logger, log_and_print


def read_requests(r_clients: List[MsgrServerConnection], all_clients: list) -> List[str]:
    messages = []
    for client_conn in r_clients:
        try:
            data = client_conn.receive()
            messages.append(data)
        except Exception:
            log_and_print(srv_logger.info, f'Client {client_conn.address} disconnected.')
            all_clients.remove(client_conn)
    return messages


def send_responses(broadcast_msgs: list, w_clients: List[MsgrServerConnection], all_clients: list):
    for client_conn in w_clients:
        for msg in broadcast_msgs:
            try:
                client_conn.send(message=msg)
            except Exception:
                log_and_print(srv_logger.info, f'Client {client_conn.address} disconnected.')
                all_clients.remove(client_conn)
                client_conn.close()


def mainloop(listener: MsgrListener):
    clients = []
    while True:
        try:
            srv_conn = listener.accept_connection()
        except OSError:
            pass
        else:
            log_and_print(srv_logger.info, f"Получен запрос на соединение от {srv_conn.address}")
            clients.append(srv_conn)
        finally:
            wait = 0
            read = []
            write = []
            try:
                read, write, error = select(clients, clients, [], wait)
            except Exception:
                pass

            messages = read_requests(read, clients)
            send_responses(messages, write, clients)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-a", "--address", type=str, help="client's ip-address (all IP by default)", default='')
    parser.add_argument("-p", "--port", type=int, help="listener tcp-port number (default is 7777)", default=7777)
    parser.add_argument("-t", "--timeout", type=int, help="checking interval (default is 0.5)", default=0.5)
    parser.add_argument("-b", "--backlog", type=int, help="maximum connections (default is 10)", default=10)
    args = parser.parse_args()

    with MsgrListener(listen=args.address, port=args.port, backlog=args.backlog, timeout=args.timeout) as srv_listener:
        diag_msg = f'Server started at {args.port} port.'
        srv_logger.info(diag_msg)
        print(diag_msg)
        mainloop(srv_listener)
