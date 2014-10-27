import math

class Mapa():
	def __init__(self, array):
		'''
			Formato del array para el mapa
			array[i][j] =("",1)
		'''
		self.mapa = []

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

	def coste(self):
		return 0

	def en_rango(self, x, y):
		return (x >= 0 and x < len(self.mapa)) and (y >= 0 and y < len(self.mapa[0]))

	def adyacentes(self, nodo):
		lista = []

		if ( nodo ):

			if (not nodo.es_obstaculo()):
				x = nodo.x
				y = nodo.y

				if ( self.en_rango(x-1, y-1) ):
					lista.append(self.mapa[x-1][y-1])
				if ( self.en_rango(x, y-1) ):
					lista.append(self.mapa[x][y-1])
				if ( self.en_rango(x+1, y-1) ):
					lista.append(self.mapa[x+1][y-1])
				if ( self.en_rango(x-1, y) ):
					lista.append(self.mapa[x-1][y])
				if ( self.en_rango(x+1, y) ):
					lista.append(self.mapa[x+1][y])
				if ( self.en_rango(x-1, y+1) ):
					lista.append(self.mapa[x-1][y+1])
				if ( self.en_rango(x, y+1) ):
					lista.append(self.mapa[x][y+1])
				if ( self.en_rango(x+1, y+1) ):
					lista.append(self.mapa[x+1][y+1])

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
		return math.sqrt(math.pow(self.x-nodo.x,2)+math.pow(self.y-nodo.y,2))

	def es_obstaculo(self):
		return self.obstaculo

	'''
		imprime la posicion del nodo
	'''
	def to_srt(self):
		return "[{x}, {y}]".format(x=self.x, y=self.y)

	def get_penalizacion(self):
		return self.f_prima

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def marcado_visitado(self):
		self.visitado = True
		pass

	def esta_visitado(self):
		return self.visitado

class A_estrella():
	#La clase A estrella realiza el calculo de la ruta y almacena el mapa

	def __init__(self,objeto):
		self.objeto = objeto
		if( hasattr(objeto,"get_inicio") and hasattr(objeto,"get_meta") and hasattr(objeto,"coste") and hasattr(objeto,"adyacentes") ):
			self.calcula_ruta()
			self.ordenar_ruta()
		else:
			print "\n no tiene los metodos"

	def calcula_ruta(self):
		nodo = self.objeto.get_inicio()
		meta = self.objeto.get_meta()

		print "\n el nodo inicio {n}".format(n=nodo.to_srt())
		print "\n el nodo meta {n}".format(n=meta.to_srt())

		nodo_menor = None
		while nodo != meta:

			lista_nodos = self.objeto.adyacentes(nodo)
			''' Nodo con valor infinito para empezar con los adyacentes'''
			nodo_menor = Nodo(0,0,False, None, 10000000000)

			for i in lista_nodos:
				if (i.esta_visitado()):
					continue

				g = nodo.g + nodo.coste(i)
				h = i.coste(self.objeto.meta)

				f = g + h

				if ( nodo_menor and nodo_menor.f > f ):
					nodo_menor = i
			nodo_menor.padre=nodo
			nodo.marcado_visitado()
			nodo = nodo_menor

			print "\n nodo seleccionado {n}".format(n=nodo.to_srt())

	def ordenar_ruta(self):
		ruta = []
		ruta.append(self.objeto.get_meta())

		nodo = self.objeto.get_meta().get_padre()

		while nodo != self.objeto.get_inicio():
			ruta.append(nodo)
			nodo = nodo.get_padre()

			print ruta

		ruta.append(self.objeto.get_inicio())
		ruta = ruta.reverse()

		for i in range(ruta):
			print ruta[i].to_srt() + " "


array = [[("inicio",0),("obstaculo",0),("meta",0)],[("vacio",0),("obstaculo",0),("vacio",0)],[("vacio",0),("vacio",0),("vacio",0)]]
mapa = Mapa(array)
nodo = mapa.get_nodo(1,1)
print nodo
print (mapa.adyacentes( nodo ))
a = A_estrella(mapa)

print "\n Finish"
