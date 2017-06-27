
###################### MAPA ######################
# Tamanho das Salas: 5x "|" por 10x "_"          #
#                                                #
#    __________    Sala pode possuir:            #
#   |          |   - Uma chave                   #
#   |          |   - Quatro portas               #
#   |  Sala 1  |   - Presença do jogador 1 ou 2  #
#   |          |                                 #
#   |__________|__________                       #
#   |          |          |                      #
#   |          |          |                      #
#   |  Sala 2  |  Sala 3  |                      #
#   |          |          |                      #
#   |__________|__________|                      #
#   |          |          |                      #
#   |          |          |                      #
#   |  Sala 4  |  Sala 5  |                      #
#   |          |          |                      #
#   |__________|__________|                      #
#                                                #
##################################################
"""
class Porta:
	
	def __init__(self, salaOrigem, salaDestino):
		self.conecta = (salaOrigem, salaDestino)			# Tupla indicando salas conectadas pela porta


class Sala:

    def __init__(self, chave, numeroSala, player1, player2, objetoFinal):
    	self.objetoFinal = objetoFinal						# Boolean que indica se o objeto final esta na sala	
    	self.chave = chave									# Boolean que indica se a chave esta na sala
    	self.numeroSala = numeroSala						# Indica o numero da sala
    	self.player1 = player1								# Boolean que indica se o jogador1 esta na sala
    	self.player2 = player2								# Boolean que indica se o jogador2 esta na sala
    	self.botao = False									# Botao da sala que pode ser pressionado pelo player

    def pressionaBotao(self, player):
    	player.botoesPressionados[self.numeroSala] = True
    	player.sequenciaBotoes.append(self.numeroSala)

    def dadosSala(self):
    	return "\nSala: " + str(self.numeroSala) + "\nChave: " + str(self.chave) + "\nPlayer1 na sala: " + str(self.player1) + "\nPlayer2 na sala: " + str(self.player2) + "\nSalas: " #Printar direçoes e salas correspondentes




class Player:
    def __init__(self, numeroPlayer, sala):
        self.numeroPlayer = numeroPlayer
        self.sala = sala
        self.chave = False
        self.objetoFinal = False
        self.botoesPressionados = { 1 : False,
                                    2 : False,
                                    3 : False,
                                    4 : False,
                                    5 : False }
        self.sequenciaBotoes = []



if __name__ == "__main__":
	salas = []
    salas.append(Sala(False, 1, False, False, True))
    salas.append(Sala(False, 2, False, False, False))
    salas.append(Sala(True,  3, False, False, False))
    salas.append(Sala(False, 4, True,  True,  False))
    salas.append(Sala(False, 5, False, False, False))

    players = []
    players.append(Player(1, 4))
    players.append(Player(2, 4))

    portas = []
    portas.append(Porta(1, 2))
    portas.append(Porta(2, 3))
    portas.append(Porta(3, 5))
    portas.append(Porta(5, 4))
    portas.append(Porta(4, 2))
    
    print("\nBem-vindo ao nosso Jogo Multiplayer!")
    print("\nVocé o player número: " + Player1.numeroPlayer)
    print("\nSegue uma lista de possíveis commandos: ")
    print("\nExaminar \nMover <N/S/L/O> \nPegar <objeto> \nLargar <objeto> \nInventario \nUsar <objeto> \nFalar <texto> \nCochichar <texto> <player> \nAjuda"

"""

