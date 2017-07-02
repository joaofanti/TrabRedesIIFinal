import sys
sys.path.insert(0, "Modelos/Mapa")
from Map import *
from Item import Item

"""
	Define a classe que manipula a logica do jogo.
"""
class Game:

	"""
		Define um jogador do jogo.
	"""
	class Player:

		"""
			Cria uma nova instancia de jogador
		"""
		def __init__(self, name, addr, map):
			self.Name = name
			self.Addr = addr
			self.Room = 1 # Jogador sempre inicia na sala 1
			self.Inventario = []
			self.Inventario.append(Item("Mapa", map))

	"""
		Cria uma nova instancia de jogo.
	"""
	def __init__(self, map):
		self.Map = map
		self.Players = []

	"""
		Cria um novo jogador. Retorna falso se jogador ja existe. Retorna verdadeiro se jogador foi criado.
	"""
	def CriaJogador(self, playerId, addr):
		if (self.getPlayer(playerId) != None):
			return "Jogador ja existe."
		
		self.Players.append(self.Player(playerId, addr, self.Map.showMap()))
		return "Jogador criado na sala inicial."

	"""
		Examina a sala em que o jogador se encontra.
	"""
	def Examina(self, playerId):
		player = self.getPlayer(playerId)
		room = self.Map.getRoom(player.Room)
		return room.ToString()

	"""
		Move o jogador para outra sala.
	"""
	def Move(self, playerId, direction):
		player = self.getPlayer(playerId)
		room = self.Map.getRoom(player.Room)
		roomInDirection = room.GetRoomInDirection(direction)
		if (roomInDirection != None):
			if (room.CanMoveTo(direction)):
				player.Room = roomInDirection
				for item in player.Inventario:
					if item.Name == "Mapa":
						item.Description = self.Map.showMap(roomInDirection)
				return "O jogador se moveu para a sala " + str(roomInDirection) + "."
			else:
				return "A porta esta fechada."
		else:
			return "Nao ha sala nesta direcao."

	def LeInventorio(self, playerId):
		player = self.getPlayer(playerId)

		result = ""
		ln = len(player.Inventario)
		for i in range(0, ln):
			result += player.Inventario[i].Name
			if (i + 1 != ln):
				result += " | "
		return result

	def UsaItem(self, playerId, itemName, target = None):
		player = self.getPlayer(playerId)
		for item in player.Inventario:
			if item.Name == itemName:
				if item.Name.startswith("Nota") or item.Name == "Mapa":
					return item.Description
				elif item.Name.startswith("Chave"):
					return "Ainda nao implementado"
				else:
					return "Item nao existente no inventario"
	"""
		Busca o jogador na lista de jogadores conectados ao jogo.
	"""
	def getPlayer(self, playerName):
		for player in self.Players:
			if player.Name == playerName:
				return player
		return None