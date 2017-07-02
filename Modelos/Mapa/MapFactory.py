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
		for connectedRoom in roomJson["ConnectedRoomsID"]:
			door = self.GenerateDoor(currentRoomID, connectedRoom)
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
	def GenerateDoor(self, room1ID, room2JSON):

		room2ID = room2JSON["Room"]

		room2Direction = room2JSON["Direction"]
		room1Direction = "N"
		if (room2Direction == "N"):
			room1Direction = "S"
		elif (room2Direction == "L"):
			room1Direction = "E"
		elif (room2Direction == "E"):
			room1Direction = "L"

		door = Door(room1ID, room1Direction, room2ID, room2Direction, room2JSON["Opened"] == "True")
		self.DoorsList.append(door)

		return door