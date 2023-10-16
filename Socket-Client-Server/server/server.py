from datetime import datetime
import platform
import socket
from os import system
from time import time

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
        _can_receive: bool = True
        while True:
            if _can_receive:
                client_socket, client_address = self.socket.accept()
                data = client_socket.recv(1024).decode('utf-8')

                self.say("Recording message time...")
                last_message_time = time()
                _can_receive = False
                self.say(f"Recorded at {last_message_time}")

                print(f"<{client_socket.getsockname()}> {data} // [{datetime.now().time().strftime('%H:%M:%S')}]")
            
            if time() - last_message_time > 5:
                self.say("Five seconds past, sending to Client...")
                client_socket.send(f"Success".encode("ASCII"))
                _can_receive = True
            
if __name__ == "__main__":
    Server()