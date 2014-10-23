import math

class Mapa():
	def __init__(self, array):
		#array[i][j] =[{"",1}
		self.mapa = None

		for i in len(array):
			for j in len(array[i]):
				tipo = array[i][j][0]

				if ( tipo == "inicio" ):
					nodo = Nodo(i, j, False, None, 0)
					mapa[i][j] = nodo
					self.inicio = nodo
				elif ( tipo == "meta" ):
					nodo = Nodo(i, j, False, None, 0)
					mapa[i][j] = nodo
					self.meta = nodo
				elif ( tipo == "obstaculo" ):
					mapa[i][j] = Nodo(i, j, True, None, 0)
				elif ( tipo == "penalizacion" ):
					mapa[i][j] = Nodo(i, j, True, None, array[i][j][1])
				elif ( tipo == "vacio" ):
					nodo = Nodo(i, j, False, None, 0)

	def en_rango(x,y):
		return (x < 0 and x >= len(mapa))

	def adyacentes(nodo):
		lista = {}

		if (not nodo.es_obstaculo()):
			x = nodo.x
			y = nodo.y

			if ( en_rango() ):
				lista.append(mapa[x-1][y-1])
			if ( en_rango() ):
				lista.append(mapa[x][y-1])
			if ( en_rango() ):
				lista.append(mapa[x+1][y-1])
			if ( en_rango() ):
				lista.append(mapa[x-1][y])
			if ( en_rango() ):
				lista.append(mapa[x+1][y])
			if ( en_rango() ):
				lista.append(mapa[x-1][y+1])
			if ( en_rango() ):
				lista.append(mapa[x][y+1])
			if ( en_rango() ):
				lista.append(mapa[x+1][y+1])

		return lista


class Nodo():
	"""docstring for Nodo"""
	def __init__(self, x, y,obstaculo, padre, penalizacion):
		self.x = x
		self.y = y
		self.padre = padre
		self.f = float("inf")
		self.obstaculo = obstaculo
		self.f_prima = penalizacion

	def get_padre():
		return padre

	def coste (nodo):
		return math.sqrt(math.pow(self.x-nodo.x,2)+math.pow(self.y-nodo.y,2))

	def es_obstaculo():
		return obstaculo


class A_estrella():
	#La clase A estrella realiza el calculo de la ruta y almacena el mapa

	def __init__(self,objeto):
		self.objeto = objeto
		if(not(hasattr(objeto,"get_inicio")and hasattr(objeto,"meta")and hasattr(objeto,"coste")and hasattr(objeto,"adyacentes"))):
			pass
		else:
			calcula_ruta()
			ordenar_ruta()
			

	def calcula_ruta():
		nodo = objeto.get_inicio()
		while nodo is not objeto.meta():

			lista_nodos = objeto.adyacentes(nodo)

			for i in lista_nodos:

				g = nodo.g + nodo.coste(i)
				h = i.coste(objeto.meta)

				f = g + h

				if ( nodo_menor and nodo_menor.f > f ):
					nodo_menor = i
			nodo_menor.padre=nodo
			nodo = menor

	def ordenar_ruta():
		ruta = ""
		nodo = objeto.meta().get_padre()
		while nodo is not objeto.get_inicio():
			ruta.append(nodo)
			nodo = nodo.get_padre()
		ruta = ruta.reverse()


array = [[("inicio",0),("obstaculo",0),("meta",0)],[("vacio",0),("obstaculo",0),("vacio",0)],[("vacio",0),("vacio",0),("vacio",0)]]
a = A_estrella("")


print("db es un nazi5")