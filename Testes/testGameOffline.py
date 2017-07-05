import sys
# Adicionar o caminho do MAP FACTORY
sys.path.insert(0, '../Modelos/')
sys.path.insert(0, '../Modelos/Mapa/')
from Game import *
from Map import *
from MapFactory import *
import json

"""
    Metodo para testar uma instancia do jogo completo
"""
if __name__ == "__main__":
	
	fct = MapFactory()
	with open('../Recursos/Mapa.txt', 'r') as data_file:
		jsonFormatted = json.load(data_file)
		with open('../Recursos/MapaDesign.txt', 'r') as mapDesign:
			generatedMap = fct.GenerateMap(jsonFormatted, mapDesign.read())


	#Instancia o jogo
	game = Game(generatedMap)

	#Cria dois jogadores
	game.CriaJogador("Joao", "127.0.0.1")
	game.CriaJogador("Link", "127.0.0.1")

	#Comeca o jogo
	jogador = raw_input("Qual seu nick?\n")
	while True:
		print "Comandos: Examina, Move, Inventario, Pegar, Largar, "
		comando = raw_input("Escreva o comando a ser utilizado\n")
		if(comando == "Examina"):
			print game.Examina(jogador) + "\n"
		elif(comando == "Move"):
			direcao = raw_input("Escreva a direcao\n")
			print game.Move(jogador, direcao) + "\n"
		elif(comando == "Inventario"):
			print game.Inventario(jogador) + "\n"
		elif(comando == "Pegar"):
			objeto = raw_input("Escreva o objeto a ser pego\n")
			print game.Pegar(jogador, objeto) + "\n"
		elif(comando == "Largar"):
			objeto = raw_input("Escreva o objeto a ser solto\n")
			print game.Largar(jogador, objeto) + "\n"
		else:
			print "Comando nao encontrado"