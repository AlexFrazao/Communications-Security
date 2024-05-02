from ships import Ship, Carrier, Battleship, Destroyer, Cruiser, Submarine
from boards import boards

class Player:
	def __init__(self):
		super(Player, self).__init__()

	def set_board(self, board_number):
		coordinates = boards[board_number]
		self.carrier = Carrier()
		self.carrier.set_position(coordinates[0])
		self.battleship = Battleship()
		self.battleship.set_position(coordinates[1])
		self.destroyer = Destroyer()
		self.destroyer.set_position(coordinates[2])
		self.cruiser1 = Cruiser(1)
		self.cruiser1.set_position(coordinates[3])
		self.cruiser2 = Cruiser(2)
		self.cruiser2.set_position(coordinates[4])
		self.submarine1 = Submarine(1)
		self.submarine1.set_position(coordinates[5])
		self.submarine2 = Submarine(2)
		self.submarine2.set_position(coordinates[6])