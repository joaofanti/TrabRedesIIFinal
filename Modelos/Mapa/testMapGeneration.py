import json
from MapFactory import MapFactory

"""
    Metodo principal para rodar o cliente
"""
if __name__ == "__main__":

	fct = MapFactory()
	with open('Mapa.txt', 'r') as data_file:
		jsonFormatted = json.load(data_file)
		with open('MapaDesign.txt', 'r') as mapDesign:
			generatedMap = fct.GenerateMap(jsonFormatted, mapDesign.read())
	print generatedMap.showMap()