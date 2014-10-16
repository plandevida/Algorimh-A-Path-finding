import math

class Nodo():
	"""docstring for Nodo"""
	def __init__(self, x, y, padre):
		self.x = x
		self.y = y
		self.padre = padre
		self.f = float("inf")

	def get_padre():
		return padre

	def coste (nodo):
		return math.sqrt(math.pow(self.x-nodo.x,2)+math.pow(self.y-nodo.y,2))


class A_estrella():

	def __init__(self,objeto):
		self.objeto = objeto
		if(not(hasattr(objeto,"get_inicio")and hasattr(objeto,"meta")and hasattr(objeto,"coste")and hasattr(objeto,"adyacentes"))):
			pass
		else:
			nodo = objeto.get_inicio()
			while nodo is not objeto.meta():

				lista_nodos = objeto.adyacentes(nodo)

				for i in lista_nodos:

					g = i.coste(objeto.get_inicio())
					h = i.coste(objeto.meta)

					f = g + h

					if ( nodo_menor and nodo_menor.f > f ):
						nodo_menor = i

					



		

print("db es un nazi5")