import socket
import time
import os
import subprocess
import sys

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send message to server
    player_socket.sendto("Ready".encode(), (SERVER_IP, SERVER_PORT)) # Send message to server
    player_number, server_address = player_socket.recvfrom(1024)
    player_number = player_number.decode()
    player_directory = f"player_{player_number}"

    player_zokcode = """
    def main(private field a, field b) {
        assert(a * a == b);
        return;
    } 
    """

    with open(f"{player_directory}/root{player_number}.zok", 'w') as file:
        file.write(player_zokcode)
    subprocess.run(['zokrates', 'compile', '-i', f'root{player_number}.zok'], cwd=player_directory)
    subprocess.run(['zokrates', 'setup'], cwd=player_directory)
    subprocess.run(['zokrates', 'compute-witness', '-a', '337', '113569'], cwd=player_directory)
    subprocess.run(['zokrates', 'generate-proof'], cwd=player_directory)

    """ ships = [
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], # Carrier
            [(0, 1), (1, 1), (2, 1), (3, 1)], # Battleship
            [(0, 2), (1, 2), (2, 2)], # Destroyer
            [(0, 3), (1, 3)], # Cruiser 1
            [(0, 4), (1, 4)], # Cruiser 2
            [(0, 5)], # Submarine 1
            [(0, 6)], # Submarine 1
        ] """

    ships = [
            [(0, 0)] # Submarine 1
        ]

    while True:
        # Get user input for message to send
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