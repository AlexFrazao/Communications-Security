import socket
import time
import subprocess
import sys
import json
import os

from proofs import proof_main

def set_hash_to_file(proof_number):
    file = open(f"{player_directory}/proof{proof_number}/proof.json")
    content = json.load(file)
    file.close()

    with open(f"{player_directory}/hash.json", 'w+') as output_file:
        json.dump(content['inputs'], output_file)

def write_proof_in_players_file(proof_number):
    proof_request = {
        "proof_name": f"proof{proof_number}_zok"
    }
    proof_result_str = proof_main(json.dumps(proof_request))
    proof_result = json.loads(proof_result_str)

    if proof_result["status"] == "success":
        proof_data = proof_result["proof"]
        with open(f"{player_directory}/proof{proof_number}/proof{proof_number}.zok", 'w') as file:
            file.write(proof_data)

def wait_server_proof_verification(player_directory, proof_number):
    print(f"##players.py | {player_directory} waiting server {player_directory}/proof{proof_number}/done.txt")

    proof_file = f'{player_directory}/proof{proof_number}/done.txt'
    time.sleep(2)
    while not os.path.exists(proof_file):
        time.sleep(0.1)
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof{proof_number}')

    print(f"##players.py | {player_directory} deleted {player_directory}/proof{proof_number}/done.txt")

def wait_for_third_party(player_directory):
    print(f"##players.py | {player_directory} waiting third_party {player_directory}/proof3/done.txt")

    proof_file = f'{player_directory}/proof3/done.txt'
    while not os.path.exists(proof_file):
        time.sleep(0.1)
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof3')

    print(f"##players.py | {player_directory} deleted {player_directory}/proof3/done.txt")

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player_socket.sendto("Ready".encode(), (SERVER_IP, SERVER_PORT)) # Send message to server

player_create_or_join_lobby = input("Create or join a lobby [C/J]?")
while True:
    print("1")
    if player_create_or_join_lobby.lower() == "j":
        player_socket.sendto(player_create_or_join_lobby.lower().encode(), (SERVER_IP, SERVER_PORT))
        print("2")
        lobby_list, server_address = player_socket.recvfrom(1024)
        print("3")
        lobby_list = json.loads(lobby_list.decode())
        if len(lobby_list) != 0:
            print("4")
            for i in lobby_list:
                print(lobby_list[i])
            lobby_to_join_player = input("lobby number:")
            player_socket.sendto(lobby_to_join_player.encode(), (SERVER_IP, SERVER_PORT))
            break
        else:
            print("No lobbys available.")
            create_or_join_lobby = input("Create a lobby [C]?")
            player_socket.sendto(create_or_join_lobby.lower().encode(), (SERVER_IP, SERVER_PORT))
            break
    elif player_create_or_join_lobby.lower() == "c":
        print("4")
        break


players_information, server_address = player_socket.recvfrom(1024)
players_information = players_information.decode().split()
player_number = players_information[0]
number_of_players = players_information[1]
last_player_directory = f'player_{int(number_of_players) - 1}'

player_directory = f"player_{player_number}"

write_proof_in_players_file(1)
write_proof_in_players_file(2)
write_proof_in_players_file(3)

fleet = [
    [0, 0], [1, 0], [2, 0], [3, 0], [4, 0],
    [0, 1], [1, 1], [2, 1], [3, 1],
    [0, 2], [1, 2], [2, 2],
    [0, 3], [1, 3],
    [0, 4], [1, 4],
    [0, 5],
    [0, 6]
]

nonce = 5

wait_for_third_party(player_directory)
subprocess.run(['python', 'compute_witness.py', '1', json.dumps(fleet), str(nonce), player_number])
subprocess.run(['zokrates', 'generate-proof'], cwd=f'{player_directory}/proof1')
set_hash_to_file(proof_number=1)
subprocess.run(['touch', f'{player_directory}/proof1/done.txt'])

wait_server_proof_verification(player_directory, proof_number=1)

if int(player_number) == 0:
    shot = input(f"Player{player_number}:: ")
    player_socket.sendto(shot.encode(), (SERVER_IP, SERVER_PORT))
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof1')
    print(f"\t\t\t\tplayers.py | deleted {player_directory}/proof1/done.txt")

initialization = True

try:
    while True:
        data, server = player_socket.recvfrom(1024)
        message = data.decode().split()

        if len(message) == 0 and initialization == True:
            player_socket.sendto("Ready".encode(), (SERVER_IP, SERVER_PORT))
            initialization = False

        elif message[1] == "shoot":
            target_player_index = message[0]
            x_coordinate = int(message[2])
            y_coordinate = int(message[3])
            hit_coordinates = [x_coordinate, y_coordinate]
            
            report = f"Player {player_number} shooting player {target_player_index} at ({x_coordinate}, {y_coordinate})"
            print(report)

            proof_number = 2
            subprocess.run(['python', 'compute_witness.py', f'{proof_number}', json.dumps(hit_coordinates), json.dumps(fleet), str(nonce), player_number])
            subprocess.run(['zokrates', 'generate-proof'], cwd=f'{player_directory}/proof{proof_number}')
            set_hash_to_file(proof_number=2)
            subprocess.run(['touch', f'{player_directory}/proof{proof_number}/done.txt'])
            print(f"\t\t\t\tplayers.py | created {player_directory}/proof{proof_number}/done.txt")
            wait_server_proof_verification(player_directory, proof_number)

            proof_number = 3
            subprocess.run(['python', 'compute_witness.py', f'{proof_number}', json.dumps(fleet), player_number])
            subprocess.run(['zokrates', 'generate-proof'], cwd=f'{player_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{player_directory}/proof{proof_number}/done.txt'])
            print(f"\t\t\t\tplayers.py | created {player_directory}/proof{proof_number}/done.txt")
            wait_server_proof_verification(player_directory, proof_number)

            for i, ship_coordinates in enumerate(fleet):
                if hit_coordinates == ship_coordinates:
                    attack_report = "Hit"
                    print(attack_report)
                    hit_flag = True
                    fleet[i] = [11, 11]
                    break

            if not hit_flag:
                attack_report = "Water"
                print(attack_report)
            
            print(fleet)

            player_socket.sendto(attack_report.encode(), (SERVER_IP, SERVER_PORT))

            time.sleep(0.001)
            message = input(f"Player{player_number}:: ")
            player_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

        else:
            print(message)

except KeyboardInterrupt:
    print("hello")
    sys.exit(0)
