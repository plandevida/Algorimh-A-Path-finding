import sys
from PySide.QtGui import *
from PySide import QtGui
from ui.tablero import Ui_MainWindow
import constants

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow(constants.get_table_x(),constants.get_table_y(),AllowMultiProcessing=constants.allow_multiprocessing())
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
