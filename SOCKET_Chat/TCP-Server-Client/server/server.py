from datetime import datetime
import socket
import platform
from os import system
from time import time

from threading import Thread

class ClientConnection:
    def __init__(self, socket, host) -> None:
        self.socket = socket
        self.host = host


class Server:
    def __init__(self) -> None:
        self.client_list: list = []
        self.initialize()

        Thread(target=self.accept_clients).start()
        self.manage_clients()
    
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
    
    def manage_client(self, client: ClientConnection) -> None:
        _can_receive: bool = True
        while True:
            if _can_receive:
                data = client.socket.recv(1024).decode('utf-8')

                last_message_time = time()
                _can_receive = False

                print(f"<{client.socket.getsockname()}> {data} // [{datetime.now().time().strftime('%H:%M:%S')}]")
            
            if time() - last_message_time > 5:
                self.send_response(client.socket, "Thanks for your message.")
                _can_receive = True
            
            if data == "exit":
                self.say("Shutting down...")

                for client in self.client_list:
                    client.socket.close()
                self.socket.close()

                break

    def accept_clients(self) -> None:
        while True:
            try:
                client_socket, client_host = self.socket.accept()
                if client_socket and client_host:
                    self.client_list.append(ClientConnection(client_socket, client_host))
                    self.send_response(client_socket, "Welcome, we attached your client.")
            except Exception:
                pass
    
    def manage_clients(self) -> None:
        clients_amount = len(self.client_list)

        for client in self.client_list:
            Thread(target=self.manage_client, args=(client,)).start()

        while True:
            if len(self.client_list) != clients_amount:
                clients_amount = len(self.client_list)
                Thread(target=self.manage_client, args=(self.client_list[-1],)).start()
    
if __name__ == "__main__":
    Server()