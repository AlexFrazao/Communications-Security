import socket
import os
import subprocess

SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

third_party_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if not os.path.exists('third_party'):
    os.makedirs('third_party')

message = "Third Party created."
third_party_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

while True:
    players_number, server_address = third_party_socket.recvfrom(1024)
    players_directory = f'player_{players_number}'
    
    """ subprocess.run(['zokrates', 'compile', '-i', 'proof1.zok'], cwd=players_directory)
    subprocess.run(['zokrates', 'setup'], cwd=players_directory) """

third_party_socket.close()