import socket
from socket import timeout as TimeoutException
import subprocess
import time
import os
import sys
import json

subprocess.run(['rm', '-r', 'lobby*'])

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))

""" import signal
from functools import wraps

class TimeOutError(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeOutError()

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@timeout(seconds=300) """
def wait_for_challenge(win_stater_number, ingame_players, lobby_list):
    executed = False 
    while True: 
        if not executed:
            server_socket.settimeout(30)
            lobby_number = 0

            for lobby in lobby_list:
                print("1")
                print(lobby_list, lobby)
                for player_number in lobby:
                    print("2")
                    print(player_number, lobby)
                    if win_stater_number == player_number:
                        print("3")
                        print(win_stater_number, player_number)
                        challenge_lobby_number = lobby_number
                        print("lobby number:", lobby_number)
                        for player_number in lobby:
                            print("4")
                            if win_stater_number == player_number:
                                continue
                            else:
                                player_address = ingame_players[player_number]
                                print(player_address)
                                server_socket.sendto("win_confrontation".encode(), player_address)
                lobby_number += 1
            executed = True

        data, player_address = server_socket.recvfrom(1024)
        player_message = data.decode().split()

        if len(player_message) == 1 and player_message[0] == "y":

            challenger = ingame_players.index(player_address)
            challenger_directory = f'lobby_{challenge_lobby_number}/player_{challenger}'
            server_socket.sendto("win_check".encode(), player_address)

            print(f"Player {challenger} responded to the challenge.")

            proof_number = 3
            wait_for_player_witness_and_proof(challenger_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{challenger_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{challenger_directory}/proof{proof_number}/done.txt'])
            print(f'##5server.py | created {challenger_directory}/proof{proof_number}/done.txt')

            if fleet_is_sunk(challenger_directory):
                print(f'Player {challenger} has no boats left.')
            else:
                print(f"Player {challenger} successfully responded to the challenge! \nTherefore, it's his turn to shoot.")
                return player_address
        else:
            continue

def fleet_is_sunk(challenger_directory):
    file = open(f'{challenger_directory}/proof3/proof.json', 'r')
    content = json.load(file)
    file.close()
    if int(content['inputs'][0], 16) == 0:
        return True
    return False

print("Server started...")

ingame_players = []
timeof_play = []
third_party_created = False
number_of_proofs1_verified = 0
number_of_lobbys = 0
lobby_list = []

def wait_for_player_witness_and_proof(player_directory, proof_number):
    print(f"##1server.py | waiting {player_directory}/proof{proof_number}/done.txt.")

    proof_file = f'{player_directory}/proof{proof_number}/done.txt'
    while not os.path.exists(proof_file):
        time.sleep(0.1)
    subprocess.run(['rm', 'done.txt'], cwd=f'{player_directory}/proof{proof_number}')

    print(f"##2server.py | deleted {player_directory}/proof{proof_number}/done.txt.")

try:
    subprocess.Popen(['python', 'third_party.py'])
    third_party_message, third_party_address = server_socket.recvfrom(1024)
    print(third_party_message.decode())

    while True:
        data, player_address = server_socket.recvfrom(1024)

        if player_address not in ingame_players:
            ingame_players.append(player_address)
            player_number = ingame_players.index(player_address)
            print(f"Player {player_number} joined.")

            server_socket.sendto(json.dumps(lobby_list).encode(), player_address)
            
            player_create_or_join_lobby, player_address = server_socket.recvfrom(1024)
            player_create_or_join_lobby = player_create_or_join_lobby.decode()
            if player_create_or_join_lobby == "c":
                lobby_directory = f'lobby_{len(lobby_list)}'
                lobby_list.append([player_number])
                number_of_lobbys += 1
                print(f"Player {player_number} created {lobby_directory}")
            else:
                lobby_number = int(player_create_or_join_lobby)
                lobby_directory = f'lobby_{lobby_number}'
                lobby_list[lobby_number].append(player_number)
                
            player_directory = f"{lobby_directory}/player_{player_number}"
            
            if not os.path.exists(player_directory):
                os.makedirs(player_directory)
                for i in range(3):
                    os.makedirs(f'{player_directory}/proof{i+1}')

            server_socket.sendto(bytes(f"{player_number} {player_directory}", 'utf-8'), player_address)
            server_socket.sendto(bytes(str(player_directory), 'utf-8'), third_party_address)
            timeof_play.append(time.time())

        if number_of_proofs1_verified < len(ingame_players):
            proof_number = 1
            wait_for_player_witness_and_proof(player_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{player_directory}/proof1')
            subprocess.run(['touch', f'{player_directory}/proof1/done.txt'])
            print(f"##3server.py | created {player_directory}/proof1/done.txt")
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

            target_player_directory = f'{lobby_directory}/player_{target_player_index}'
            proof_number = 2
            wait_for_player_witness_and_proof(target_player_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{target_player_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{target_player_directory}/proof{proof_number}/done.txt'])
            print(f'##4server.py | created {target_player_directory}/proof{proof_number}/done.txt')

            proof_number = 3
            wait_for_player_witness_and_proof(target_player_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{target_player_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{target_player_directory}/proof{proof_number}/done.txt'])
            print(f'##5server.py | created {target_player_directory}/proof{proof_number}/done.txt')

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

        elif len(player_message) == 1 and player_message[0] == "win":
            win_stater_address = player_address
            win_stater_number = ingame_players.index(win_stater_address)
            win_stater_directory = f'{lobby_directory}/player_{win_stater_number}'

            print(f"Player {win_stater_number} states that he won.")

            server_socket.sendto("win_check".encode(), win_stater_address)
            
            proof_number = 3
            wait_for_player_witness_and_proof(win_stater_directory, proof_number)
            subprocess.run(['zokrates', 'verify'], cwd=f'{win_stater_directory}/proof{proof_number}')
            subprocess.run(['touch', f'{win_stater_directory}/proof{proof_number}/done.txt'])
            print(f'##server.py | created {win_stater_directory}/proof{proof_number}/done.txt')

            if fleet_is_sunk(win_stater_directory):
                print(f'Player {win_stater_number} has no boats left. \nThe battle continues.')

            else:
                print(f'Player {win_stater_number} has some boats left. \nChallenge him in the next 5 min to continue the battle!')

                try:
                    player_address = wait_for_challenge(win_stater_number, ingame_players, lobby_list)
                    server_socket.sendto(f"11 shoot 11 11".encode(), player_address)
                    continue
                except TimeoutException:
                    print(f'Congradulations! Player {win_stater_number} won!')
                    for address in ingame_players:
                        server_socket.sendto("Player {win_stater_number} won. \nGame over".encode(), address)
                    break

        server_socket.sendto("".encode(), player_address)

except KeyboardInterrupt:
    print("Server stopped.")
    ingame_players.clear()
    server_socket.close()
    sys.exit(0)
