from datetime import datetime
import platform
import random
import socket
from os import system


class Server:
    def __init__(self) -> None:
        self.initialize()
        self.accept_clients()
    
    def say(self, message: str) -> None:
        print(f"<{self.__class__.__name__}> {message}")
        
    def clear_console(self):
        system_platform = platform.system().lower()

        if system_platform == "windows":
            system("cls")
        elif system_platform == "linux":
            system("clear")
        else:
            pass
    
    def bind(self) -> None:
        self.socket.bind((socket.gethostname(), self.port))

    def initialize(self) -> None:
        self.clear_console()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port: int = 1024

        self.bind()
        self.socket.listen(5)

        self.say(f"Launched on {socket.gethostbyname(socket.gethostname())}:{self.port}")

    def accept_clients(self) -> None:
        while True:
            client_socket, client_address = self.socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(f"<{client_socket.getsockname()}> {data} // [{datetime.now().time().strftime('%H:%M:%S')}]")
            
            client_socket.send(f"Success".encode("ASCII"))

if __name__ == "__main__":
    Server()