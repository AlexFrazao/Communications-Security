import socket
import time

# Define server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto("Ready".encode(), (SERVER_IP, SERVER_PORT)) # Send message to server

time.sleep(0.1)
shot = input("Player0::")
client_socket.sendto(shot.encode(), (SERVER_IP, SERVER_PORT))

ships = [
		[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], # Carrier
		[(0, 1), (1, 1), (2, 1), (3, 1)], # Battleship
		[(0, 2), (1, 2), (2, 2)], # Destroyer
		[(0, 3), (1, 3)], # Cruiser 1
		[(0, 4), (1, 4)], # Cruiser 2
		[(0, 5)], # Submarine 1
		[(0, 6)], # Submarine 1
	]

""" ships = [
		[(0, 0)] # Submarine 1
	] """

while True:
    # Get user input for message to send
    response, server_address = client_socket.recvfrom(1024)

    if response:
        if not ships:
            response = response.decode().split()
            # Receive response from server
            #print(f"You received a shoot at ({response[2]}, {response[3]})")
            hit_flag = False

            hit_coordinates = (int(response[2]), int(response[3]))
            # Check if a ship square was hitted
            for ships in ships:
                for ship_coordinates in ships:
                    if hit_coordinates == ship_coordinates:
                        attack_report = " Hit"
                        hit_flag = True
                        #print(attack_report)
                        # Remove the destroyed ship square from the coordinates
                        ships.remove(hit_coordinates)
                        break
                    
            if hit_flag == False:
                attack_report = " Water"
                #print(attack_report)

            client_socket.sendto(attack_report.encode(), (SERVER_IP, SERVER_PORT))

            time.sleep(0.001)
            message = input("Player0:: ")
            if message.lower() == 'q':
                break
        else:
            message = "sunk"
            
        client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))


# Close the client socket
client_socket.close()
