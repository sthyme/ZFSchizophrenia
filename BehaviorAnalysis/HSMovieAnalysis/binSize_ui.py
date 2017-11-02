#------------------------
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'binsize.ui'
# Created: Tue Feb 24 19:23:36 2015 by: PyQt4 UI code generator 4.11.3
#
# Created by Emily Conklin
# February 2015
# This program is called from main widget (NeuroGUI.py) and is a sub-user interface
# It gets a bin size as user input (default is 6)
# For use in analyzing average activity over binned frames (grouped regions of interest) 
#------------------------

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

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

class Ui_BinSize(QtGui.QDialog):
    '''
    sub-window class - QDialog type
    '''
    def __init__(self):
        '''
        initializes the dialog, data members
        '''
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.binSizeOut=""
    
    def setupUi(self, BinSize):
        '''
        called in the initialization method
        sets up each layout, labels, button, etc.
        '''
        BinSize.setObjectName(_fromUtf8("BinSize"))
        BinSize.resize(250, 100)
        BinSize.setMaximumSize(QtCore.QSize(250, 100))
        self.verticalLayout_2 = QtGui.QVBoxLayout(BinSize)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        
        #line 1: bin size label and line entry
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.BinSizeLabel = QtGui.QLabel(BinSize)
        self.BinSizeLabel.setObjectName(_fromUtf8("BinSizeLabel"))
        self.horizontalLayout.addWidget(self.BinSizeLabel)
        self.BinSizeLE = QtGui.QLineEdit(BinSize)
        self.BinSizeLE.setMaximumSize(QtCore.QSize(100, 16777215))
        self.BinSizeLE.setObjectName(_fromUtf8("BinSizeLE"))
        
        #line 2: submit button
        self.horizontalLayout.addWidget(self.BinSizeLE)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Submit = QtGui.QPushButton(BinSize)
        self.Submit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.Submit.setObjectName(_fromUtf8("Submit"))
        self.horizontalLayout_2.addWidget(self.Submit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(BinSize)
        QtCore.QMetaObject.connectSlotsByName(BinSize)

    def retranslateUi(self, BinSize):
        '''
        called in the setup method
        sets label/button text and window titles
        links buttons to other methods
        '''
        BinSize.setWindowTitle(_translate("BinSize", "Bin Size", None))
        self.BinSizeLabel.setText(_translate("BinSize", "Enter bin size:", None))
        self.Submit.setText(_translate("BinSize", "Submit", None))
        self.BinSizeLE.setText("6") #sets default bin size to 6
        self.Submit.clicked.connect(self.getBinSize)

    def getBinSize(self):
        self.binSizeOut=self.BinSizeLE.text() #gets bin size from line edit upon hitting submit
        self.accept() #closes window

if __name__=='__main__':
    '''
    main function to test widget as a standalone
    '''
    app=QtGui.QApplication(sys.argv)
    ex=Ui_BinSize()
    ex.show()
    sys.exit(app.exec_())