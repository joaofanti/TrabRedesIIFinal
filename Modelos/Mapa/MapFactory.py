import json
from Map import Map
from Door import Door
from Room import Room
from Item import Item

"""
	Define um gerador de mapas.
"""
class MapFactory:

	"""
		Cria uma nova instancia de gerador de mapas.
	"""
	def __init__(self):
		self.RoomsList = []	# Lista de salas geradas.
		self.DoorsList = []	# Lista de portas geradas.
		pass

	"""
		Gera um mapa a partir de um arquivo de texto com a definicao do mapa em JSON.
	"""
	def GenerateMap(self, mapJson, mapDesignText):
		# Para cada sala no arquivo JSON, gera um novo objeto Sala e entao o salva na lista de salas.
		for roomJson in mapJson:
			newRoom = self.GenerateRoom(roomJson)
			self.RoomsList.append(newRoom)

		return Map(self.RoomsList, mapDesignText)

	"""
		Gera uma sala a partir de um JSON de sala.
	"""
	def GenerateRoom(self, roomJson):

		currentRoomID = roomJson["ID"]

		doors = []
		for connectedRoomID in roomJson["ConnectedRoomsID"]:
			door = self.GenerateDoor(currentRoomID, connectedRoomID)
			doors.append(door)

		objects = []
		for objectJson in roomJson["Objects"]:

			# Se existe "State" nas configuracoes do objeto, adiciona! Se nao, usa None			
			if ("State" in objectJson):
				newObject = Item(objectJson["Name"], objectJson["Description"], objectJson["State"])
			else:
				newObject = Item(objectJson["Name"], objectJson["Description"])

			objects.append(newObject)

		newRoom = Room(currentRoomID, roomJson["StartRoom"], doors, objects)
		return newRoom

	"""
		Gera uma porta a partir de um JSON de porta ou, caso ela ja exista, utiliza a ja existente.
	"""
	def GenerateDoor(self, room1ID, room2ID):
		door = self.GetDoor([room1ID, room2ID], self.DoorsList)

		# Se a porta nao existe na lista, a cria e adiciona na lista de portas
		if (door == None):
			door = Door(room1ID, room2ID)
			self.DoorsList.append(door)

		return door

	"""
		Verifica se uma porta ja existe numa lista.
		i.e: Com a lista = [(1, 2)] e a porta = (2,1) dara verdadeiro pois a porta existe.
	"""
	def GetDoor(self, doorJson, doorsList):
		for doorFromList in doorsList:
			connectedRooms = doorFromList.ConnectedRooms
			if (((connectedRooms[0] == doorJson[0]) and (connectedRooms[1] == doorJson[1])) or ((connectedRooms[1] == doorJson[0]) and (connectedRooms[0] == doorJson[1]))):
				return doorFromList
		return None
