import socket
import threading
import time

class ChatClient:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connect()

    def connect(self):
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                print("Connected to the server!")
                self.listen_for_messages()
                break
            except Exception as e:
                print(f"Error connecting to server: {e}")
                time.sleep(5)  # Wait before retrying

    def listen_for_messages(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(f"Server: {message}")
                else:
                    print("Disconnected from server.")
                    self.client_socket.close()
                    self.connect()  # Reconnect
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.client_socket.close()
                self.connect()  # Reconnect
                break

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def run(self):
        while True:
            try:
                message = input("You (Client): ")
                self.send_message(message)
            except Exception as e:
                print(f"Error in input: {e}")

if __name__ == "__main__":
    client = ChatClient()
    client.run()

