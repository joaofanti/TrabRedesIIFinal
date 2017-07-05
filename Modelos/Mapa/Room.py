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
		Retorna qual sala esta na direcao solicitada em referencia a sala atual.
	"""
	def GetRoomInDirection(self, direction):
		for door in self.Doors:
			# Se estou na primeira sala, entao deve devolver a segunda sala
			if door.ConnectedRooms[0] == self.ID:
				if door.DirRoom2 == direction:
					return door.ConnectedRooms[1]
			# Se estou na segunda sala, entao deve devolver a primeira sala
			elif door.ConnectedRooms[1] == self.ID:
				if door.DirRoom1 == direction:
					return door.ConnectedRooms[0]
		return None

	"""
		Retorna se o jogador pode mover-se para a sala na direcao.
	"""
	def CanMoveTo(self, direction):
		for door in self.Doors:
			# Se estou na primeira sala, entao deve devolver a segunda sala
			if door.ConnectedRooms[0] == self.ID:
				if door.DirRoom2 == direction:
					return door.Opened
			# Se estou na segunda sala, entao deve devolver a primeira sala
			elif door.ConnectedRooms[1] == self.ID:
				if door.DirRoom1 == direction:
					return door.Opened
		return False

	"""
	"""
	def ToString(self):
		currDoors = ""
		for door in self.Doors:
			currDoors += door.ToString() + " - "

		currObjects = ""
		for roomObject in self.Objects:
			currObjects += roomObject.ToString() + "; "
		result = "Sala #" + str(self.ID)
		if (self.Initial):
			result += " (sala inicial)"
		result += ":"
		result += "\nPortas: " + currDoors
		result += "\nObjetos: " + currObjects

		return result

