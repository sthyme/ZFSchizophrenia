#-----------------------
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'selectUI.ui'
# Created: Thu Feb 26 13:45:32 2015 by: PyQt4 UI code generator 4.11.3
#
# Created by Emily Conklin
# February 2015
# This program is connected to the main widget (NeuroGUI.py) and is a sub-user interface
# Called from imageTools.setCameraResolution
# Allows the user to specify:
#   1) default resolution
#   2) fit-to-screen resolution
#   3) fit-to-projector resolution
#-----------------------

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

class Ui_setResolutionWidget(QtGui.QDialog):
    '''
    sub-window class - QDialog type
    '''
    def __init__(self):
        '''
        initializes the dialog, data member
        '''
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.videoType=0
    
    def setupUi(self, setResolutionWidget):
        '''
        called in the initialization method
        sets up each layout, labels, buttons, etc.
        '''
        setResolutionWidget.setObjectName(_fromUtf8("setResolutionWidget"))
        setResolutionWidget.resize(404, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(setResolutionWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        
        #line 1: label for desired resolution
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.desiredResolutionLabel = QtGui.QLabel(setResolutionWidget)
        self.desiredResolutionLabel.setObjectName(_fromUtf8("desiredResolutionLabel"))
        self.horizontalLayout.addWidget(self.desiredResolutionLabel)
        
        #lines 2,3,4: resolution options
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.defaultResRB = QtGui.QRadioButton(setResolutionWidget)
        self.defaultResRB.setObjectName(_fromUtf8("defaultResRB"))
        self.verticalLayout_3.addWidget(self.defaultResRB)
        self.fitToScreenLE = QtGui.QRadioButton(setResolutionWidget)
        self.fitToScreenLE.setObjectName(_fromUtf8("fitToScreenLE"))
        self.verticalLayout_3.addWidget(self.fitToScreenLE)
        self.fitToProjectorLE = QtGui.QRadioButton(setResolutionWidget)
        self.fitToProjectorLE.setObjectName(_fromUtf8("fitToProjectorLE"))
        self.verticalLayout_3.addWidget(self.fitToProjectorLE)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.defaultResRB.setChecked(True) #defaults default resolution
        
        #sets up button group with the three options
        self.buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup.addButton(self.defaultResRB,0)
        self.buttonGroup.addButton(self.fitToScreenLE,1)
        self.buttonGroup.addButton(self.fitToProjectorLE,2)
        
        #line 5: submit button
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.Submit = QtGui.QPushButton(setResolutionWidget)
        self.Submit.setObjectName(_fromUtf8("Submit"))
        self.horizontalLayout_4.addWidget(self.Submit)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        
        self.retranslateUi(setResolutionWidget)
        QtCore.QMetaObject.connectSlotsByName(setResolutionWidget)
    
    def retranslateUi(self, setResolutionWidget):
        '''
        called in the setup method
        sets label/button text and window titles
        links buttons to other methods
        '''
        setResolutionWidget.setWindowTitle(_translate("setResolutionWidget", "Resolution Options", None))
        self.desiredResolutionLabel.setText(_translate("setResolutionWidget", "Choose desired resolution:", None))
        self.defaultResRB.setText(_translate("setResolutionWidget", "Default resolution", None))
        self.fitToScreenLE.setText(_translate("setResolutionWidget", "Fit to screen (~720p)", None))
        self.fitToProjectorLE.setText(_translate("setResolutionWidget", "Fit to projector (~480p)", None))
        self.Submit.setText(_translate("setResolutionWidget", "Submit",None))
        
        #finds out which radio button was pressed
        self.defaultResRB.clicked.connect(self.readSignal)
        self.fitToScreenLE.clicked.connect(self.readSignal)
        self.fitToProjectorLE.clicked.connect(self.readSignal)
        
        self.Submit.clicked.connect(self.submitClose) #connects submit button to submitClose
    
    def readSignal(self):
        '''
        checks button group signal to determine radio button clicked
        '''
        self.videoType = self.buttonGroup.checkedId() #checks radio button signal
    
    def submitClose(self):
        '''
        closes window when user hits submit, passes videoType
        '''
        self.accept()

if __name__=='__main__':
    '''
    main function to test widget as a standalone
    '''
    app=QtGui.QApplication(sys.argv)
    ex=Ui_setResolutionWidget()
    ex.show()
    sys.exit(app.exec_())
