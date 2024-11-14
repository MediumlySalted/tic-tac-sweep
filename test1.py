import socket

def find_server(port, timeout=5):
    # Set up the UDP socket for broadcasting
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.settimeout(timeout)
    
    message = b"DISCOVERY_REQUEST"
    broadcast_address = ('<broadcast>', port)
    udp_socket.sendto(message, broadcast_address)
    print(f"Broadcasting on port {port}...")

    while True:
        try:
            response, server_address = udp_socket.recvfrom(1024)
            if response == b"DISCOVERY_RESPONSE":
                print(f"Server found at {server_address[0]}:{server_address[1]}")
                return server_address[0]
        except socket.timeout:
            print("No server found within the timeout period.")
            break

    udp_socket.close()
    return None

def advertise_server(port):
    # Create a UDP socket to listen for discovery requests
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to the specified port
    udp_socket.bind(('127.0.0.1', port))
    print(f"Listening for discovery requests on port {port}...")

    try:
        while True:
            # Wait for a discovery request from any client
            data, client_address = udp_socket.recvfrom(1024)
            if data == b"DISCOVERY_REQUEST":
                print(f"Discovery request received from {client_address}")
                
                # Respond to the discovery request
                response_message = b"DISCOVERY_RESPONSE"
                udp_socket.sendto(response_message, client_address)
                print("Sent discovery response")
    finally:
        udp_socket.close()

def start_server(port):
    host = '127.0.0.1'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Hosting TCP server on {host}:{port}...")
    
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")
        client_socket.sendall(b"Message received")
    
    client_socket.close()
    server_socket.close()

def connect_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    message = "Hello, Server!"
    client_socket.sendall(message.encode())
    
    response = client_socket.recv(1024)
    print(f"Server response: {response.decode()}")
    
    client_socket.close()

def main(port=27612):
    server_ip = find_server(port)
    
    if server_ip:
        print(f"Connecting to server at {server_ip}:{port}")
        connect_server(server_ip, port)
    else:
        print("No server found. Starting as the host...")
        advertise_server(port)
        start_server(port)


if __name__ == "__main__":
    main()
