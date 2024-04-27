import socket
import sys

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set SO_REUSEADDR option
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to IP and port
server_socket.bind((SERVER_IP, SERVER_PORT))

print("Server started...")

# List to store addresses of players currently in the game
ingame_players = []

try:
    while True:
        # Receive message from player
        data, player_address = server_socket.recvfrom(1024)
        # Checks if it's a new player
        if player_address not in ingame_players:
            ingame_players.append(player_address)
            print(f"Player {ingame_players.index(player_address)} joined.")

        player_request = data.decode().split()

        if len(player_request) >= 4 and player_request[0] == "shoot":
            target_player_index = int(player_request[1])
            x_coordinate = player_request[2]
            y_coordinate = player_request[3]
            
            print(f"Player {ingame_players.index(player_address)} shoots player {target_player_index} at ({x_coordinate}, {y_coordinate})")
            
            target_player_message = f"{ingame_players.index(player_address)} {player_request[0]} {x_coordinate} {y_coordinate}"
            target_player_address = ingame_players[target_player_index]
            server_socket.sendto(target_player_message.encode(), target_player_address)

        response = ""
        server_socket.sendto(response.encode(), player_address)

except KeyboardInterrupt:
    print("Server stopped.")
    # Clean up ingame_players list
    ingame_players.clear()
    server_socket.close()
    sys.exit(0)
