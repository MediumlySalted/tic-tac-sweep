import socket
import threading
import random
import json

class Match:
    def __init__(self, game, port=7212):
        self.game = game
        self.host = False
        self.port = port
        self.connection = None

    def find_match(self, stop_searching):
        ip = None
        while not ip and not stop_searching.is_set():
            ip = self.find_server(stop_searching)
            if ip:
                self.connect_server(ip, self.port)
            elif not stop_searching.is_set():
                ip = self.advertise_server(stop_searching)
                if ip:
                    self.start_server()
                    self.host = True

    def find_server(self, stop_searching, timeout=1):
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
        while not server_ip and not stop_searching.is_set():
            try:
                response, server_address = udp_socket.recvfrom(1024)
                if response == b"hosting tic-tac-sweep" and not stop_searching.is_set():
                    print(f"Server found at [{server_address[0]}:{server_address[1]}].")
                    server_ip = server_address[0]

            except socket.timeout:
                if not stop_searching.is_set(): print("\nNo server found within the timeout period.")
                break

        udp_socket.close()
        return server_ip

    def advertise_server(self, stop_searching, timeout=5):
        # Create a UDP socket to listen for discovery requests
        timeout += round(random.uniform(0, 2), 3) # Randomizes timeout to prevent sync'd searches
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.settimeout(timeout)
        udp_socket.bind(('', self.port))
        print(f"Listening for clients on port [{self.port}]...")

        client_ip = None
        while not client_ip and not stop_searching.is_set():
            try:
                data, client_address = udp_socket.recvfrom(1024)
                if data == b"looking for tic-tac-sweep" and not stop_searching.is_set():
                    print(f"Client found at [{client_address}].")
                    response_message = b"hosting tic-tac-sweep"
                    udp_socket.sendto(response_message, client_address)
                    client_ip = client_address[0]

            except socket.timeout:
                if not stop_searching.is_set(): print("\nNo client found within the timeout period.")
                break

        udp_socket.close()
        return client_ip

    def recieve_messages(self):
        print(f'Update Messages:\n{'-' * 25}')
        self.connection.settimeout(1)
        while self.game.game_state not in {'Win', 'Lose', 'Tie'}:
            try:
                data = self.connection.recv(1024).decode()
                message = json.loads(data)
                if message:
                    print(f'Recieved: {message}')
                    if message == 'QUIT':
                        self.game.update(message)
                        self.end()
                        break
                    else: self.game.update(message)
            except socket.timeout: continue
            except OSError: break

        self.end()

    def send_message(self, message):
        print(f'Sent message: {message}')
        data = json.dumps(message)
        self.connection.sendall(data.encode())

    def message_handler(self):
        # Send & Recieve game settings from opponent and initialize an inbetween value
        self.send_message((self.game.size, self.game.bomb_percent))
        message = self.connection.recv(1024).decode()
        game_data = json.loads(message)
        print(f'Recieved game data: {game_data}')
        size = (game_data[0] + self.game.size) // 2
        bomb_percent = round((game_data[1] + self.game.bomb_percent) / 2, 2)
        self.game.size = size
        self.game.bomb_percent = bomb_percent
        self.game.game_frame.master.settings.size = size
        self.game.game_frame.master.settings.bomb_percent = bomb_percent
        self.game.game_frame.master.settings.update_settings()

        receive_thread = threading.Thread(target=self.recieve_messages)
        receive_thread.start()
        receive_thread.join()

    def start_server(self):
        self.host = True
        print(f"\nHosting TCP server on port {self.port}...")
        host = ''
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, self.port))
        server_socket.listen(1)

        client_socket, client_address = server_socket.accept()
        print(f"{'-'*10} Connection established with [{client_address}] {'-'*10}\n")

        self.connection = client_socket
        self.message_handler()
        server_socket.close()
        print("Server closed.")

    def connect_server(self, host, port):
        print(f"\n{'-'*10} Connecting to server at [{host}:{port}] {'-'*10}\n")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        self.connection = client_socket
        self.message_handler()

    def end(self):
        if self.connection:
            print('Ending connection.')
            try:
                self.send_message('QUIT')
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError: pass
            finally:
                self.connection.close()
                print('Connection ended.')
