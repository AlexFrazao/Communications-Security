import socket
import time
import subprocess
import sys
import json

from proofs import proof_main

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player_socket.sendto("Ready".encode(), (SERVER_IP, SERVER_PORT)) # Send message to server
player_number, server_address = player_socket.recvfrom(1024)
player_number = player_number.decode()
player_directory = f"player_{player_number}"

# Request proof using the proof function
proof_request = {
    "proof_name": "proof1_zok"  # Specify which proof is needed
}
proof_result_str = proof_main(json.dumps(proof_request))
proof_result = json.loads(proof_result_str)

# Example: write the proof to a file if successful
if proof_result["status"] == "success":
    proof_data = proof_result["proof"]
    with open(f"{player_directory}/proof1.zok", 'w') as file:
        file.write(proof_data)

""" subprocess.run(['zokrates', 'compute-witness', '-a', '337', '113569'], cwd=player_directory)
subprocess.run(['zokrates', 'generate-proof'], cwd=player_directory) """

time.sleep(0.7)
shot = input(f"Player{player_number}:: ")
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
                message = input(f"Player{player_number}:: ")

                if message.lower() == 'q':
                    break

                player_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    # Close the client socket
    player_socket.close()

except KeyboardInterrupt:
    player_socket.close()
    sys.exit(0)