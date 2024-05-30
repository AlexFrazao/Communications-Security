import socket
import subprocess
import time
import os
import sys

subprocess.run(['rm', '-r', 'player_*'])

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))

print("Server started...")

ingame_players = []
timeof_play = []
third_party_created = False
number_of_proofs1_verified = 0
""" number_of_lobbys = 0
lobby_list = [] """

def wait_for_player_witness_and_proof(player_directory, proof_number):
    print(f"##server.py | waiting {player_directory}/proof{proof_number}/done.txt.")

    proof_file = f'{player_directory}/proof{proof_number}/done.txt'
    while not os.path.exists(proof_file):
        time.sleep(0.1)
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof{proof_number}')

    print(f"##server.py | deleted {player_directory}/proof{proof_number}/done.txt.")

try:
    subprocess.Popen(['python', 'third_party.py'])
    third_party_message, third_party_address = server_socket.recvfrom(1024)
    print(third_party_message.decode())
    """ print(f"Number of Lobby's: {lobby_list.len()}") """

    while True:
        data, player_address = server_socket.recvfrom(1024)

        if player_address not in ingame_players:
            ingame_players.append(player_address)
            player_number = ingame_players.index(player_address)
            print(f"Player {player_number} joined.")
            """ player_create_or_join_lobby, player_address = server_socket.recvfrom(1024)

            match player_create_or_join_lobby:
                case "c":
                    lobby_list.append(f"Lobby{lobby_list.len()}")
                    print(f"Player {player_number} created Lobby{lobby_list.len()}.")
                    continue
                case "j":
                    for i in len(lobby_list.len()):
                        print(lobby_list[i])
                    continue
                case _:
                    continue """

            player_directory = f"player_{player_number}"
            if not os.path.exists(player_directory):
                os.makedirs(player_directory)
                for i in range(3):
                    os.makedirs(f"{player_directory}/proof{i+1}")

            server_socket.sendto(bytes(f"{player_number} {len(ingame_players)}", 'utf-8'), player_address)
            server_socket.sendto(bytes(str(player_number), 'utf-8'), third_party_address)
            timeof_play.append(time.time())

        if number_of_proofs1_verified < len(ingame_players):
            player_directory = f"player_{player_number}"
            proof_number = 1
            wait_for_player_witness_and_proof(player_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{player_directory}/proof1')
            subprocess.run(['touch', f'{player_directory}/proof1/done.txt'])
            print(f"##server.py | created {player_directory}/proof1/done.txt")
            number_of_proofs1_verified += 1

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

            target_player_directory = f'player_{target_player_index}'
            proof_number = 2
            wait_for_player_witness_and_proof(target_player_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{target_player_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{target_player_directory}/proof{proof_number}/done.txt'])
            print(f'##server.py | created {target_player_directory}/proof{proof_number}/done.txt')

            proof_number = 3
            wait_for_player_witness_and_proof(target_player_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{target_player_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{target_player_directory}/proof{proof_number}/done.txt'])
            print(f'##server.py | created {target_player_directory}/proof{proof_number}/done.txt')

            attack_report, player_address = server_socket.recvfrom(1024)
            print(attack_report.decode())
            timeof_play[target_player_index] = time.time()

            if (attack_report.decode() == "sunk"):
                player_timeof_play = []
                for last_play_time in timeof_play:
                    player_timeof_play.append(time.time() - last_play_time)
                highest_time = max(player_timeof_play)
                highest_player_timeof_play = player_timeof_play.index(highest_time)
                player_address = ingame_players[highest_player_timeof_play]
                server_socket.sendto("11 shoot 11 11".encode(), player_address)
                continue

        server_socket.sendto("".encode(), player_address)

except KeyboardInterrupt:
    print("Server stopped.")
    ingame_players.clear()
    server_socket.close()
    sys.exit(0)
