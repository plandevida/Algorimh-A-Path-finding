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
				
				if array[i][j] == None:
					fila.append( Nodo(i, j, False, None, 0) )
				else:
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
						fila.append( Nodo(i, j, False, None, array[i][j][1]) )
					elif ( tipo == "vacio" ):
						fila.append( Nodo(i, j, False, None, 0) )
					else:
						fila.append( Nodo(i, j, False, None, 0) )

			self.mapa.append(fila)
		#print [(self.mapa[i][j].f_prima) for i in range(len(self.mapa)) for j in range(len(self.mapa[0]))]
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
		return (len(self.mapa), len(self.mapa[0]))

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
		self.h = 0
		self.visitado = False
		self.abierto = False

	def __ne__(self, other):
		return not self.__eq__(other)

	'''
	by Emilio:
		cuidado con la recursion en bucle, me he pasado 3 horas buscando este error.
		El dict comprueba los atributos que a su vez son nodos que a su vez se comprueban....
	'''
	def __eq__(self, nodo):
		#return (isinstance(nodo, self.__class__) and self.__dict__ == nodo.__dict__)
		return (isinstance(nodo, self.__class__) and nodo.x == self.x and nodo.y == self.y)

	def get_padre(self):
		return self.padre

	'''
		coste desde el nodo dado hasta este
	'''
	def coste(self, nodo):
		return (math.sqrt(math.pow(self.x-nodo.x,2)+math.pow(self.y-nodo.y,2)) + nodo.f_prima)

	def es_obstaculo(self):
		return self.obstaculo

	'''
		imprime la posicion del nodo
	'''
	def to_srt(self):
		return "({x}, {y})".format(x=self.x, y=self.y)

	def marcado_visitado(self):
		self.visitado = True
		pass

	def esta_visitado(self):
		return self.visitado

	def esta_abierto(self):
		return self.abierto
	def marcado_abierto(self):
		self.abierto = True
		pass

	def set_g(self, gnuevo):
		self.g = gnuevo
		pass

class A_estrella():
	#La clase A estrella realiza el calculo de la ruta y almacena el mapa

	def __init__(self,objeto):
		self.objeto = objeto
		self.set_solucionable(False)
		if( hasattr(objeto,"get_inicio") and hasattr(objeto,"get_meta") and hasattr(objeto,"dim") and hasattr(objeto,"adyacentes") ):

			if ( self.objeto.get_inicio() and self.objeto.get_meta() ):
				self.calcula_ruta()
				self.ordenar_ruta()
			else:
				self.error="No se ha definido el inicio y/o la meta"
		else:
			self.error="No tiene los metodos genericos"

	''' No conseguia aclararme para hacer la reasignacion de enlaces asi que me lo he reimplementado de nuevo
	def calcula_ruta(self):

		#tupla con la dimension del mapa
		dimension = self.objeto.dim()

		#No es lo que piensas EB, cochino
		abiertos = PriorityQueue(maxsize=(dimension[0] * dimension[1]))

		nodo = self.objeto.get_inicio()
		nodo.marcado_abierto()
		abiertos.put( (0, nodo) )
		meta = self.objeto.get_meta()

		while nodo != meta and not abiertos.empty():

			try:
				padre = nodo
				nodo = abiertos.get()[1]
				nodo.marcado_visitado()
				#nodo.set_g(padre.g + nodo.coste(padre) )
				print "nodo seleccionado ", (nodo.x,nodo.y), " nodo padre", (padre.x,padre.y)
			except:
				self.error="Hubo un error extrayendo de la cola"

			lista_nodos = self.objeto.adyacentes(nodo)
			print "lista de adyacentes: ", [(x.x,x.y) for x in lista_nodos]
			for i in lista_nodos:
				try:
					if  not i.esta_abierto() :
						i.g = nodo.g + nodo.coste(i)
						i.h = i.coste(self.objeto.meta)
						i.f = i.g + i.h
						i.marcado_abierto()
						i.padre = nodo
						#La cola de prioridad usa por debajo un monticulo (modulo heapq), si se le pasa una tupla usa el primer elemento para la prioridad
						abiertos.put( (i.f, i) )
					elif i.esta_abierto():
						print "uno"
						if i.esta_visitado() and i.padre != nodo:
							print "dos"
							coste_reenlace = nodo.g + nodo.coste(i)
							print "nodo ",(nodo.x,nodo.y),"coste reenlace ",coste_reenlace, " coste actual ", i.f
							if coste_reenlace < i.f:
								print "tres"
								i.g= coste_reenlace
								i.f= i.g+i.h
								i.padre = nodo

				except:
					self.error="ColaOverflowError"
	'''

	def calcula_ruta(self):

		''' tupla con la dimension del mapa'''
		dimension = self.objeto.dim()
		''' standard output takes a lot of time, use for debug purposes only '''
		debugMode = False
		''' No es lo que piensas EB, cochino'''
		meta = self.objeto.get_meta()
		abiertos = PriorityQueue(maxsize=(dimension[0] * dimension[1]))
		abiertos.put((0,self.objeto.get_inicio()))
		nodo = self.objeto.get_inicio()
		nodo.padre=self.objeto.get_inicio()
		while nodo != meta and not abiertos.empty():
			nodo=abiertos.get()[1]
			nodo.marcado_abierto()
			nodo.marcado_visitado()
			lista_nodos = self.objeto.adyacentes(nodo)
			if debugMode: print ">>>> nodo seleccionado ", (nodo.x,nodo.y), " nodo padre", (nodo.padre.x,nodo.padre.y), " nodo g", (nodo.g), "nodo h", nodo.h
			if debugMode: print "lista de adyacentes: ", [(x.x,x.y) for x in lista_nodos]
			for i in lista_nodos:
				try:
					if  not i.esta_abierto() :
						i.g = nodo.g + nodo.coste(i)
						i.h = i.coste(self.objeto.meta)
						i.f = i.g + i.h
						i.padre = nodo
						i.marcado_abierto()
						if debugMode: print (i.x,i.y), " ", nodo.coste(i)," ", i.f_prima
						''' La cola de prioridad usa por debajo un monticulo (modulo heapq), si se le pasa una tupla usa el primer elemento para la prioridad'''
						abiertos.put( (i.g, i) )
					elif i.esta_abierto():
						coste_reenlace = nodo.g + nodo.coste(i)
						if debugMode: print "padre", (nodo.x,nodo.y),"nodo ",(i.x,i.y),"coste reenlace ",coste_reenlace, " coste actual ", i.g
						if coste_reenlace < i.g:
							if debugMode: print "reenlace hecho"
							i.g= coste_reenlace
							i.f= i.g+i.h
							i.padre = nodo

				except:
					self.error="ColaOverflowError"
			

	def ordenar_ruta(self):
		self.ruta = []

		nodo = self.objeto.get_meta()

		if ( nodo.get_padre() ):
			while nodo != self.objeto.get_inicio():
				self.ruta.append(nodo)
				nodo = nodo.get_padre()

			self.ruta.append(self.objeto.get_inicio())
			self.ruta.reverse()
			self.ruta = [(node.x,node.y) for node in self.ruta]
			self.set_solucionable(True)
			
		else:
			self.error="No se ha encontrado solucion"


	def get_ruta(self):
		return self.ruta

	def set_solucionable(self,value):
		self.solucionable = value

	def get_solucionable(self):
		return self.solucionable

	def get_error(self):
		return self.error 


# array = [[("inicio",0),("obstaculo",0),("meta",0)],[("obstaculo",0),("obstaculo",0),("vacio",0)],[("vacio",0),("vacio",0),("vacio",0)]]
# mapa = Mapa(array)
# a = A_estrella(mapa)

# print("\n Finish")

