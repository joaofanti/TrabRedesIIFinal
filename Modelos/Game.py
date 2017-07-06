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
			self.Addr = addr #IP
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
			return "FAIL"
		
		self.Players.append(self.Player(playerId, addr, self.Map.showMap()))
		return "OK"

	"""
		Examina a sala em que o jogador se encontra.
	"""
	def Examina(self, playerId):
		player = self.getPlayer(playerId)
		if(player == None):
			return "Player nao encontrado"
		room = self.Map.getRoom(player.Room)
		return room.ToString()

	"""
		Move o jogador para outra sala.
	"""
	def Move(self, playerId, direction):
		player = self.getPlayer(playerId)
		if(player == None):
			return "Player nao encontrado"
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

	def Inventario(self, playerId):
		player = self.getPlayer(playerId)
		if(player == None):
			return "Player nao encontrado"
		result = ""
		ln = len(player.Inventario)
		for i in range(0, ln):
			result += player.Inventario[i].Name
			if (i + 1 != ln):
				result += " | "
		return result

	def UsaItem(self, playerId, itemName, target = None):
		player = self.getPlayer(playerId)
		if(player == None):
			return "Player nao encontrado"
		salaAtual = self.Map.getRoom(player.Room)

		for item in player.Inventario:
			if item.Name == itemName:
				if ("Nota" in str(item.Name)) or item.Name == "Mapa":
					print item.Description
				elif ("Chave" in str(item.Name)):
					for x in range(0, len(salaAtual.Doors)):
						salaAtual.Doors[x].opened = True
						return "Portas da sala "+str(salaAtual.ID)+" foram abertas" 
				else:
					return "Item nao existente no inventario"

	"""
		Jogador pega um objeto que esta na sala atual
	"""
	def Pegar(self, playerId, objeto):
		player = self.getPlayer(playerId)
		if(player == None):
			return "Player nao encontrado"
		salaAtual = self.Map.getRoom(player.Room)
		if(salaAtual == None):
			return "Sala nao encontrada"
		objetoAdicionado = False
		lenObjetos = len(salaAtual.Objects)
		for x in range(0, lenObjetos):
			objetoEncontrado = salaAtual.Objects[x]
			if(str(objeto) == str(objetoEncontrado.Name)):
				objetoAdicionado = True
				del salaAtual.Objects[x]
				player.Inventario.append(Item(objetoEncontrado.Name, objetoEncontrado.Description))
				break
		if(objetoAdicionado == True):
			return "Objeto " + objeto + " adicionado ao inventario"
		else:
			return "Objeto " + objeto + " nao foi encontrado nesta sala"

	"""
		Larga objeto do inventario na sala atual
	"""
	def Largar(self, playerId, objeto):
		player = self.getPlayer(playerId)
		if(player == None):
			return "Player nao encontrado"
		salaAtual = self.Map.getRoom(player.Room)
		objetoDeletado = False
		for x in range(0, len(player.Inventario)):
			itemPlayer = player.Inventario[x]
			if(itemPlayer.Name == str(objeto)):
				objetoDeletado = True
				del player.Inventario[x]
				salaAtual.Objects.append(Item(itemPlayer.Name, itemPlayer.Description))
		if(objetoDeletado == True):
			return "Objeto " + objeto + " adicionado a sala"
		else:
			return "Objeto " + objeto + " nao foi encontrado no inventario"

	"""
		Envia um texto para um jogador especifico
	"""
	def Cochichar(self, playerSource, text, playerTarget):
		player = self.getPlayer(playerSource)
		for x in range(0, len(self.Players)):
			if(self.Players[x].Name == str(playerTarget)):
				return (self.Players[x].Addr, text)

	"""
		Retorna os players presente na sala passada por parametro
	"""
	def getPlayersInRoom(self, room):
		sala = self.Map.getRoom(room)
		if(sala == None):
			return "Sala nao encontrada"
		playersNaSala = []
		for x in range(0, len(self.Players)):
			if(self.Players[x].Room == room):
				playersNaSala.append(self.Players[x].Addr)
		return playersNaSala

	"""
		Busca o jogador na lista de jogadores conectados ao jogo.
	"""
	def getPlayer(self, playerName):
		for player in self.Players:
			if player.Name == playerName:
				return player
		return None

