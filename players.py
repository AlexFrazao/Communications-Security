import socket
import time
import subprocess
import sys
import json
import os

from proofs import proof_main

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
    print(f"\t\t\t\tplayers.py | {player_directory} waiting server {player_directory}/proof{proof_number}/done.txt")
    
    proof_file = f'{player_directory}/proof{proof_number}/done.txt'
    time.sleep(2)
    while not os.path.exists(proof_file):
        time.sleep(0.1)
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof{proof_number}')
    
    print(f"\t\t\t\tplayers.py | {player_directory} deleted {player_directory}/proof{proof_number}/done.txt")

def wait_for_third_party(player_directory):
    print(f"\t\t\t\tplayers.py | {player_directory} waiting third_party {player_directory}/proof3/done.txt")

    proof_file = f'{player_directory}/proof3/done.txt'
    while not os.path.exists(proof_file):
        time.sleep(0.1)
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof3')
    
    print(f"\t\t\t\tplayers.py | {player_directory} deleted {player_directory}/proof3/done.txt")

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player_socket.sendto("Ready".encode(), (SERVER_IP, SERVER_PORT)) # Send message to server
players_information, server_address = player_socket.recvfrom(1024)
players_information = players_information.decode().split()
player_number = players_information[0]
number_of_players = players_information[1]
last_player_directory=f'player_{int(number_of_players)-1}'

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
subprocess.run(['touch', f'{player_directory}/proof1/done.txt'])    # signalize to server witness and proof have been generated
print(f"\t\t\t\tplayers.py | created {player_directory}/proof1/done.txt")

if int(number_of_players) > 1:
    proof_number = 1
    wait_server_proof_verification(last_player_directory, proof_number)

is_first_player = len(sys.argv) > 1 and sys.argv[1] == '1'
if is_first_player:
    time.sleep(int(number_of_players) * 4)
    shot = input(f"Player{player_number}:: ")
    player_socket.sendto(shot.encode(), (SERVER_IP, SERVER_PORT))
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof1')
    print(f"\t\t\t\tplayers.py | deleted {player_directory}/proof1/done.txt")

try:
    while True:
        response, server_address = player_socket.recvfrom(1024)

        if response:
            response = response.decode().split()
            hit_flag = False
            ship_sunk = False                              
            hit_coordinates = [int(response[2]), int(response[3])]

            proof_number = 2
            subprocess.run(['python', 'compute_witness.py', f'{proof_number}', json.dumps(hit_coordinates), json.dumps(fleet), str(nonce), player_number])
            subprocess.run(['zokrates', 'generate-proof'], cwd=f'{player_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{player_directory}/proof{proof_number}/done.txt'])
            print(f"\t\t\t\tplayers.py | created {player_directory}/proof{proof_number}/done.txt")
            wait_server_proof_verification(player_directory, proof_number)

            proof_number = 3
            subprocess.run(['python', 'compute_witness.py', f'{proof_number}', json.dumps(fleet), player_number])
            subprocess.run(['zokrates', 'generate-proof'], cwd=f'{player_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{player_directory}/proof{proof_number}/done.txt'])
            print(f"\t\t\t\tplayers.py | created {player_directory}/proof{proof_number}/done.txt")
            wait_server_proof_verification(player_directory, proof_number)

            time.sleep(0.001)
            message = input(f"Player{player_number}:: ")

            if message.lower() == 'q':
                break

            player_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    player_socket.close()
    subprocess.run(['rm', '-r', 'player_*'], cwd=player_directory)

except KeyboardInterrupt:
    player_socket.close()
    sys.exit(0)
