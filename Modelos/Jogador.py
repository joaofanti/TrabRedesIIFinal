"""
	Define um jogador.
"""
class Player:

	ID = ""			# Identificador do jogador
	Inventario = []	# Inventario contendo os objetos carregados pelo jogador

	"""
		Cria uma nova instancia de jogador.
	"""
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
