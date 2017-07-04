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

	def LeInventario(self, playerId):
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

	"""
		Jogador pega um objeto que está na sala atual
	"""
	def Pegar(self, playerId, objeto):
		player = self.getPlayer(playerId)
		salaAtual = self.Map.getRoom(player.Room)
		objetoAdicionado = False
		for x in range(0, len(salaAtual.Objects)):
			objetoEncontrado = salaAtual.Objects[x]
			if(str.upper(objeto) == str.upper(objetoEncontrado.Name)):
				objetoAdicionado = True
				player.Inventario.append(Item(objetoEncontrado.Name, objetoEncontrado.Description))
		if(objetoAdicionado == True):
			return "Objeto "+str(objeto)+" adicionado ao inventario"
		else:
			return "Objeto "+str(objeto)+" não foi encontrado nesta sala"

	"""
		Larga objeto do inventario na sala atual
	"""
	def Larga(self, playerId, objeto):
		player = self.getPlayer(playerId)
		salaAtual = self.Map.getRoom(player.Room)
		objetoDeletado = False
		for x in range(0, len(player.Inventario)):
			itemPlayer = player.Inventario[x]
			if(itemPlayer.Name == str(objeto)):
				objetoDeletado = True
				del player.Inventario[x]
				salaAtual.Objects.append(Item(itemPlayer.Name, itemPlayer.Description))
		if(objetoDeletado == True):
			return "Objeto "+str(objeto)+" adicionado à sala"
		else:
			return "Objeto "+str(objeto)+" não foi encontrado no inventário"

	"""
		Utiliza um objeto, pode ser usado em um alvo
	"""
	def Usar(self, playerId, object, target):
		player = self.getPlayer(playerId)
		objetoEncontrado = False
		for x in range(0, len(player.Inventario)):
			itemPlayer = player.Inventario[x]
			if(itemPlayer.Name == str(objeto)):
				objetoEncontrado = True
				itemPlayer.use() 					#Implementar método para utilizar item
		if(objetoEncontrado == True):
			return "Objeto "+str(objeto)+" foi utilizado"
		else:
			return "Objeto "+str(objeto)+" não foi encontrado no inventário"
				

	"""
		Envia um texto para todos os jogadores da sala atual
	"""
	def Falar(self, text):
		pass

	"""
		Envia um texto para um jogador especifico
	"""
	def Cochichar(self, text, playerTarget):
		pass