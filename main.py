import threading

from client import Client
from config import PORT
from server import Server


def create_server(port=PORT):
    Server(host='127.0.0.1', port=port)


def create_client(port=PORT):
    Client(port=port)


if __name__ == "__main__":
    server_thread = threading.Thread(target=create_server)
    client_thread = threading.Thread(target=create_client)

    server_thread.start(), client_thread.start()
