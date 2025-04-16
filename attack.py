import socket
import threading
from matchmaker import MatchSearch

class Attack:
    def __init__(self, target_port, target_address):
        self.target_port = target_port
        self.target_address = target_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_running = True
        self.running = threading.Event()
        self.start_communication()

    def spoof_message(self, message):
        print(f"Sending message to {self.target_address}...")
        self.sock.sendto(message.encode(), self.target_address)
        print("Sent!")

        if message == 'QUIT': self.close_connection()

    def start_communication(self):
        print("\nStarting receiving thread...")
        self.sock.settimeout(0.5)
        self.running.set()
        self.recv_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.recv_thread.start()
        print("Receiving thread started!")

    def receive_messages(self):
        while self.running.is_set():
            try:
                response, addr = self.sock.recvfrom(1024)
                print(f"\n{'-' * 20}\nResponse recieved from {addr}: \n{response}\n{'-' * 20}\nEnter message ('QUIT' to stop): ", end="")

                if response in ['QUIT', 'WIN', 'TIE']:
                    attack.close_connection()
                    break

            except socket.timeout: continue

    def close_connection(self):
        print("\nClosing connection...")
        self.is_running = False
        self.running.clear()

        # Ensure the receiving thread is cleaned up
        if self.recv_thread and self.recv_thread.is_alive():
            if threading.current_thread() != self.recv_thread:
                print("Waiting for receive thread to stop...")
                self.recv_thread.join()
                print("Receive thread stopped!")
            else: print("Skipping join on recv_thread (self-join)")

        self.sock.close()
        print("Connection closed!")


if __name__ == "__main__":
    found_matches = MatchSearch().discover_matches()
    for match in found_matches:
        print(match)

    if found_matches:
        target_port = int(input('Enter the port of the game you want to attack: '))
        target_address = ("127.0.0.1", target_port)

        attack = Attack(target_port, target_address)
        while attack.is_running:
            message = input("\nEnter message ('QUIT' to stop): ")
            attack.spoof_message(message)
