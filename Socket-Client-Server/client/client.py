import socket
import configparser

class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_info = self.get_server_address()
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
    
    def send_message(self, message: str):
        self.socket.send(message.encode("UTF-8"))
    
    def prompt(self):
        self.socket.connect((self.server_info["host"], self.server_info["port"]))
        while True:
            message = input("Message to Server: ")
            self.send_message(message)
        
            print("Waiting for Server response...")
            response = self.socket.recv(1024).decode("UTF-8")
            if response:
                print(f"Server said: {response}")
            else:
                print(f"Server closed the connection.")
                break

if __name__ == "__main__":
    Client()