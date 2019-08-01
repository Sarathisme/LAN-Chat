import os
import socket
import threading

from config import PORT
from devices import Mapper


class Client:
    def __init__(self, port):
        self._HOST = None
        self._PORT = port
        self._END = False
        self.start_chat()

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def start_chat(self):
        while True:
            scan = input("Scan devices? ")
            if scan == 'bye' or scan == 'BYE' or scan == -1:
                return
            elif 'y' in scan or 'Y' in scan or scan == 1:
                self.clear_screen()
                hosts = Mapper().get_addresses()
                self._END = False
                self._HOST = self.get_selected_host(hosts)
                if self._HOST != -1:
                    self.connect_to_server()

    @staticmethod
    def get_selected_host(hosts):
        try:
            for index in range(0, len(sorted(set(hosts)))):
                print(str(index + 1) + '. ', hosts[index])

            print("Your device details: ", socket.gethostbyname(socket.gethostname()), socket.gethostname(), "\n")

            return hosts[int(input('Enter the host number you want to connect to: ')) - 1]
        except IndexError as e:
            print("No active devices")
            return -1

    def send_message(self, socket=None):
        while True:
            message = input()
            if message == 'BYE' or message == 'bye':
                self._END = True
            socket.sendall(str.encode(message))

    def connect_to_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self._HOST, self._PORT))

                threading.Thread(target=self.send_message, args=(s,)).start()
                while not self._END:
                    data = s.recv(1024)
                    if data:
                        print(data.decode())

        except ConnectionRefusedError as ce:
            print("\nDevice not active or not running the chat server\n")

        except Exception as e:
            print(e)

        finally:
            self.start_chat()


if __name__ == "__main__":
    client = Client(port=PORT)
