"""
	Define uma sala.
"""
class Room:

	ID = 1			# Identificador da sala.
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
		currDoors = ""
		for door in self.Doors:
			currDoors += door.ToString() + "\n"

		currObjects = ""
		for roomObject in self.Objects:
			currObjects += roomObject.ToString() + "\n"
		result = "Sala #" + str(self.ID)
		if (self.Initial):
			result += " (sala inicial)"
		result += ":"
		result += "\nPortas: " + currDoors
		result += "\nObjetos: " + currObjects

		print currDoors
		return result