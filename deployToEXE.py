'''
Generate a .exe binary from .py files
'''

from distutils.core import setup
import py2exe
from glob import glob
import sys
#data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
# sys.path.append("C:\\Users\W8.1 BSoD\\Downloads\\Sublime Text 2.0.2\\")
#data_files=data_files,
setup(windows=['ui_main.py'], options={"py2exe": {"includes": ["sip", "PyQt4.QtGui"]}})