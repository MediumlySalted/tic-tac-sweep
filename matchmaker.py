import socket
import threading
import random


class Match:
    def __init__(self, game, port=7212):
        self.game = game
        self.host = False
        self.port = port
        self.connection = None

    def find_match(self):
        ip = None
        while not ip:
            ip = self.find_server()
            if ip:
                self.connect_server(ip, self.port)
            else:
                ip = self.advertise_server()
                if ip: self.start_server()

    def find_server(self, timeout=1):
        # Set up the UDP socket for broadcasting
        timeout += round(random.uniform(0, 2), 3) # Randomizes timeout to prevent sync'd searches
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(timeout)

        message = b"looking for tic-tac-sweep"
        broadcast_address = ('<broadcast>', self.port)
        udp_socket.sendto(message, broadcast_address)
        print(f"\nSearching for servers on port [{self.port}]...")

        server_ip = None
        while not server_ip:
            try:
                response, server_address = udp_socket.recvfrom(1024)
                if response == b"hosting tic-tac-sweep":
                    print(f"Server found at [{server_address[0]}:{server_address[1]}].")
                    server_ip = server_address[0]

            except socket.timeout:
                print("No server found within the timeout period.")
                break

        udp_socket.close()
        return server_ip

    def advertise_server(self, timeout=5):
        # Create a UDP socket to listen for discovery requests
        timeout += round(random.uniform(0, 2), 3) # Randomizes timeout to prevent sync'd searches
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.settimeout(timeout)
        udp_socket.bind(('', self.port))
        print(f"\nListening for clients on port {self.port}...")

        client_ip = None
        while not client_ip:
            try:
                data, client_address = udp_socket.recvfrom(1024)
                if data == b"looking for tic-tac-sweep":
                    print(f"Client found at [{client_address}].")
                    response_message = b"hosting tic-tac-sweep"
                    udp_socket.sendto(response_message, client_address)
                    client_ip = client_address[0]

            except socket.timeout:
                print("No client found within the timeout period.")
                break

        udp_socket.close()
        return client_ip

    def recieve_messages(self):
        self.connection.settimeout(1)
        while self.game.game_state not in {'Win', 'Lose', 'Tie'}:
            try:
                message = self.connection.recv(1024).decode()
                if message: self.game.update(message)
            except socket.timeout:
                continue

    def send_message(self, message):
        message = message
        self.connection.sendall(message.encode())

    def message_handler(self):
        receive_thread = threading.Thread(target=self.recieve_messages)

        receive_thread.start()
        receive_thread.join()

        self.connection.close()
        print("Connection closed")

    def start_server(self):
        self.host = True
        print(f"\nHosting TCP server on port {self.port}...")
        host = ''
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, self.port))
        server_socket.listen(1)

        client_socket, client_address = server_socket.accept()
        print(f"Connection established with [{client_address}].")

        self.connection = client_socket
        self.message_handler()
        server_socket.close()
        print("Server closed.")

    def connect_server(self, host, port):
        print(f"\nConnecting to server at [{host}:{port}].")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        self.connection = client_socket
        self.message_handler()
