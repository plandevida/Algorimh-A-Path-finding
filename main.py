import math
from Queue import PriorityQueue

class Mapa():
	def __init__(self, array):
		'''
			Formato del array para el mapa
			array[i][j] =("",1)
		'''
		self.mapa = []
		self.inicio = None
		self.meta = None

		for i in range(0, len(array)):

			fila = []
			for j in range(0, len(array[i])):
				tipo = array[i][j][0]

				if ( tipo == "inicio" ):
					nodo = Nodo(i, j, False, None, 0)
					fila.append(nodo)
					self.inicio = nodo
				elif ( tipo == "meta" ):
					nodo = Nodo(i, j, False, None, 0)
					fila.append(nodo)
					self.meta = nodo
				elif ( tipo == "obstaculo" ):
					fila.append( Nodo(i, j, True, None, 0) )
				elif ( tipo == "penalizacion" ):
					fila.append( Nodo(i, j, True, None, array[i][j][1]) )
				elif ( tipo == "vacio" ):
					fila.append( Nodo(i, j, False, None, 0) )

			self.mapa.append(fila)

	def get_inicio(self):
		return self.inicio

	def get_meta(self):
		return self.meta

	def get_nodo(self, x, y):

		if ( self.en_rango(x, y) ):
			return self.mapa[x][y]
		else:
			return None

	def dim(self):
		return (len(array), len(array[0]))

	def en_rango(self, x, y):
		return (x >= 0 and x < len(self.mapa)) and (y >= 0 and y < len(self.mapa[0]))

	def adyacentes(self, nodo):
		lista = []

		if ( nodo ):

			if (not nodo.es_obstaculo()):
				x = nodo.x
				y = nodo.y

				if ( self.en_rango(x-1, y-1) ):
					nodo_adyacente = self.mapa[x-1][y-1]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)
				if ( self.en_rango(x, y-1) ):
					nodo_adyacente = self.mapa[x][y-1]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)
				if ( self.en_rango(x+1, y-1) ):
					nodo_adyacente = self.mapa[x+1][y-1]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)
				if ( self.en_rango(x-1, y) ):
					nodo_adyacente = self.mapa[x-1][y]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)
				if ( self.en_rango(x+1, y) ):
					nodo_adyacente = self.mapa[x+1][y]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)
				if ( self.en_rango(x-1, y+1) ):
					nodo_adyacente = self.mapa[x-1][y+1]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)
				if ( self.en_rango(x, y+1) ):
					nodo_adyacente = self.mapa[x][y+1]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)
				if ( self.en_rango(x+1, y+1) ):
					nodo_adyacente = self.mapa[x+1][y+1]
					if ( not nodo_adyacente.es_obstaculo()):
						lista.append(nodo_adyacente)

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
		self.g = 0
		self.visitado = False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __eq__(self, nodo):
		return (isinstance(nodo, self.__class__) and self.__dict__ == nodo.__dict__)

	def get_padre(self):
		return self.padre

	'''
		coste desde el nodo dado hasta este
	'''
	def coste(self, nodo):
		return math.sqrt(math.pow(self.x-nodo.x,2)+math.pow(self.y-nodo.y,2)) + self.f_prima

	def es_obstaculo(self):
		return self.obstaculo

	'''
		imprime la posicion del nodo
	'''
	def to_srt(self):
		return "[{x}, {y}]".format(x=self.x, y=self.y)

	def marcado_visitado(self):
		self.visitado = True
		pass

	def esta_visitado(self):
		return self.visitado

	def set_g(self, gnuevo):
		self.g = gnuevo
		pass

class A_estrella():
	#La clase A estrella realiza el calculo de la ruta y almacena el mapa

	def __init__(self,objeto):
		self.objeto = objeto
		if( hasattr(objeto,"get_inicio") and hasattr(objeto,"get_meta") and hasattr(objeto,"dim") and hasattr(objeto,"adyacentes") ):

			if ( self.objeto.get_inicio() and self.objeto.get_meta() ):

				self.calcula_ruta()
				self.ordenar_ruta()
			else:
				print("\n no se ha definido el inicio y/o la meta")
		else:
			print("\n no tiene los metodos")

	def calcula_ruta(self):

		''' tupla con la dimension del mapa'''
		dimension = self.objeto.dim()

		''' No es lo que piensas EB, cochino'''
		abiertos = PriorityQueue(maxsize=(dimension[0] * dimension[1]))

		nodo = self.objeto.get_inicio()
		abiertos.put( (0, nodo) )
		meta = self.objeto.get_meta()

		while nodo != meta and not abiertos.empty():

			try:
				padre = nodo

				nodo = abiertos.get()[1]
				nodo.marcado_visitado()

				nodo.padre = padre
				nodo.set_g(padre.g + nodo.coste(padre) )
			except:
				print("Hubo un error extrayendo de la cola")

			lista_nodos = self.objeto.adyacentes(nodo)

			for i in lista_nodos:
				try:
					if ( not i.esta_visitado() ):
						g = nodo.g + nodo.coste(i)
						h = i.coste(self.objeto.meta)

						f = g + h
						''' La cola de prioridad usa por debajo un monticulo (modulo heapq), si se le pasa una tupla usa el primer elemento para la prioridad'''
						abiertos.put( (f, i) )
				except:
					print "Cola al maximo"

	def ordenar_ruta(self):
		ruta = []

		nodo = self.objeto.get_meta()

		if ( nodo.get_padre() ):
			while nodo != self.objeto.get_inicio():
				ruta.append(nodo)
				nodo = nodo.get_padre()

			ruta.append(self.objeto.get_inicio())
			ruta.reverse()

			for i in range(0, len(ruta)):
				print(ruta[i].to_srt() + " ")
		else:
			print("\n No se ha encontrado solucion")


array = [[("inicio",0),("obstaculo",0),("meta",0)],[("vacio",0),("obstaculo",0),("vacio",0)],[("vacio",0),("vacio",0),("vacio",0)]]
mapa = Mapa(array)
a = A_estrella(mapa)

print("\n Finish")
