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

    def send_response(self, client: socket, response: str) -> bool:
        response_size = len(response.encode("ASCII"))
        sent_data_size = 0

        while sent_data_size < response_size:
            sent_data_size += client.send(response.encode("ASCII")[sent_data_size:])
        
        if sent_data_size == response_size:
            self.say("Successfully sent response to client.")
            return True
        else:
            self.say("Error in sending data.")
        return False
        

    def accept_clients(self) -> None:
        _can_receive: bool = True
        client_socket, client_address = self.socket.accept()
        while True:
            if _can_receive:
                data = client_socket.recv(1024).decode('utf-8')

                last_message_time = time()
                _can_receive = False

                print(f"<{client_socket.getsockname()}> {data} // [{datetime.now().time().strftime('%H:%M:%S')}]")
            
            if time() - last_message_time > 5:
                self.send_response(client_socket, "Thanks for your message.")
                _can_receive = True
            
            if data == "exit":
                client_socket.close()
                self.socket.close()
                break
        self.say("Shutting down...")
    
if __name__ == "__main__":
    Server()