import socket
import threading
import time

class ChatServer:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port
        self.client_socket = None
        self.client_address = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Server is running and waiting for a connection...")

        self.accept_connection()

    def accept_connection(self):
        while True:
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
                print(f"Client {self.client_address} connected!")
                self.listen_for_messages()
                break
            except Exception as e:
                print(f"Error accepting connection: {e}")
                time.sleep(5)  # Wait before retrying

    def listen_for_messages(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(f"Client: {message}")
                else:
                    print("Client disconnected.")
                    self.client_socket.close()
                    self.accept_connection()  # Reaccept connection
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.client_socket.close()
                self.accept_connection()  # Reaccept connection
                break

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def run(self):
        while True:
            try:
                message = input("You (Server): ")
                self.send_message(message)
            except Exception as e:
                print(f"Error in input: {e}")

if __name__ == "__main__":
    server = ChatServer()
    server.run()

