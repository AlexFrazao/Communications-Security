import socket
import time
import subprocess
import sys
import json

from proofs import proof_main

def write_proof_in_players_file(proof_number):
    proof_request = {
        "proof_name": f"proof{proof_number}_zok"
    }
    proof_result_str = proof_main(json.dumps(proof_request))
    proof_result = json.loads(proof_result_str)

    # Example: write the proof to a file if successful
    if proof_result["status"] == "success":
        proof_data = proof_result["proof"]
        with open(f"{player_directory}/proof{proof_number}/proof{proof_number}.zok", 'w') as file:
            file.write(proof_data)

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player_socket.sendto("Ready".encode(), (SERVER_IP, SERVER_PORT))
players_information, server_address = player_socket.recvfrom(1024)
players_information = players_information.decode().split()
player_directory = f"player_{players_information[0]}"

write_proof_in_players_file(1)
write_proof_in_players_file(2)
write_proof_in_players_file(3)

time.sleep(int(players_information[1])*25)
subprocess.run(['zokrates', 'compute-witness', '-a', '0','0','1','0','2','0','3','0','4','0','0','1','1','1','2','1','3','1','0','2','1','2','2','2','0','3','1','3','0','4','1','4','0','5','0','6','5'], cwd=f"{player_directory}/proof1")
subprocess.run(['zokrates', 'generate-proof'], cwd=f"{player_directory}/proof1")

time.sleep(int(players_information[1])*4)
shot = input(f"Player{players_information[0]}:: ")
player_socket.sendto(shot.encode(), (SERVER_IP, SERVER_PORT))

ships = [
		[(0, 0)] # Submarine 1
	]

try:
    while True:
        response, server_address = player_socket.recvfrom(1024)

        if response:
            response = response.decode().split()
            # Receive response from server
            #print(f"You received a shoot at ({response[2]}, {response[3]})")
            hit_flag = False
            ship_sunk = False

            hit_coordinates = (int(response[2]), int(response[3]))
            # Check if a ship square was hitted

            for ship in ships:
                for ship_coordinates in ship:
                    if hit_coordinates == ship_coordinates:
                        attack_report = " Hit"
                        print("Hit")
                        hit_flag = True
                        #print(attack_report)
                        # Remove the destroyed ship square from the coordinates
                        ship.remove(hit_coordinates)
                        if not ship:
                            attack_report = "sunk"
                            print("sunk")
                            ship_sunk = True
                        break
            
                if hit_flag == False:
                    print("water")
                    attack_report = " Water"
                    #print(attack_report)

            if ship_sunk == True:
                player_socket.sendto(attack_report.encode(), (SERVER_IP, SERVER_PORT))
            else:
                player_socket.sendto(attack_report.encode(), (SERVER_IP, SERVER_PORT))

                time.sleep(0.001)
                message = input(f"Player{players_information[0]}:: ")

                if message.lower() == 'q':
                    break

                player_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    player_socket.close()
    subprocess.run(['rm', '-r', 'player_*'], cwd=player_directory)

except KeyboardInterrupt:
    player_socket.close()
    sys.exit(0)