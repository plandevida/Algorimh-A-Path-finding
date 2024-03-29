
from PyQt4 import *
from PyQt4.Qt import *
from PyQt4.QtGui import *

# Define constant values 

''' A* constants'''
def debugMode():
	return False

def algorimthReLink():
	return True

''' Constants for random in-route apparitions '''
'''Not implemented'''
def get_random_background():
	return QBrush ( Qt.green, Qt.CrossPattern )
def get_random_cell_value():
	return ("penalizacion", 15)
def get_in_cell_background():
	return QBrush ( Qt.green, Qt.CrossPattern )

'''Main Ui constants'''
'''Size of the board'''
def get_table_x():
	return 30
def get_table_y():
	return 30
def allow_multiprocessing():
	return False
'''
	Background color constants
'''
def get_start_background():
	return QBrush ( Qt.green, Qt.CrossPattern )
def get_ending_background():
	return QBrush ( Qt.red, Qt.Dense2Pattern )
def get_block_background():
	return QBrush ( Qt.black, Qt.SolidPattern )
def get_setback_background():
	return QBrush ( Qt.gray, Qt.SolidPattern )
def get_empty_background():
	return QBrush ( Qt.white, Qt.SolidPattern )
def get_waypoint_background():
	return QBrush ( Qt.yellow, Qt.SolidPattern )

'''
	waycell background colors
'''
def get_waycell_empty_background():
	return QBrush ( Qt.blue, Qt.SolidPattern )
def get_waycell_start_background():
	return QBrush ( Qt.green, Qt.CrossPattern )
def get_waycell_ending_background():
	return QBrush ( Qt.red, Qt.Dense2Pattern )
def get_waycell_waypoint_background():
	return QBrush ( Qt.blue, Qt.Dense7Pattern )
def get_waycell_setback_background():
	return QBrush ( Qt.darkBlue, Qt.SolidPattern )

	'''
		Guis map constants
	'''
def get_empty_cell_value():
	return ("vacio",0)
def get_block_cell_value():
	return ("obstaculo",0)
def get_setback_cell_value():
	return ("penalizacion",0.4)
def get_start_cell_value():
	return ("inicio",0)
def get_ending_cell_value():
	return ("meta",0)
def get_waypoint_cell_value():
	return ("waypoint",0)

