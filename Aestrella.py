import math,constants
from Queue import PriorityQueue


class Mapa():
	def __init__(self, array,inicio,meta):
		'''
			Formato del array para el mapa
			array[i][j] =("",1)
		'''
		self.mapa = []
		self.meta = None
		self.inicio = None

		for i in range(0, len(array)):

			fila = []
			for j in range(0, len(array[i])):
				
				if array[i][j] == None:
					fila.append( Nodo(i, j, False, None, 0) )
				else:
					tipo = array[i][j][0]
					'''
					if ( tipo == "inicio" ):
						nodo = Nodo(i, j, False, None, 0)
						fila.append(nodo)
						self.inicio = nodo
					elif ( tipo == "meta" ):
						nodo = Nodo(i, j, False, None, 0)
						fila.append(nodo)
						self.meta = nodo
					'''
					if ( tipo == "obstaculo" ):
						fila.append( Nodo(i, j, True, None, 0) )
					elif ( tipo == "penalizacion" ):
						fila.append( Nodo(i, j, False, None, array[i][j][1]) )
					elif ( tipo == "vacio" ):
						fila.append( Nodo(i, j, False, None, 0) )
					else:
						fila.append( Nodo(i, j, False, None, 0) )

			self.mapa.append(fila)
		''' Si el inicio y meta se pasa por parametro nos podemos ahorrar hacer un deepcopy del array'''
		if inicio != None:
			self.inicio = Nodo(inicio[0],inicio[1],False,None,0)
			self.mapa[inicio[0]][inicio[1]] = self.inicio
		if meta != None:
			self.meta = Nodo(meta[0],meta[1],False,None,0)
			self.mapa[meta[0]][meta[1]] = self.meta
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
		'''Para realizar el reenlace se tienen que conocer los hijos,implementado con un hashtable'''
		self.diccionario_hijos = {}

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

	def get_coordenadas(self):
		return (self.x,self.y)

class A_estrella():
	#La clase A estrella realiza el calculo de la ruta y almacena el mapa

	def __init__(self,objeto):
		self.objeto = objeto
		self.set_solucionable(False)
		if( hasattr(objeto,"get_inicio") and hasattr(objeto,"get_meta") and hasattr(objeto,"dim") and hasattr(objeto,"adyacentes") ):

			if ( self.objeto.get_inicio() and self.objeto.get_meta() ):

				if ( constants.algorimthReLink() ):
					print "Algoritmo con re-enlace"
					self.calcula_ruta_reenlace()
				else:
					print "Algoritmo sin re-enlace"
					self.calcula_ruta()

				self.ordenar_ruta()
			else:
				self.error="No se ha definido el inicio y/o la meta"
		else:
			self.error="No tiene los metodos genericos"


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
	
	''' Esta implementacion realiza reenlaces'''
	def calcula_ruta_reenlace(self):
		''' tupla con la dimension del mapa'''
		dimension = self.objeto.dim()
		meta = self.objeto.get_meta()
		abiertos = {}
		nodo = self.objeto.get_inicio()
		nodo.g=0
		nodo.h=nodo.coste(meta) 
		nodo.padre=self.objeto.get_inicio()
		nodo.f= nodo.g+nodo.h
		abiertos[nodo.get_coordenadas()]=nodo.f
		while len(abiertos) > 0 and nodo != meta:
			'''obtenemos el minimo elemento de los abiertos y lo eliminamos de la lista'''
			coordenadas = minimum_element(abiertos)
			nodo = self.objeto.get_nodo(coordenadas[0],coordenadas[1])
			nodo.marcado_visitado()
			del abiertos[coordenadas]
			lista_nodos = self.objeto.adyacentes(nodo)
			if constants.debugMode(): print ">>>> nodo seleccionado ", coordenadas, " nodo padre", (nodo.padre.x,nodo.padre.y), " nodo g", (nodo.g), "nodo h", nodo.h
			if constants.debugMode(): print "lista de adyacentes: ", [(x.x,x.y) for x in lista_nodos]
			for i in lista_nodos:
				distancia_actual =nodo.g+nodo.coste(i)
				if constants.debugMode(): print "padre", (nodo.x,nodo.y),"nodo ",(i.x,i.y),"coste reenlace ",distancia_actual, " coste actual ", i.g
				if i.esta_visitado():
					'''intentamos rehacer el enlace'''
					if i.g > distancia_actual:
						del i.get_padre().diccionario_hijos[i.get_coordenadas()]
						nodo.diccionario_hijos[i.get_coordenadas()]= i
						relink(nodo,i,abiertos,(i.g-distancia_actual))
						i.padre=nodo
				elif i.esta_abierto():
					'''actualizamos el g y f'''
					if i.g > distancia_actual:
						i.g = distancia_actual
						i.f=distancia_actual+i.h
						abiertos[i.get_coordenadas()]= i.f
						del i.get_padre().diccionario_hijos[i.get_coordenadas()]
						nodo.diccionario_hijos[i.get_coordenadas()]= i
						i.padre=nodo
				else:
					i.g = distancia_actual
					i.h = i.coste(meta)
					i.f=i.g+i.h
					i.marcado_abierto()
					abiertos[i.get_coordenadas()]= i.f
					nodo.diccionario_hijos[i.get_coordenadas()]= i
					i.padre=nodo


		pass
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

def minimum_element(array):
	minimum_element = None
	minimum_value = None
	if len(array)>0:
		for key in array:
			if minimum_element == None:
				minimum_value = array[key]
				minimum_element=key
			elif array[key] < minimum_value:
				minimum_value = array[key]
				minimum_element=key
	return minimum_element

def relink(nuevo_padre,hijo,abiertos,reduccion):
	hijo.g-= reduccion
	hijo.f-=reduccion
	hijo.padre=nuevo_padre
	for x in hijo.diccionario_hijos:
		if x in abiertos:
			abiertos[x] = abiertos[x]-reduccion
		relink(hijo,hijo.diccionario_hijos[x],abiertos,reduccion)

# array = [
# 	[("obstaculo",0),("obstaculo",0),("penalizacion",22), ("penalizacion",20)], 
# 	[("obstaculo",0),("inicio",0),("obstaculo",0),("obstaculo",0)],
# 	[("penalizacion",1),("penalizacion",3),("penalizacion",30), ("obstaculo",0)],
# 	[("obstaculo",0),("obstaculo",0),("obstaculo",0),("meta",0)]
# ]
# mapa = Mapa(array, (1,1), (3,3))
# a = A_estrella(mapa)
# print("\n")
# print(a.get_ruta())

# print("\n Finish")