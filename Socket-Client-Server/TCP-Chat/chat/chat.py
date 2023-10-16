import platform
import socket
from datetime import datetime
from os import system
from threading import Thread
from time import time
import select


class ChatUser:
    def __init__(self, socket, host, name: str) -> None:
        self.socket = socket
        self.host = host
        self.name = name

class Chat:
    def __init__(self) -> None:
        self.user_list: list = []
        self.clear_console()
        self.initialize()

        Thread(target=self.accept_users).start()
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
    
    def initialize(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port: int = 1024
        self.socket.bind((socket.gethostname(), self.port))
        self.socket.listen(5)

        self.say(f"Launched on {socket.gethostbyname(socket.gethostname())}:{self.port}")

    def send_response(self, client: socket, response: str) -> bool:
        response_size = len(response.encode("ASCII"))
        sent_data_size = 0

        while sent_data_size < response_size:
            try:
                sent_data_size += client.send(response.encode("ASCII")[sent_data_size:])
            except Exception:
                break
        
        return True if sent_data_size == response_size else False
    
    def promote_system_message(self, message: str) -> None:
        for user in self.user_list:
            self.send_response(user.socket, f"{message}")
    
    def promote_message(self, sender: ChatUser, message: str) -> None:
        for user in self.user_list:
            if user.name != sender.name:
                self.send_response(user.socket, f"<{sender.name}> {message}")

    def manage_user(self, user: ChatUser) -> None:
        while True:
            try:
                message = user.socket.recv(1024).decode("UTF-8")
                print(f"[{datetime.now().time().strftime('%H:%M:%S')}] <{user.name}> {message} // <{user.socket.getsockname()}>")
                self.promote_message(user, message)
            except ConnectionResetError:
                self.promote_system_message(f"{user.name} has left.")
                print(f"[{datetime.now().time().strftime('%H:%M:%S')}] username has left.")
                self.user_list.remove(user)
                break
                
    def accept_users(self) -> None:
        while True:
            try:
                client_socket, client_host = self.socket.accept()
                if client_socket and client_host:
                    username = client_socket.recv(1024).decode("UTF-8")
                    self.user_list.append(ChatUser(client_socket, client_host, username))
                    self.send_response(client_socket, f"1")
                    self.promote_system_message(f"{username} has joined.")
                    print(f"[{datetime.now().time().strftime('%H:%M:%S')}] {username} has joined.")
            except Exception:
                pass
    
    def manage_clients(self) -> None:
        clients_amount = len(self.user_list)

        for user in self.user_list:
            Thread(target=self.manage_user, args=(user,)).start()

        while True:
            if len(self.user_list) > clients_amount:
                clients_amount = len(self.user_list)
                Thread(target=self.manage_user, args=(self.user_list[-1],)).start()
    
if __name__ == "__main__":
    Chat()