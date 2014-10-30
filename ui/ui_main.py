import sys
from PyQt4.QtGui import QApplication, QDialog, QMainWindow,QSizePolicy
from PyQt4 import QtGui
from seleccion import Ui_Dialog
from tablero import Ui_MainWindow

class VentanaSeleccion(QDialog, Ui_Dialog):
	def aceptar_listener(self):
		self.accept()

	def __init__(self):
		QDialog.__init__(self)

		# Set up the user interface from Designer.
		self.ui = Ui_Dialog
		self.setupUi(self)

		# Connect up the buttons.
		self.bttn_aceptar.clicked.connect(self.aceptar_listener)
		self.bttn_cancelar.clicked.connect(self.reject)

class Tablero(QMainWindow, Ui_MainWindow):

	def boton_clicked(self):
		boton = self.sender()
		indice = self.gridLayout.indexOf(boton)
		posicion = self.gridLayout.getItemPosition(indice)
		print "boton", boton, "at row/col", posicion[:2], "size ", boton.size()

	def __init__(self, x, y):
		QMainWindow.__init__(self)

		self.ui = Ui_MainWindow
		self.setupUi(self)

		for row in xrange(3):
			for col in xrange(3):
				boton = QtGui.QPushButton("boton %d-%d" % (row,col))
				boton.setFlat(True)
				boton.clicked.connect(self.boton_clicked)
				self.gridLayout.addWidget(boton,row,col)
				
		print(self.gridLayout.maximumSize())

		


app = QApplication(sys.argv)
window = Tablero(3,4)
window.show()
sys.exit(app.exec_())
