"""
	Define uma porta.
"""
class Door:


	"""
		Cria uma nova instancia de Door.
	"""
	def __init__(self, room1, dirRoom1, room2, dirRoom2, opened):
		self.ConnectedRooms = [room1, room2] # Quais salas ela conecta
		self.DirRoom1 = dirRoom1 # Direcao da sala 1 em relacao a porta
		self.DirRoom2 = dirRoom2 # Direcao da sala 2 em relacao a porta
		self.Opened = opened	 # Porta esta aberta

	"""
		Abre a porta.
	"""
	def OpenDoor(self):
		self.Opened = True

	"""
		Fecha a porta
	"""
	def CloseDoor(self):
		self.Opened = False

	"""
		Traduz o objeto Porta como string.
	"""
	def ToString(self):
		openedText = "fechada"
		if (self.Opened):
			openedText = "aberta"

		formattedRooms = str(self.ConnectedRooms[0]) + " (" + self.DirRoom1 + ")"
		formattedRooms += ", " + str(self.ConnectedRooms[1]) + " (" + self.DirRoom2 + ")"
		result = "[(" + formattedRooms + "), " + openedText + "]" 
		return result
