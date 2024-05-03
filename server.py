import socket
import sys
import subprocess
import time

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
number_of_players = int(input("Number of Players: "))

# List to store addresses of players currently in the game
ingame_players = []
timeof_play = []
time_since_last_play = []

try:

    # Start player0.py
    subprocess.Popen(['/usr/bin/python3', 'player1.py'])

    for i in range(number_of_players-1):
        subprocess.Popen(['/usr/bin/python3', 'players.py'])

    while True:
        # Receive message from player
        """ after the 'sunk' message is staying here. I think is to wait for another message"""
        data, player_address = server_socket.recvfrom(1024)
        # Checks if it's a new player
        if player_address not in ingame_players:
            ingame_players.append(player_address)
            print(f"Player {ingame_players.index(player_address)} joined.")
            timeof_play.append(time.time())
        player_message = data.decode().split()
        if len(player_message) >= 4 and player_message[0] == "shoot":
            target_player_index = int(player_message[1])
            x_coordinate = player_message[2]
            y_coordinate = player_message[3]

            print(f"Player {ingame_players.index(player_address)} shoots player {target_player_index} at ({x_coordinate}, {y_coordinate})")
            
            if len(player_message) > 4:  # Check if attack_report is included
                report = player_message[4]
                print(f"{report}")
            
            target_player_message = f"{target_player_index} {player_message[0]} {x_coordinate} {y_coordinate}"
            target_player_address = ingame_players[target_player_index]
            server_socket.sendto(target_player_message.encode(), target_player_address)
            
            attack_report, player_address = server_socket.recvfrom(1024)
            timeof_play[target_player_index] = time.time()

            print(f"{attack_report.decode()}")
        
        elif (player_message == "sunk"):
            for player_index, last_play_time in timeof_play:
                time_since_last_play[player_index] = time.time() - last_play_time
            player_with_highest_time = max(time_since_last_play, key=time_since_last_play.get)
            print(player_with_highest_time)
            continue

        response = ""
        server_socket.sendto(response.encode(), player_address)

except KeyboardInterrupt:
    print("Server stopped.")
    # Clean up ingame_players list
    ingame_players.clear()
    server_socket.close()
    sys.exit(0)