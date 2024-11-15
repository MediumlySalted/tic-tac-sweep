import socket
import threading
import random
import sys
import select

def find_server(port, timeout=1):
    # Set up the UDP socket for broadcasting
    timeout += round(random.uniform(0, 2), 3) # Randomizes timeout to prevent sync'd searches
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.settimeout(timeout)

    message = b"DISCOVERY_REQUEST"
    broadcast_address = ('<broadcast>', port)
    udp_socket.sendto(message, broadcast_address)
    print(f"\nSearching for servers on port [{port}]...")

    server_ip = None
    while not server_ip:
        try:
            response, server_address = udp_socket.recvfrom(1024)
            if response == b"DISCOVERY_RESPONSE":
                print(f"Server found at [{server_address[0]}:{server_address[1]}].")
                server_ip = server_address[0]
                
        except socket.timeout:
            print("No server found within the timeout period.")
            break

    udp_socket.close()
    return server_ip

def advertise_server(port, timeout=8):
    # Create a UDP socket to listen for discovery requests
    timeout += round(random.uniform(0, 2), 3) # Randomizes timeout to prevent sync'd searches
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.settimeout(timeout)
    udp_socket.bind(('', port))
    print(f"\nListening for clients on port {port}...")

    client_ip = None
    while not client_ip:
        try:
            data, client_address = udp_socket.recvfrom(1024)
            if data == b"DISCOVERY_REQUEST":
                print(f"Client found at [{client_address}].")
                response_message = b"DISCOVERY_RESPONSE"
                udp_socket.sendto(response_message, client_address)
                client_ip = client_address[0]

        except socket.timeout:
            print("No client found within the timeout period.")
            break

    udp_socket.close()
    return client_ip

def recieve_messages(connection, stop_communication):
    connection.settimeout(1)
    while not stop_communication.is_set():
        try:
            message = connection.recv(1024).decode()
            if message == "q":
                print("Connection has been terminated.")
                stop_communication.set()
                return
            if message and not stop_communication.is_set(): print(f"Received: {message}")
        except socket.timeout:
            continue

def send_messages(connection, stop_communication):
    print('-' * 50)
    print('\nReady to send messages.')
    print('Enter anything to send or "q" to quit\n')
    print('-' * 50)
    while not stop_communication.is_set():
        message = input()
        if not stop_communication.is_set(): connection.sendall(message.encode())
        if message == "q":
            print("You have terminated the connection.")
            stop_communication.set()
            return

def message_handler(connection):
    stop_communication = threading.Event()
    receive_thread = threading.Thread(target=recieve_messages, args=(connection, stop_communication))
    send_thread = threading.Thread(target=send_messages, args=(connection, stop_communication))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    connection.close()
    print("Connection closed")

def start_server(port):
    print(f"\nHosting TCP server on port {port}...")
    host = ''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with [{client_address}].")

    message_handler(client_socket)
    server_socket.close()
    print("Server closed.")

def connect_server(host, port):
    print(f"\nConnecting to server at [{host}:{port}].")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message_handler(client_socket)


def main(port=7212):
    ip = None
    while not ip:
        ip = find_server(port)
        if ip:
            connect_server(ip, port)
        else:
            ip = advertise_server(port)
            if ip: start_server(port)


if __name__ == "__main__":
    main()
