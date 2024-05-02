import socket

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = input("Join Game: ")
client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT)) # Send message to server
shot = input("::")
client_socket.sendto(shot.encode(), (SERVER_IP, SERVER_PORT))

while True:
    # Get user input for message to send
    response, server_address = client_socket.recvfrom(1024)
    
    if (response):
        response = response.decode().split()
        # Receive response from server
        print(f"You received a shoot at ({response[2]},{response[3]})")
        
        message = input("::")
        client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
