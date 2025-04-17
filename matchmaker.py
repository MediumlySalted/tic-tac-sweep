import socket
import threading
import random
import json
import hashlib
import hmac
import base64
from cryptography.fernet import Fernet

BROADCAST_PORTS = range(6432, 6436)
GAME_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"TIC_TAC_SWEEP").digest())
GAME_CIPHER = Fernet(GAME_KEY)

DISCOVERY_MESSAGE = "DISCOVERY_MESSAGE"
JOIN_REQUEST = "JOIN_REQUEST"
JOIN_NOTICE = "JOIN_NOTICE"

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

        self.shared_secret = None
        self.cipher = None

    def create_game_id(self):
        self.game_id = f"TicTacSweepGame{random.randint(1000, 9999)}"

    def derive_shared_key(self):
        self.shared_secret = hashlib.sha256(self.game_id.encode()).digest()
        self.cipher = Fernet(base64.urlsafe_b64encode(self.shared_secret))

    def sign_message(self, message_bytes):
        return hmac.new(self.shared_secret, message_bytes, hashlib.sha256).hexdigest()

    def verify_signature(self, message_bytes, signature):
        try:
            expected = hmac.new(self.shared_secret, message_bytes, hashlib.sha256).hexdigest()
            return hmac.compare_digest(expected, signature)
        
        except Exception as e:
            print(f"ERROR [verify_signature]: {e}")
            self.stop()

    def create_host_port(self):
        print("\nFinding port...")

        for port in BROADCAST_PORTS:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(("127.0.0.1", port))
                self.sock = sock
                self.host_port = port
                print(f"Port found! Hosting game on port: {self.host_port}")
                return
            
            except OSError as e: print(f"Port {port} in use: {e}")

        raise RuntimeError("No available ports.")

    def start(self, stop_searching):
        print("\nStarting game...")
        self.host = True
        self.running.set()
        self.create_host_port()
        self.create_game_id()
        self.derive_shared_key()

        self.waiting_thread = threading.Thread(target=self.listen, daemon=True, args=(stop_searching,))
        self.waiting_thread.start()

    def stop(self):
        print("\nStopping Match...")
        self.running.clear()

        if self.connection:
            self.send_message("QUIT")
            self.connection = None

        # Clean up running threads
        for thread in [self.waiting_thread, self.recv_thread]:
            if thread and thread.is_alive() and threading.current_thread() != thread:
                thread.join()

        if self.sock:
            try: self.sock.close()
            except Exception as e: print(f"Socket close error: {e}")
            self.sock = None

        print("Match ended.")

    def listen(self, stop_searching):
        print("Waiting for connection...")
        self.sock.settimeout(0.5)
        join_connection = None

        while self.running.is_set() and not stop_searching.is_set():
            try:
                data, addr = self.sock.recvfrom(1024)

                try: decrypted = GAME_CIPHER.decrypt(data).decode()
                except Exception:  continue

                if decrypted == DISCOVERY_MESSAGE:
                    response = {
                        "port": self.host_port,
                        "board_size": self.board_size,
                        "bomb_percent": self.bomb_percent,
                    }
                    self.sock.sendto(GAME_CIPHER.encrypt(json.dumps(response).encode()), addr)

                elif decrypted == JOIN_REQUEST:
                    join_connection = addr
                    print(f"Player found at {addr}")
                    match_info = {
                        "game_id": self.game_id,
                        "board_size": self.board_size,
                        "bomb_percent": self.bomb_percent
                    }
                    self.sock.sendto(GAME_CIPHER.encrypt(json.dumps(match_info).encode()), addr)

                elif decrypted == JOIN_NOTICE and addr == join_connection:
                    print("Player joined!")
                    self.running.clear()
                    self.connection = join_connection
                    self.start_communication()
                    return

            except socket.timeout: continue

    def connect(self, host_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.settimeout(1)

        try:
            print(f"Joining game on port {host_port}...")
            sock.sendto(GAME_CIPHER.encrypt(JOIN_REQUEST.encode()), ("127.0.0.1", host_port))

            data, addr = sock.recvfrom(1024)
            settings = json.loads(GAME_CIPHER.decrypt(data).decode())

            self.game_id = settings["game_id"]
            self.board_size = settings["board_size"]
            self.bomb_percent = settings["bomb_percent"]
            self.derive_shared_key()

            self.connection = addr
            self.sock = sock

            sock.sendto(GAME_CIPHER.encrypt(JOIN_NOTICE.encode()), addr)
            print("Sent join notice.")

            self.session.create_game(self.board_size, self.bomb_percent)
            self.start_communication()
            return True

        except Exception as e:
            print(f"Connect error: {e}")
            self.stop()
            return False

    def start_communication(self):
        self.session.update_info_bar()
        self.session.start_game()

        print(f"\n\n=========== Communication started ===========")
        print(f"Game ID: {self.game_id}")
        print(f"Shared Secret: {self.shared_secret}")
        print(f"Connected to: {self.connection}\n")

        self.running.set()
        self.sock.settimeout(0.1)
        self.recv_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.recv_thread.start()

    def receive_messages(self):
        while self.running.is_set():
            if self.session.game.game_state in {"Win", "Lose", "Tie"}: continue

            try:
                response, _ = self.sock.recvfrom(1024)
                payload = json.loads(response.decode())
                encrypted_data = bytes.fromhex(payload["message"])

                if not self.verify_signature(encrypted_data, payload["signature"]):
                    print("Message blocked.")
                    continue

                decrypted = self.cipher.decrypt(encrypted_data).decode()
                print(f"Decrypted message: {decrypted}")
                if decrypted: self.session.update_game(decrypted)

            except (socket.timeout, json.JSONDecodeError, KeyError): continue

            except Exception as e:
                print(f"Receive error: {e}")
                self.stop()

    def send_message(self, message):
        try:
            encrypted = self.cipher.encrypt(message.encode())
            signature = self.sign_message(encrypted)

            payload = json.dumps({
                "message": encrypted.hex(),
                "signature": signature
            }).encode()

            self.sock.sendto(payload, self.connection)

        except Exception as e: print(f"Send error: {e}")


class MatchSearch:
    def __init__(self):
        self.matches = []

    def discover_matches(self):
        print("\nLooking for matches...")
        self.matches.clear()
        sockets = []

        for port in BROADCAST_PORTS:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.25)
            sockets.append((s, port))

        for sock, port in sockets:
            try:
                sock.sendto(GAME_CIPHER.encrypt(DISCOVERY_MESSAGE.encode()), ("127.0.0.1", port))
                data, _ = sock.recvfrom(1024)
                match = json.loads(GAME_CIPHER.decrypt(data).decode())
                self.matches.append(match)

            except (socket.timeout, json.JSONDecodeError, Exception): pass

            finally: sock.close()

        print(f"Found {len(self.matches)} matches.")
        return self.matches
