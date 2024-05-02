# coordinates (x, y)
# (0, 0) bottom left
# (9, 9) top right

boards = [
	[
		[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], # Carrier
		[(0, 1), (1, 1), (2, 1), (3, 1)], # Battleship
		[(0, 2), (1, 2), (2, 2)], # Destroyer
		[(0, 3), (1, 3)], # Cruiser 1
		[(0, 4), (1, 4)], # Cruiser 2
		[(0, 5)], # Submarine 1
		[(0, 6)], # Submarine 1
	],
	[
		[(5, 9), (6, 9), (7, 9), (8, 9), (9, 9)], # Carrier
		[(6, 8), (7, 8), (8, 8), (9, 8)], # Battleship
		[(7, 7), (8, 7), (9, 7)], # Destroyer
		[(8, 6), (9, 6)], # Cruiser 1
		[(8, 5), (9, 5)], # Cruiser 2
		[(9, 4)], # Submarine 1
		[(9, 3)], # Submarine 1
	],
]