import StringIO

"""
	Define o mapa do jogo.
"""
class Map(object):

	Rooms = []					# Lista de salas
	RoomDesign = ""				# Desenho da sala para usar de modelo
	PlayerPlace = "<        >"	# Espaco onde vai ficar o texto "Jogador"

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
		result = ""

		# Pesquisa por "Sala #", onde "#" eh a o ID da sala em que o jogador esta
		formattedRoom = "Sala " + playerPositionRoomId
		idx = self.RoomDesign.index(formattedRoom)

		if (idx > 0):
			
		else:
			return self.RoomDesign.replace(self.PlayerPlace, '          ')

