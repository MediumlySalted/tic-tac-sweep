import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.0.0.15', 27612))

message = "Hello, Server!"
client_socket.sendall(message.encode())

response = client_socket.recv(1024)
print(f"Server response: {response.decode()}")

client_socket.close()
