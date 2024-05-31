import socket
import os
import subprocess
import time

def third_party_compile_proof(proof_number):
    subprocess.run(['zokrates', 'compile', '-i', f'proof{proof_number}.zok'], cwd=f"{player_directory}/proof{proof_number}")
    subprocess.run(['zokrates', 'setup'], cwd=f"{player_directory}/proof{proof_number}")

SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

third_party_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if not os.path.exists('third_party'):
    os.makedirs('third_party')

message = "Third Party created."
third_party_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

while True:
    player_directory, server_address = third_party_socket.recvfrom(1024)
    player_directory = player_directory.decode()
    print(f"\t\t\t\tthird_party.py | perfoming compilations {player_directory}")

    third_party_compile_proof(1)
    third_party_compile_proof(2)
    third_party_compile_proof(3)

    subprocess.run(['touch', f'{player_directory}/proof3/done.txt'])
    print(f"\t\tthird_party.py | generated .txt in {player_directory}")

third_party_socket.close()