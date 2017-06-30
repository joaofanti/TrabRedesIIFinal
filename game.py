
###################### MAPA ######################
# Tamanho das Salas: 5x "|" por 10x "_"          #
#                                                #
#    __________    Sala pode possuir:            #
#   |          |   - Uma chave                   #
#   |          |   - Quatro portas               #
#   |  Sala 1  |   - Presenca do jogador 1 ou 2  #
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

    def __init__(self, numeroSala):
    	self.numeroSala = numeroSala						# Indica o numero da sala
    	self.botao = False									# Botao da sala que pode ser pressionado pelo player
    	self.objetos = []
    	self.players = []

    def pressionaBotao(self, player):
    	self.botao = True
    	player.botoesPressionados[self.numeroSala] = True
    	player.sequenciaBotoes.append(self.numeroSala)

    def adicionaObjeto(self, objeto):
    	self.objetos.append(objeto)

    def dadosSala(self):
		stringAux = ""
		stringAux += "\nSala: " + str(self.numeroSala)
		if(self.numeroSala == 1):
			stringAux += "\nSalas Adjacentes: 2 (Sul)"
		elif(self.numeroSala == 2):
			stringAux += "\nSalas Adjacentes: 1 (Norte), 3 (Leste), 4 (Sul)"
		elif(self.numeroSala == 3):
			stringAux += "\nSalas Adjacentes: 2 (Oeste), 5 (Sul)"
		elif(self.numeroSala == 4):
			stringAux += "\nSalas Adjacentes: 2 (Norte), 5 (Leste)"
		elif(self.numeroSala == 5):
			stringAux += "\nSalas Adjacentes: 3 (Norte), 4 (Oeste)"
		stringAux += "\nObjetos: " + str(self.objetos)
		stringAux += "\nPlayers: " + str(self.players)
		return stringAux




class Player:
    def __init__(self, numeroPlayer, sala, nome):
    	self.salaAtual = 4
        self.numeroPlayer = numeroPlayer
        self.nome = nome
        self.sala = sala
        self.chave = False
        self.objetoFinal = False
        self.botoesPressionados = { 1 : False,
                                    2 : False,
                                    3 : False,
                                    4 : False,
                                    5 : False }
        self.sequenciaBotoes = []



class Game:
	def __init__(self):
		self.salas = []
		sala = Sala(1)
		sala.adicionaObjeto("ObjetoFinal")
		self.salas.append(sala)
		sala = Sala(2)
		self.salas.append(sala)
		sala = Sala(3)
		self.salas.append(sala)
		sala = Sala(4)
		self.salas.append(sala)
		sala = Sala(5)
		self.salas.append(sala)

		self.players = []

		self.portas = []
		self.portas.append(Porta(1, 2))
		self.portas.append(Porta(2, 3))
		self.portas.append(Porta(3, 5))
		self.portas.append(Porta(5, 4))
		self.portas.append(Porta(4, 2))
