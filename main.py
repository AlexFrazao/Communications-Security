# Import necessary modules
from server import Server
from player_node import PlayerNode

def main():
    # Initialize server
    server = Server()
    
    # Initialize player nodes
    player1 = PlayerNode(player_id=1)
    player2 = PlayerNode(player_id=2)

    # Example of accessing player fleet
    print("Player 1 Fleet:", player1.fleet)
    print("Player 2 Fleet:", player2.fleet)
    
    # Start the game
    server.start_game(player1, player2)
    
if __name__ == "__main__":
    main()