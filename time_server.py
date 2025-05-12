from socket import *
import socket
import threading
import logging
import datetime

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        buffer = ""
        while True:
            data = self.connection.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8', errors='ignore')

            if buffer.endswith('\r\n'):
                logging.info(f"Received from {self.address}: {buffer.strip()}")
                
                # Handle TIME request
                if buffer.startswith("TIME") and buffer.endswith("\r\n"):
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                
                # Handle QUIT
                if buffer.strip() == "QUIT":
                    break
                
                buffer = ""

        self.connection.close()
        logging.info(f"Connection closed with {self.address}")

# Main server thread
class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))  # Port 45000
        self.my_socket.listen(5)
        logging.warning("Time Server started on port 45000...")
        while True:
            connection, client_address = self.my_socket.accept()
            logging.warning(f"Connection from {client_address}")
            clt = ProcessTheClient(connection, client_address)
            clt.start()
            self.the_clients.append(clt)

# Run the server
def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
