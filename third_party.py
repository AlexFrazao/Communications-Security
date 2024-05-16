import socket
import sys
import subprocess
import time
import os

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

third_party_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if not os.path.exists('third_party'):
    os.makedirs('third_party')

third_party_socket.sendto("Third Party created.".encode(), (SERVER_IP, SERVER_PORT)) 

""" subprocess.run(['zokrates', 'compile', '-i', f'proof1.zok'], cwd='third_party')
subprocess.run(['zokrates', 'setup'], cwd=server_directory) """
