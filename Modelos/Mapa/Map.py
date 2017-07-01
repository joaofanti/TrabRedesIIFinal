import StringIO

"""
	Define o mapa do jogo.
"""
class Map(object):

	Rooms = []					# Lista de salas
	RoomDesign = ""				# Desenho da sala para usar de modelo
	PlayerPlace = "PLAYER"		# Texto para escrever onde esta o jogador

	"""
		Cria uma nova instancia de Mapa
	"""
	def __init__(self, rooms, roomDesign):
		self.Rooms = rooms
		self.RoomDesign = roomDesign

	"""
		Retorna o mapa desenhado como ASCII com a posicao do jogador, se necessario.
	"""
	def showMap(self, playerPositionRoomId = -1):
		if (playerPositionRoomId > 0):
			return "Voce esta na sala " + str(playerPositionRoomId) + "\n" + self.RoomDesign
		else:
			return self.RoomDesign

	def getRoom(self, roomId):
		for room in self.Rooms:
			if room.ID == roomId:
				return room
		return None