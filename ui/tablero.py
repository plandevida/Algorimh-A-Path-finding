# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablero.ui'
#
# Created: Thu Oct 30 23:17:33 2014
#      by: PyQt4 UI code generator 4.11.2
# Modified: Fri Oct 31 1:02:00 2014
#      by: Emilio Álvarez Piñeiro
#
# WARNING! All changes made in this file will be lost!
'''
For test values lookup constants.py
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Queue import PriorityQueue
from Aestrella import *
import random, constants, copy, threading
from  multiprocessing import Process, Pipe
from error_dialog import *



try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	
	# Initializes the needed variables
	def __init__(self,x,y,AllowMultiProcessing):
		self.row_count=x
		self.column_count=y
		self.clear_map()
		self.AllowMultiProcessing=AllowMultiProcessing

	def clear_map(self):
		'''
		Una absoluta pesadilla hasta que he conseguido montar el array de tuplas
		'''
		self.mapa=[[None for y in range(self.column_count)] for x in range(self.row_count)]
		self.waypoint_priority_queue = []
		self.start_cell=None
		self.ending_cell=None

	def clear_table(self):
		self.clear_map()
		for i in range(self.row_count):
			for j in range(self.column_count):
				item =self.centralwidget.findChild(QTableWidget, "table").item(i,j)
				item.setBackground(constants.get_empty_background())
				item.setText("")

	# Delete painted routes
	def clear_route(self):

		for i in range(self.row_count):
			for j in range(self.column_count):
				if self.mapa[i][j] == None:
					background = constants.get_empty_background()
				elif self.mapa[i][j][0] == "inicio":
					background = constants.get_start_background()
				elif self.mapa[i][j][0] == "meta":
					background = constants.get_ending_background()
				elif self.mapa[i][j][0] == "penalizacion":
					background = constants.get_setback_background()
				elif self.mapa[i][j][0] == "obstaculo":
					background = constants.get_block_background()
				elif self.mapa[i][j][0] == "waypoint":
					background = constants.get_waypoint_background()
				else:
					background = constants.get_empty_background()
				self.centralwidget.findChild(QTableWidget, "table").item(i,j).setBackground(background)



	# Makes the call to A* algorithm and gets the answer	
	def generate_solution(self):

		if len(self.waypoint_priority_queue) == 0 or (self.start_cell == None or self.ending_cell == None):
			mp = Mapa(self.mapa, self.start_cell,self.ending_cell)
			a = A_estrella(mp)
			if a.get_solucionable():
				self.print_solution(a.get_ruta())
			else:
				self.Dialog = QtGui.QDialog()
				self.popup_window = Ui_Error_Dialog(a.get_error())
				self.popup_window.setupUi(self.Dialog)
				self.Dialog.show()
		else:

			if self.AllowMultiProcessing == True: 
				print "multiprocessing"
				self.generate_solution_multiprocess_pipes()
				

			else:
				print "no multiprocessing"
				doable = True
				error = ""
				start = self.start_cell
				end = self.ending_cell
				waypoint_end=self.start_cell
				route = []
				route_aux =[]
				mp_aux=[]
				for i in range(len(self.waypoint_priority_queue)+1):
					waypoint_start = waypoint_end
					if i < len(self.waypoint_priority_queue):
						waypoint_end = self.waypoint_priority_queue[i]
					else:
						waypoint_end = end
					print ">>>>>>>>>>>>>>>>>>[DEBUG] waypoint_start ", waypoint_start, " waypoint_end ", waypoint_end
					'''
					mp_aux = copy.deepcopy(self.mapa)
					if end != None : mp_aux[end[0]][end[1]] = constants.get_empty_cell_value()
					if start != None : mp_aux[start[0]][start[1]] = constants.get_empty_cell_value()
					if waypoint_start != None: mp_aux[waypoint_start[0]][waypoint_start[1]] = constants.get_start_cell_value()
					if waypoint_end != None:mp_aux[waypoint_end[0]][waypoint_end[1]] = constants.get_ending_cell_value()
					'''
					mp = Mapa(self.mapa, waypoint_start, waypoint_end)
					a = A_estrella(mp)
					doable = doable and a.get_solucionable()
					if a.get_solucionable():
						route_aux.append(a.get_ruta())
						print ">>>>>>>>>>>>>>>>>>[DEBUG] waypoint_start ", waypoint_start, " waypoint_end ", waypoint_end, " waypoint route: " , route_aux
					else:
						error= a.get_error()

				if doable:
					route = [(route_aux[y][x][0],route_aux[y][x][1])  for y in range(len(route_aux)) for x in range(len(route_aux[y]))]
					print ">>>>>>>>>>>>>>>>>>[DEBUG] ruta final waypoints: ",route
					self.print_solution(route)
				else:
					self.Dialog = QtGui.QDialog()
					self.popup_window = Ui_Error_Dialog(error)
					self.popup_window.setupUi(self.Dialog)
					self.Dialog.show()
				
					
				
	''' attemp to define multithreading waypoints
		works fine but
		Suspicion: threading only runs on one core due to GLI restrictions, try multiprocessing lib
	 '''

	def generate_solution_multithread(self):

		local_data = threading.local()
		self.lock = threading.Lock()
		self.doable = True
		self.error = ""
		start = self.start_cell
		end = self.ending_cell
		waypoint_end=self.start_cell
		self.route = []
		self.route_aux = []
		threads = []
		
		for i in range(len(self.waypoint_priority_queue)+1):
			waypoint_start = waypoint_end
			if i < len(self.waypoint_priority_queue):
				waypoint_end = self.waypoint_priority_queue[i]
			else:
				waypoint_end = end
			thread = threading.Thread(target=self.run_thread, args=(local_data,waypoint_start,waypoint_end,))
			threads.append(thread)
			thread.start()
			print ">>>>>>>>>>>>>>>>>>[DEBUG] waypoint_start ", waypoint_start, " waypoint_end ", waypoint_end
		for thread in threads:
			thread.join()
		if self.doable:
			self.route = [(self.route_aux[y][x][0],self.route_aux[y][x][1])  for y in range(len(self.route_aux)) for x in range(len(self.route_aux[y]))]
			print ">>>>>>>>>>>>>>>>>>[DEBUG] ruta final waypoints: ",self.route
			self.print_solution(self.route)
		else:
			self.Dialog = QtGui.QDialog()
			self.popup_window = Ui_Error_Dialog(self.error)
			self.popup_window.setupUi(self.Dialog)
			self.Dialog.show()
		

	def run_thread(self,local_data,waypoint_start,waypoint_end):
		local_data.doable = True
		local_data.a = None
		local_data.mp = None
		local_data.error = None
		#local_data.start = self.start_cell
		#local_data.end = self.ending_cell	
		local_data.waypoint_start=waypoint_start
		local_data.waypoint_end=waypoint_end
		''' No es necesario con la nueva implementacion de mapa
		local_data.mp_aux=copy.deepcopy(self.mapa)
		if local_data.end != None : local_data.mp_aux[local_data.end[0]][local_data.end[1]] = constants.get_empty_cell_value()
		if local_data.start != None : local_data.mp_aux[local_data.start[0]][local_data.start[1]] = constants.get_empty_cell_value()
		if local_data.waypoint_start != None: local_data.mp_aux[local_data.waypoint_start[0]][local_data.waypoint_start[1]] = constants.get_start_cell_value()
		if local_data.waypoint_end != None: local_data.mp_aux[local_data.waypoint_end[0]][local_data.waypoint_end[1]] = constants.get_ending_cell_value()
		'''
		local_data.mp = Mapa(self.mapa, local_data.waypoint_start,local_data.waypoint_end)
		local_data.a = A_estrella(local_data.mp)
		local_data.doable = local_data.doable and local_data.a.get_solucionable()
		with self.lock:
			self.doable = self.doable and local_data.doable
			if local_data.doable:
				local_data.route = local_data.a.get_ruta()
				self.route_aux.append(local_data.route)
				print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Rutas parciales ",self.route_aux
			else:
				self.error = local_data.a.get_error()

	'''attemp to define multiprocessing waypoints
	works but blocks with tables too big, queue size limitations i suppose, let´s try pipes '''
	def generate_solution_multiprocess(self):

		self.doable = True
		self.error = ""
		waypoint_end=self.start_cell
		self.route = []
		processes = []
		self.multiprocess_result_queue = multiprocessing.Queue()
		self.multiprocess_error_queue = multiprocessing.Queue()
		route_aux=[]
		for i in range(len(self.waypoint_priority_queue)+1):
			waypoint_start = waypoint_end
			if i < len(self.waypoint_priority_queue):
				waypoint_end = self.waypoint_priority_queue[i]
			else:
				waypoint_end = end
			process = Process(target = run_process, args= (self.mapa,waypoint_start,waypoint_end,self.multiprocess_result_queue,self.multiprocess_error_queue,))
			processes.append(process)
			process.start()
			print ">>>>>>>>>>>>>>>>>>[DEBUG] waypoint_start ", waypoint_start, " waypoint_end ", waypoint_end
		for process in processes:
			process.join()
		if self.multiprocess_error_queue.qsize() == 0:
			while not self.multiprocess_result_queue.empty():
				route_aux.append(self.multiprocess_result_queue.get())
			self.route = [(route_aux[y][x][0],route_aux[y][x][1])  for y in range(len(route_aux)) for x in range(len(route_aux[y]))]
			#print ">>>>>>>>>>>>>>>>>>[DEBUG] ruta final waypoints: ",self.route
			self.print_solution(self.route)
		else:
			self.Dialog = QtGui.QDialog()
			self.popup_window = Ui_Error_Dialog(self.multiprocess_error_queue.get())
			self.popup_window.setupUi(self.Dialog)
			self.Dialog.show()
	'''attemp to define multiprocessing waypoints with pipes
	works fine

	-Tests
		1M cell table:
		- 1m54s on secuential(25% cpu usage)
		- 1m14s on parrallel(75% cpu usage)
	'''
	def generate_solution_multiprocess_pipes(self):

		doable = True
		error = ""
		start = self.start_cell
		end = self.ending_cell
		waypoint_end=self.start_cell
		route = []
		processes = []
		route_pipes = []
		route_aux=[]
		for i in range(len(self.waypoint_priority_queue)+1):
			waypoint_start = waypoint_end
			if i < len(self.waypoint_priority_queue):
				waypoint_end = self.waypoint_priority_queue[i]
			else:
				waypoint_end = end
			#mp_aux=copy.deepcopy(mapa) Not needed any more
			parent_conn_route, child_conn_route = Pipe()
			route_pipes.append(parent_conn_route)
			process = Process(target = run_process_pipes, args= (self.mapa,waypoint_start,waypoint_end,child_conn_route,))
			process.start()
			print ">>>>>>>>>>>>>>>>>>[DEBUG] waypoint_start ", waypoint_start, " waypoint_end ", waypoint_end
		for i in range(len(route_pipes)):
			route_aux.append(route_pipes[i].recv())
			print "proces ",i, " recieved"
		if doable:
			route = [(route_aux[y][x][0],route_aux[y][x][1])  for y in range(len(route_aux)) for x in range(len(route_aux[y]))]
			print ">>>>>>>>>>>>>>>>>>[DEBUG] ruta final waypoints: ",route
			self.print_solution(route)
		else:
			self.Dialog = QtGui.QDialog()
			self.popup_window = Ui_Error_Dialog("")
			self.popup_window.setupUi(self.Dialog)
			self.Dialog.show()

	# Prints the result of A* on the table 
	def print_solution(self,route):

		for index in route:
			if self.mapa[index[0]][index[1]] == None:
				background=constants.get_waycell_empty_background()
			elif self.mapa[index[0]][index[1]][0] == "inicio":
				background=constants.get_waycell_start_background()
			elif self.mapa[index[0]][index[1]][0] == "meta":
				background=constants.get_waycell_ending_background()
			elif self.mapa[index[0]][index[1]][0] == "penalizacion":
				background=constants.get_waycell_setback_background()
			elif self.mapa[index[0]][index[1]][0] == "waypoint":
				background=constants.get_waycell_waypoint_background()
			else:
				background=constants.get_waycell_empty_background()

			self.centralwidget.findChild(QTableWidget, "table").item(index[0],index[1]).setBackground(background)



	# Method in charge of generating random maps
	def generate_random_map(self):
		self.clear_table()
		random.seed()
		obstaculos= int((random.random()%0.3)*len(self.mapa)*len(self.mapa[0]))
		penalizaciones= int((random.random()%0.3)*len(self.mapa)*len(self.mapa[0]))
		print "random obstaculos", obstaculos
		print "random penalizaciones", penalizaciones
		for i in range(obstaculos):
			x=int(random.random()*len(self.mapa))
			y=int(random.random()*len(self.mapa[0]))
			self.mapa[x][y] = constants.get_block_cell_value()
			self.centralwidget.findChild(QTableWidget, "table").item(x,y).setBackground(constants.get_block_background())
		for i in range(penalizaciones):
			x=int(random.random()*len(self.mapa))
			y=int(random.random()*len(self.mapa[0]))
			self.mapa[x][y] = constants.get_setback_cell_value()
			self.centralwidget.findChild(QTableWidget, "table").item(x,y).setBackground(constants.get_setback_background())


	# Event called when a table cell is clicked
	def item_clicked(self, index):
		
		#print index.row(), index.column()
		if  not self.mapa[index.row()][index.column()] is constants.get_waypoint_cell_value():
			if self.centralwidget.findChild(QRadioButton,"startRadio") is self.radioB:
				if self.start_cell != None:
					self.centralwidget.findChild(QTableWidget, "table").item(self.start_cell[0],self.start_cell[1]).setBackground(constants.get_empty_background())
					self.mapa[self.start_cell[0]][self.start_cell[1]] = constants.get_empty_cell_value()
				self.start_cell = (index.row(), index.column())
				self.centralwidget.findChild(QTableWidget, "table").item(self.start_cell[0],self.start_cell[1]).setBackground(constants.get_start_background())
				self.mapa[self.start_cell[0]][self.start_cell[1]] = constants.get_start_cell_value()
				if self.ending_cell == (index.row(), index.column()):
					self.ending_cell = None

			if self.centralwidget.findChild(QRadioButton,"blockRadio") is self.radioB:
				self.centralwidget.findChild(QTableWidget, "table").item(index.row(),index.column()).setBackground(constants.get_block_background())
				self.mapa[index.row()][index.column()] = constants.get_block_cell_value()
				if self.ending_cell == (index.row(), index.column()):
					self.ending_cell = None
				elif self.start_cell == (index.row(), index.column()):
					self.start_cell = None

			if self.centralwidget.findChild(QRadioButton,"endingRadio") is self.radioB:
				if self.ending_cell != None:
					self.centralwidget.findChild(QTableWidget, "table").item(self.ending_cell[0],self.ending_cell[1]).setBackground(constants.get_empty_background())
					self.mapa[self.ending_cell[0]][self.ending_cell[1]] = constants.get_empty_cell_value()
				self.ending_cell = (index.row(), index.column())
				self.centralwidget.findChild(QTableWidget, "table").item(self.ending_cell[0],self.ending_cell[1]).setBackground(constants.get_ending_background())
				self.mapa[self.ending_cell[0]][self.ending_cell[1]] = constants.get_ending_cell_value()
				if self.start_cell == (index.row(), index.column()):
					self.start_cell = None

			if self.centralwidget.findChild(QRadioButton,"setbackRadio") is self.radioB:
				self.centralwidget.findChild(QTableWidget, "table").item(index.row(),index.column()).setBackground(constants.get_setback_background())
				self.mapa[index.row()][index.column()] = constants.get_setback_cell_value()
				if self.ending_cell == (index.row(), index.column()):
					self.ending_cell = None
				elif self.start_cell == (index.row(), index.column()):
					self.start_cell = None

			if self.centralwidget.findChild(QRadioButton,"waypointRadio") is self.radioB:
				item=self.centralwidget.findChild(QTableWidget, "table").item(index.row(),index.column())
				self.waypoint_priority_queue.insert(len(self.waypoint_priority_queue),(index.row(),index.column()))
				item.setBackground(constants.get_waypoint_background())
				item.setTextAlignment(Qt.AlignHCenter)
				self.mapa[index.row()][index.column()] = constants.get_waypoint_cell_value()
				item.setText(str(len(self.waypoint_priority_queue)))
				if self.ending_cell == (index.row(), index.column()):
					self.ending_cell = None
				elif self.start_cell == (index.row(), index.column()):
					self.start_cell = None

	# Event called when a radio button is called
	def radio_clicked(self):
		self.radioB = self.centralwidget.sender()

	# Even that initializes the ui structure
	def setupUi(self, MainWindow):

		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		# Maximizes main window
		MainWindow.showMaximized()
		self.centralwidget = QtGui.QWidget(MainWindow)
		# Configures the master grid layout
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
		#self.gridLayoutWidget.setGeometry(MainWindow.geometry())
		self.gridLayoutWidget.setGeometry(MainWindow.visibleRegion().boundingRect())
		self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
		self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
		self.gridLayout.setMargin(20)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

		# Sets the elements in the grid layout

		#Sets the table
		table = QTableWidget(self.row_count,self.column_count)
		table.setObjectName(_fromUtf8("table"))
		table.setDragEnabled(False)
		table.setSelectionBehavior(QAbstractItemView.SelectItems)
		table.setSelectionMode(QAbstractItemView.SingleSelection)
		# Locks edit mode on every cell of the table
		for i in range(table.rowCount()):
			for j in range(table.columnCount()):
				item = QtGui.QTableWidgetItem()
				# execute the line below to every item you need locked
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				table.setItem(i, j, item)

		table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		#table.horizontalHeader().setVisible(False)
		table.verticalHeader().setResizeMode(QHeaderView.Stretch)
		#table.verticalHeader().setVisible(False)
		table.clicked.connect(self.item_clicked)
		self.gridLayout.addWidget(table,5,0,1,10)

		#Sets the button for solving
		button_solve = QPushButton("Solve")
		button_solve.setMinimumWidth(160)
		button_solve.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
		button_solve.clicked.connect(self.generate_solution)
		self.gridLayout.addWidget(button_solve,0,5,2,1,Qt.AlignRight)

		# Sets the button for randomizing maps
		button_random = QPushButton("Random Map")
		button_random.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		button_random.clicked.connect(self.generate_random_map)
		self.gridLayout.addWidget(button_random,1,2,Qt.AlignLeft)

		# Sets the button for map clearing
		button_clear_map = QPushButton("Clear Map")
		button_clear_map.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
		button_clear_map.clicked.connect(self.clear_table)
		self.gridLayout.addWidget(button_clear_map,0,4,2,1,Qt.AlignHCenter)

		# Sets the button for clearing the route
		button_clear_route = QPushButton("Clear Route")
		button_clear_route.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
		button_clear_route.clicked.connect(self.clear_route)
		self.gridLayout.addWidget(button_clear_route,0,3,2,1,Qt.AlignRight)

		# Sets the radio buttons
		start = QRadioButton("Start",MainWindow)
		start.setObjectName(_fromUtf8("startRadio"))
		start.clicked.connect(self.radio_clicked)
		start.setAutoExclusive(True)
		self.gridLayout.addWidget(start,0,0)
		start.setChecked(True)
		self.radioB = start

		ending= QRadioButton("End",MainWindow)
		ending.setObjectName(_fromUtf8("endingRadio"))
		ending.clicked.connect(self.radio_clicked)
		ending.setAutoExclusive(True)
		self.gridLayout.addWidget(ending,0,1)

		block= QRadioButton("Block",MainWindow)
		block.setObjectName(_fromUtf8("blockRadio"))
		block.clicked.connect(self.radio_clicked)
		block.setAutoExclusive(True)
		self.gridLayout.addWidget(block,0,2)

		setback= QRadioButton("Setback",MainWindow)
		setback.setObjectName(_fromUtf8("setbackRadio"))
		setback.clicked.connect(self.radio_clicked)
		setback.setAutoExclusive(True)
		self.gridLayout.addWidget(setback,1,0)

		waypoint= QRadioButton("Waypoint",MainWindow)
		waypoint.setObjectName(_fromUtf8("waypointRadio"))
		waypoint.clicked.connect(self.radio_clicked)
		waypoint.setAutoExclusive(True)
		self.gridLayout.addWidget(waypoint,1,1)

		MainWindow.setCentralWidget(self.centralwidget)

		# Menus
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menubar.setVisible(False)
		MainWindow.setMenuBar(self.menubar)
		
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		# End of elements´ asignment

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "Algorithm A*", None))

'''For some reason i cant subclass Process
'''
def run_process(mapa,waypoint_start,waypoint_end,multiprocess_result_queue,multiprocess_error_queue):
		doable = True
		a = None
		mp = None
		error = None
		'''
		mp_aux=copy.deepcopy(mapa)
		if end != None : mp_aux[end[0]][end[1]] = constants.get_empty_cell_value()
		if start != None : mp_aux[start[0]][start[1]] = constants.get_empty_cell_value()
		if waypoint_start != None: mp_aux[waypoint_start[0]][waypoint_start[1]] = constants.get_start_cell_value()
		if waypoint_end != None: mp_aux[waypoint_end[0]][waypoint_end[1]] = constants.get_ending_cell_value()
		'''
		mp = Mapa(mapa,waypoint_start,waypoint_end)
		a = A_estrella(mp)
		doable =a.get_solucionable()
		if doable:
			route = a.get_ruta()
			multiprocess_result_queue.put(route)
		else:
			multiprocess_error_queue.put(a.get_error())
def run_process_pipes(mapa,waypoint_start,waypoint_end,child_conn_route):
		doable = True
		a = None
		mp = None
		error = None
		#mp_aux=mapa
		route=[]
		'''
		if end != None : mp_aux[end[0]][end[1]] = constants.get_empty_cell_value()
		if start != None : mp_aux[start[0]][start[1]] = constants.get_empty_cell_value()
		if waypoint_start != None: mp_aux[waypoint_start[0]][waypoint_start[1]] = constants.get_start_cell_value()
		if waypoint_end != None: mp_aux[waypoint_end[0]][waypoint_end[1]] = constants.get_ending_cell_value()
		'''
		mp = Mapa(mapa,waypoint_start,waypoint_end)
		a = A_estrella(mp)
		doable =a.get_solucionable()
		if doable:
			route = a.get_ruta()
		child_conn_route.send(route)

		


