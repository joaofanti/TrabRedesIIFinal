class Game:
	def __init__(self):
		self.players = []
		self.portas = []
		self.portas.append(Porta(1, 2))
		self.portas.append(Porta(2, 3))
		self.portas.append(Porta(3, 5))
		self.portas.append(Porta(5, 4))
		self.portas.append(Porta(4, 2))
