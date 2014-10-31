# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablero.ui'
#
# Created: Thu Oct 30 23:17:33 2014
#      by: PyQt4 UI code generator 4.11.2
# Modified: Fri Oct 31 1:02:00 2014
#      by: Emilio Álvarez Piñeiro
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
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
	
	def __init__(self):
		self.mapa=[]
		self.radioB=None
	def solve_map(self):
		self.done()

	# Event called when a table cell is clicked
	def item_clicked(self, index):
		if self.centralwidget.findChildren(QRadioButton,"startRadio") is self.radioB:
			

	def radio_clicked(self,alredy_clicked):
		self.radioB = self.centralwidget.sender()

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
		table = QTableWidget(50,40)
		table.setObjectName(_fromUtf8("table"))
		table.setDragEnabled(False)
		table.setSelectionBehavior(QAbstractItemView.SelectItems)
		table.setSelectionMode(QAbstractItemView.SingleSelection)

		for i in range(table.rowCount()):
			for j in range(table.columnCount()):
				item = QtGui.QTableWidgetItem()
				# execute the line below to every item you need locked
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				table.setItem(i, j, item)
		#table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		#table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		table.horizontalHeader().setVisible(False)
		table.verticalHeader().setResizeMode(QHeaderView.Stretch)
		table.verticalHeader().setVisible(False)
		#Configures the signal listener
		table.clicked.connect(self.item_clicked)

		self.gridLayout.addWidget(table,5,0,1,10)
		#Sets the button for solving
		button_solve = QPushButton("Resolver")
		button_solve.setMinimumWidth(160)
		button_solve.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
		self.gridLayout.addWidget(button_solve,0,5,2,1,Qt.AlignRight)
		# Sets the button for randomizing maps
		button_random = QPushButton("Random Map")
		button_random.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		self.gridLayout.addWidget(button_random,1,2,Qt.AlignLeft)
		# Sets the radio buttons
		start = QRadioButton("Inicio",MainWindow)
		start.setObjectName(_fromUtf8("startRadio"))
		start.clicked.connect(self.radio_clicked)
		start.setAutoExclusive(True)
		self.gridLayout.addWidget(start,0,0)
		start.setChecked(True)
		self.radioB = start

		ending= QRadioButton("Meta",MainWindow)
		ending.setObjectName(_fromUtf8("Meta"))
		ending.clicked.connect(self.radio_clicked)
		ending.setAutoExclusive(True)
		self.gridLayout.addWidget(ending,0,1)

		block= QRadioButton("Bloque",MainWindow)
		block.setObjectName(_fromUtf8("Bloque"))
		block.clicked.connect(self.radio_clicked)
		block.setAutoExclusive(True)
		self.gridLayout.addWidget(block,0,2)

		setback= QRadioButton("Penalizacion",MainWindow)
		setback.setObjectName(_fromUtf8("Penalizacion"))
		setback.clicked.connect(self.radio_clicked)
		setback.setAutoExclusive(True)
		self.gridLayout.addWidget(setback,1,0)

		waypoint= QRadioButton("Waypoint",MainWindow)
		waypoint.setObjectName(_fromUtf8("Waypoint"))
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
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

