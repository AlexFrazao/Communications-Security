'''
1. The Carrier - 5 squares (1 pcs)
2. The Battleship - 4 squares (1 pcs)
3. The Destroyer - 3 squares (1 pcs)
4. The Cruiser - 2 squares (2 pcs)
5. The Submarine - 1 square (2 pcs)
'''

class Ship:
	def __init__(self, name, length):
		self.name = name
		self.length = length

	def set_position(self, position):
		self.position = position

	def get_position(self):
		print(self.name + " is at position " + str(self.position))

class Carrier(Ship):
	def __init__(self):
		super().__init__(name="Carrier", length=5)

class Battleship(Ship):
	def __init__(self):
		super().__init__(name="Battleship", length=4)
		
class Destroyer(Ship):
	def __init__(self):
		super().__init__(name="Destroyer", length=3)
		
class Cruiser(Ship):
	def __init__(self, number):
		super().__init__(name="Cruiser", length=2)
		self.number = number

	def get_position(self):
		print(self.name + " " + str(self.number) + " is at position " + str(self.position))
		
class Submarine(Ship):
	def __init__(self, number):
		super().__init__(name="Submarine", length=1)
		self.number = number

	def get_position(self):
		print(self.name + " " + str(self.number) + " is at position " + str(self.position))