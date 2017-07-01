"""
	Define um item.
"""
class Item(object):

	Name = ""			# Nome do item.
	Description = ""	# Descricao do item.
	State = False		# Estado do item (caso aplicavel).
	
	"""
		Cria uma nova instancia de item.
	"""
	def __init__(self, name, description, state = False):
		self.Name = name
		self.Description = description
		self.State = state

	def ToString(self):
		result = "[" + self.Name
		if (self.State):
			result += "(" + str(self.State) + ")"
		result += ": "
		result +=  self.Description + "]"
		return result
