
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
    	return "\nSala: " + str(self.numeroSala) +
    		   "\nChave: " + self.chave +
    		   "\nPlayer1 na sala: " + self.player1 +
    		   "\nPlayer2 na sala: " + self.player2 +
    		   "\nSalas: "




class Jogador:

	def __init__(self, sala):
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
	