import socket
import threading

from config import PORT


class Server:
    def __init__(self, port=PORT):
        self._HOST = socket.gethostbyname(socket.gethostname())
        self._PORT = port
        self.start_server()

    @staticmethod
    def send_message(connection):
        while True:
            reply = input()
            connection.sendall(str.encode(reply))

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self._HOST, self._PORT))
            s.listen(5)
            print("\nServer initialized...", self._PORT)
            conn, addr = s.accept()
            with conn:
                print("Connected by: ", addr)
                threading.Thread(target=self.send_message, args=(conn,)).start()
                while True:
                    data = conn.recv(1024)
                    if data:
                        print(data.decode())


if __name__ == "__main__":
    server = Server()
