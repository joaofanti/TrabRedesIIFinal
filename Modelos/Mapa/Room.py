"""
	Define uma sala.
"""
class Room:

	ID = 1			# Identificador da sala.
	Players = []	# Lista dos players que estao na sala atualmente
	Doors = []		# Lista de tuplas de [porta, direcao]
	Objects = []	# Lista de objetos da sala
	Initial = False	# Eh sala inicial do jogo

	"""
		Cria uma nova instancia de porta.
	"""
	def __init__(self, id, initial, doors, objects):
		self.ID = id
		self.Initial = initial
		self.Doors = doors
		self.Objects = objects

	"""
	"""
	def ToString(self):
		currPlayers = ', '.join(self.Players)

		currDoors = ""
		for door in self.Doors:
			currDoors += door.ToString()

		currObjects = ""
		for roomObject in self.Objects:
			currDoors += roomObject.ToString()
		result = "Sala #" + self.ID
		if (self.Initial):
			result += " (sala inicial)"
		result += ":"
		result += "\nJogadores: " + currPlayers
		result += "\nPortas: " + currDoors
		result += "\nObjetos: " + currObjects

		return result