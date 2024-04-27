import socket

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Get user input for message to send
    message = input("Enter message: ")

    # Send message to server
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    # Receive response from server
    response, server_address = client_socket.recvfrom(1024)
    print(f"Received from server: {response.decode()}")