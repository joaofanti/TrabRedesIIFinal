import sys
# Adicionar o caminho do MAP FACTORY
sys.path.insert(0, '../Modelos/')
sys.path.insert(0, '../Modelos/Mapa/')
from Game import *
from Map import *
from MapFactory import *
import json

"""
    Metodo principal para rodar o cliente
"""
if __name__ == "__main__":
	
	fct = MapFactory()
	with open('../Recursos/Mapa.txt', 'r') as data_file:
		jsonFormatted = json.load(data_file)
		with open('../Recursos/MapaDesign.txt', 'r') as mapDesign:
			generatedMap = fct.GenerateMap(jsonFormatted, mapDesign.read())

	#Teste 1 - CriaJogador 
	print "----- CriaJogador -----"
	game = Game(generatedMap)
	print game.CriaJogador("Joao", "127.0.0.1") + "\n"

	#Teste 2 - Examina
	print "----- Examina -----"
	game = Game(generatedMap)
	game.CriaJogador("Joao", "127.0.0.1")
	print game.Examina("Joao") + "\n"

	#Teste 3 - Move
	print "----- Move -----"
	game = Game(generatedMap)
	game.CriaJogador("Joao", "127.0.0.1")
	print game.Move("Joao", "S") 
	print game.Examina("Joao") + "\n"

	#Teste 4 - Inventario
	print "----- Inventario -----"
	game = Game(generatedMap)
	game.CriaJogador("Joao", "127.0.0.1")
	print game.Inventario("Joao") + "\n"

	#Teste 5 - Pegar
	print "----- Pegar -----"
	game = Game(generatedMap)
	game.CriaJogador("Joao", "127.0.0.1")
	print "Objetos no inventario: "+game.Inventario("Joao")
	print game.Pegar("Joao", "Nota1")
	print "Objetos no inventario: "+game.Inventario("Joao") + "\n"

	#Teste 6 - Largar
	print "----- Largar -----"
	game = Game(generatedMap)
	game.CriaJogador("Joao", "127.0.0.1")
	print game.Examina("Joao")
	print "Inventario do player: " + game.Inventario("Joao")
	print game.Largar("Joao", "Mapa")
	print game.Examina("Joao")
	print "Inventario do player: " + game.Inventario("Joao") + "\n"

	#Teste 7 - getPlayersInRoom
	print "----- Players na Sala -----"
	game = Game(generatedMap)
	game.CriaJogador("Joao", "127.0.0.1")
	game.CriaJogador("Bruno", "127.0.0.1")
	print game.getPlayersInRoom(1)
	print "Adiciona mais dois players"
	game.CriaJogador("Santos", "127.0.0.1")
	game.CriaJogador("Gui", "127.0.0.1")
	print game.getPlayersInRoom(1)
