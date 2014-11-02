# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'seleccion.ui'
#
# Created: Mon Oct 27 23:51:29 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Selection_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 289)
        self.spinBox_x = QtGui.QSpinBox(Dialog)
        self.spinBox_x.setGeometry(QtCore.QRect(101, 120, 51, 22))
        self.spinBox_x.setObjectName(_fromUtf8("spinBox_x"))
        self.spinBox_y = QtGui.QSpinBox(Dialog)
        self.spinBox_y.setGeometry(QtCore.QRect(251, 120, 51, 22))
        self.spinBox_y.setObjectName(_fromUtf8("spinBox_y"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 100, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(260, 100, 46, 13))
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(125, 30, 161, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.bttn_aceptar = QtGui.QPushButton("Aceptar")
        self.bttn_aceptar.setGeometry(QtCore.QRect(210, 240, 75, 23))
        self.bttn_aceptar.setObjectName(_fromUtf8("bttn_aceptar"))
        self.bttn_cancelar = QtGui.QPushButton("Cancelar")
        self.bttn_cancelar.setGeometry(QtCore.QRect(300, 240, 75, 23))
        self.bttn_cancelar.setObjectName(_fromUtf8("bttn_cancelar"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "X axis", None))
        self.label_2.setText(_translate("Dialog", "Y axis", None))
        self.label_3.setText(_translate("Dialog", "Choose de size of the canvas", None))
        self.bttn_aceptar.setText(_translate("Dialog", "PushButton", None))
        self.bttn_cancelar.setText(_translate("Dialog", "PushButton", None))

