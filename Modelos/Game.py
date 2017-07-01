import sys
sys.path.insert(0, "Modelos/Mapa")
from Map import *

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
		def __init__(self, name, addr):
			self.Name = name
			self.Addr = addr
			self.Room = 1 # Jogador sempre inicia na sala 1

	"""
		Cria uma nova instancia de jogo.
	"""
	def __init__(self, map):
		self.Map = map
		self.Players = []

	"""
		Cria um novo jogador. Retorna falso se jogador ja existe. Retorna verdadeiro se jogador foi criado.
	"""
	def CriaJogador(self, name, addr):
		if (self.getPlayer(name) != None):
			return "Jogador ja existe."
		
		self.Players.append(self.Player(name, addr))
		return "Jogador criado na sala inicial."

	"""
		Examina a sala em que o jogador se encontra.
	"""
	def Examina(self, name):
		player = self.getPlayer(name)
		room = self.Map.getRoom(player.Room)
		return room.ToString()

	"""
		Busca o jogador na lista de jogadores conectados ao jogo.
	"""
	def getPlayer(self, playerName):
		for player in self.Players:
			if player.Name == playerName:
				return player
		return None