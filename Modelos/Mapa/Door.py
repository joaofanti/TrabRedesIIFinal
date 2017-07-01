"""
	Define uma porta.
"""
class Door:


	"""
		Cria uma nova instancia de Door.
	"""
	def __init__(self, room1, room2):
		self.ConnectedRooms = [room1, room2] # Quais salas ela conecta
		self.Opened = False		# Porta esta aberta

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

		formattedRooms = ','.join(str(x) for x in self.ConnectedRooms)
		result = "[(" + formattedRooms + "), " + openedText + "]" 
		return result
