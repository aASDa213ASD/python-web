import configparser
import platform
import socket
from os import system
from threading import Thread
from threading import Event

class Client:
    def __init__(self) -> None:
        self.socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_info: dict = self.get_server_address()
        self.leave_flag = Event()
        self.name: str = self.get_name()
        self.clear_console()

        if self.connect_to_chat_room():
            self.listener = Thread(target=self.listen_chat_room)
            self.listener.start()
            self.chat()
    
    def clear_console(self):
        system_platform = platform.system().lower()

        if system_platform == "windows":
            system("cls")
        elif system_platform == "linux":
            system("clear")
        else:
            pass
    
    def get_server_address(self) -> dict:
        config = configparser.ConfigParser()
        config.read("client/settings.ini")

        # Get the server IP and PORT values
        host = config.get("Server", "host")
        port = config.getint("Server", "port")

        server_info = {
            "host": host,
            "port": port
        }

        return server_info

    def get_name(self) -> str:
        config = configparser.ConfigParser()
        config.read("client/settings.ini")
        name = config.get("User", "name")
        return name
    
    def send_message(self, message: str):
        self.socket.send(message.encode("UTF-8"))
    
    def connect_to_chat_room(self) -> bool:
        print(f"Connecting to {self.server_info['host']}:{self.server_info['port']}...")
        """ Connecting to Chat server """
        self.socket.connect((self.server_info["host"], self.server_info["port"]))
        """ Providing Chat server our name """
        self.send_message(self.name)
        """ Waiting for approving for Chat server """
        response = self.socket.recv(1024).decode("UTF-8")
        return True if response else False
    
    def disconnect_from_chat_room(self) -> None:
        self.socket.close()
    
    def listen_chat_room(self) -> None:
        while not self.leave_flag.is_set():
            chat_message = self.socket.recv(1024).decode("UTF-8")
            if chat_message:
                print(f"{chat_message}")
    
    def chat(self):
        while True:
            message = input()
            match (message):
                case "!clear":
                    self.clear_console()
                case "!leave":
                    self.leave_flag.set()
                    self.disconnect_from_chat_room()
                    print(f"<Client> end of !leave")
                case _:
                    self.send_message(message)
        print(f"<Client> Exited main loop")

if __name__ == "__main__":
    Client()