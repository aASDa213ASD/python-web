import socket
import configparser

class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_info = self.get_server_address()
        self.socket.connect((self.server_info["host"], self.server_info["port"]))
        self.prompt()
    
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
    
    def send_message(self, message):
        self.socket.send(message.encode("UTF-8"))
    
    def prompt(self):
        message = input("Message to Server: ")
        self.send_message(message)
        response = self.socket.recv(1024).decode('utf-8')
        print(f"Server said: {response}")

if __name__ == "__main__":
    Client()