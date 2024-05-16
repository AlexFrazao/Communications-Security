import socket
import sys
import subprocess
import time
import os

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))

print("Server started...")
number_of_players = int(input("Number of Players: "))

ingame_players = []
timeof_play = []
third_party_created = False

try:
    # Start player0.py
    subprocess.Popen(['python', 'player0.py'])

    for i in range(number_of_players-1):
        subprocess.Popen(['python', 'players.py'])

    while True:
        # Receive message from player
        data, player_address = server_socket.recvfrom(1024)
        # Checks if it's a new player
        if player_address not in ingame_players:
            ingame_players.append(player_address)
            player_number = ingame_players.index(player_address)
            print(f"Player {player_number} joined.")

            player_directory = f"player_{player_number}"
            if not os.path.exists(player_directory):
                os.makedirs(player_directory)

        if third_party_created == False:
            subprocess.Popen(['python', 'third_party.py'])
            third_party_message, third_party_address = server_socket.recvfrom(1024)
            third_party_created = True
            print(third_party_message)
            print(ingame_players)
            """ server_socket.sendto(bytes(str(ingame_players), 'utf-8'), third_party_address) """

            server_socket.sendto(bytes(str(player_number), 'utf-8'), player_address)
            timeof_play.append(time.time())

        player_message = data.decode().split()
        
        if len(player_message) >= 4 and player_message[0] == "shoot":
            attacker = ingame_players.index(player_address)
            target_player_index = int(player_message[1])
            x_coordinate = player_message[2]
            y_coordinate = player_message[3]

            print(f"Player {attacker} shoots player {target_player_index} at ({x_coordinate}, {y_coordinate})")
            
            if len(player_message) > 4:  # Check if attack_report is included
                report = player_message[4]
                print(f"{report}")
            
            target_player_message = f"{target_player_index} {player_message[0]} {x_coordinate} {y_coordinate}"
            target_player_address = ingame_players[target_player_index]
            server_socket.sendto(target_player_message.encode(), target_player_address)
            
            attack_report, player_address = server_socket.recvfrom(1024)
            timeof_play[target_player_index] = time.time()

            if (attack_report.decode() == "sunk"):
                player_timeof_play = []
                for last_play_time in timeof_play:
                    player_timeof_play.append(time.time() - last_play_time)
                highest_time = max(player_timeof_play)
                highest_player_timeof_play = player_timeof_play.index(highest_time)
                player_address = ingame_players[player_timeof_play.index(highest_time)]
                server_socket.sendto("11 shoot 11 11".encode(), player_address)
                continue

        server_socket.sendto("".encode(), player_address)

except KeyboardInterrupt:
    print("Server stopped.")
    # Clean up ingame_players list
    ingame_players.clear()
    server_socket.close()
    sys.exit(0)
