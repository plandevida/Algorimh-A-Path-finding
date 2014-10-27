import sys
from PyQt4.QtGui import QApplication, QDialog
from seleccion import Ui_Dialog

class VentanaSeleccion(QDialog, Ui_Dialog):
	def aceptar_listener(self):
		self.accept()

	def cancelar_listener(self):
		self.reject()

	def __init__(self):
		QDialog.__init__(self)

		# Set up the user interface from Designer.
		self.ui = Ui_Dialog
		self.setupUi(self)

		# Connect up the buttons.
		self.bttn_aceptar.clicked.connect(self.aceptar_listener)
		self.bttn_cancelar.clicked.connect(self.cancelar_listener)
app = QApplication(sys.argv)
window = VentanaSeleccion()



window.show()
sys.exit(app.exec_())