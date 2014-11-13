'''
Generate a .exe binary from .py files
'''

from distutils.core import setup
import py2exe

type = raw_input('Indicates what kind of application you want generate [console/gui]: ')

if type == 'console':

	setup(console=['main.py'])

else:
	setup(windows=['ui_main.py'])
