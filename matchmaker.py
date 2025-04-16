
import socket
import threading
import random
import json

BROADCAST_PORTS = range(6432, 6436)
DISCOVERY_MESSAGE = b"TIC_TAC_SWEEP"
JOIN_REQUEST = b"JOIN_REQUEST"
JOIN_NOTICE = b"JOIN_NOTICE"
RESPONSE_TIMEOUT = 1.0

class Match:
    def __init__(self, session, board_size=None, bomb_percent=None):
        self.session = session
        self.board_size = board_size
        self.bomb_percent = bomb_percent

        self.host = None
        self.connection = None
        self.sock = None

        self.running = threading.Event()
        self.recv_thread = None
        self.waiting_thread = None

    def create_game_id(self):
        self.game_id = f"TicTacSweepGame{random.randint(1000, 9999)}"

    def create_host_port(self):
        print("\nFinding port...")
        for port in BROADCAST_PORTS:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(("127.0.0.1", port))
                self.sock = sock
                self.host_port = port
                print(f'Port found! Hosting game on port: {self.host_port}')
                return
            
            except OSError as e:
                print(f"ERROR [{e}] - Port {port} in use")
                continue

        raise RuntimeError("ERROR - No available ports.")

    def start(self, stop_searching):
        print("\nStarting game")
        self.host = True
        self.running.set()
        
        self.create_host_port()
        self.create_game_id()

        self.waiting_thread = threading.Thread(target=self.listen, daemon=True, args=(stop_searching,))
        self.waiting_thread.start()

    def stop(self):
        print("\nStopping Match...")
        self.running.clear()

        if self.connection:
            self.send_message('QUIT')
            self.connection = None

        # Ensure the waiting thread is cleaned up
        if self.waiting_thread and self.waiting_thread.is_alive():
            if threading.current_thread() != self.waiting_thread:
                print("Waiting for search thread to stop...")
                self.waiting_thread.join()
                print("Search thread stopped!")
            else: print("Skipping join on waiting_thread (self-join)")

        # Ensure the receiving thread is cleaned up
        if self.recv_thread and self.recv_thread.is_alive():
            if threading.current_thread() != self.recv_thread:
                print("Waiting for receive thread to stop...")
                self.recv_thread.join()
                print("Receive thread stopped!")
            else: print("Skipping join on recv_thread (self-join)")
        
        if self.sock:
            try: self.sock.close()
            except Exception as e: print(f"ERROR [While closing socket]: {e}")
            self.sock = None

        print("Match ended!")

    def listen(self, stop_searching):
        print("\nWaiting for connection...")
        self.sock.settimeout(0.5)
        while self.running.is_set() and not stop_searching.is_set():
            try:
                data, addr = self.sock.recvfrom(1024)
                if data == DISCOVERY_MESSAGE:
                    response = json.dumps({
                        "game_id": self.game_id,
                        "port": self.host_port,
                        "board_size": self.board_size,
                        "bomb_percent": self.bomb_percent,
                    }).encode()
                    self.sock.sendto(response, addr)

                elif data == JOIN_REQUEST:
                    join_connection = addr
                    print(f"Player found at {addr}")

                    settings = json.dumps({
                        "board_size": self.board_size,
                        "bomb_percent": self.bomb_percent
                    }).encode()
                    self.sock.sendto(settings, addr)

                elif data == JOIN_NOTICE and addr == join_connection:
                    print("Player joined!")
                    self.running.clear()
                    self.connection = join_connection
                    self.start_communication()
                    return

            except socket.timeout: continue

    def connect(self, host_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(RESPONSE_TIMEOUT)

        try:
            print(f"Joining game hosted on port: {host_port}...")
            sock.sendto(JOIN_REQUEST, ("127.0.0.1", host_port))

            data, addr = sock.recvfrom(1024)
            print("Received settings from host:", data)

            settings = json.loads(data.decode())
            self.board_size = settings["board_size"]
            self.bomb_percent = settings["bomb_percent"]
            self.connection = addr
            self.sock = sock

            sock.sendto(JOIN_NOTICE, addr)

            print("Sent join confirmation to host.")
            self.session.create_game(self.board_size, self.bomb_percent)
            self.start_communication()
            return True

        except socket.timeout as e:
            print(f'ERROR [Socket Timeout]: {e}')
            self.stop()
            return False

        except json.JSONDecodeError as e:
            print(f"ERROR [JSONDecodeError]: {e}")
            self.stop()
            return False

        except Exception as e:
            print(f"ERROR [Unexpected exception]: {e}")
            self.stop()
            return False

    def start_communication(self):
        self.session.update_info_bar()
        self.session.start_game()
        print("Starting communication...")
        self.running.set()
        self.sock.settimeout(0.1)
        self.recv_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.recv_thread.start()

    def receive_messages(self):
        while self.running.is_set():
            if self.session.game.game_state not in {'Win', 'Lose', 'Tie'}:
                try:
                    data, addr = self.sock.recvfrom(1024)
                    print(f"\n{'-' * 20}\nData recieved from {addr}: \n{data}\n{'-' * 20}\n")

                    message = data.decode()
                    if message: self.session.update_game(message)

                except socket.timeout: continue

                except Exception as e:
                    print(f"ERROR [Unexpected exception]: {e}")
                    self.stop()

    def send_message(self, message):
        try:
            print(f"\n{'-' * 20}\nSending message: \n{message}\n{'-' * 20}\n")
            data = message.encode()
            self.sock.sendto(data, self.connection)

        except Exception as e: print(f"ERROR [Unexpected exception]: {e}")


class MatchSearch:
    def __init__(self):
        self.matches = []

    def discover_matches(self):
        print("Looking for matches...")
        self.matches.clear()
        sockets = []

        # Sweep port range for connections
        for port in BROADCAST_PORTS:
            connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            connection.settimeout(RESPONSE_TIMEOUT)
            sockets.append((connection, port))

        # Send out discover messages
        for connection, port in sockets:
            try:
                connection.sendto(DISCOVERY_MESSAGE, ("127.0.0.1", port))
                data, _ = connection.recvfrom(1024)
                match = json.loads(data.decode())
                self.matches.append(match)

            except (socket.timeout, json.JSONDecodeError): pass
            finally: connection.close()

        print(f'Done! Found {len(self.matches)}')
        return self.matches
