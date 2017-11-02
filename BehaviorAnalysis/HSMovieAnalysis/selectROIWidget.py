#-----------------------
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'selectUI.ui'
# Created: Thu Feb 26 13:45:32 2015 by: PyQt4 UI code generator 4.11.3
#
# Created by Emily Conklin
# February 2015
# This program is connected to the main widget (NeuroGUI.py) and is a sub-user interface
# Called from imageTools.UIRowsCols
# Allows the user to break up one region of interest into a grid (max number ROI = 144)
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

class Ui_selectROIWidget(QtGui.QDialog):
    '''
    sub-window class - QDialog type
    '''
    def __init__(self):
        '''
        initializes the dialog
        '''
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
    
    def setupUi(self, selectROIWidget):
        '''
        called in the initialization method
        sets up each layout, labels, buttons, etc.
        '''
        selectROIWidget.setObjectName(_fromUtf8("selectROIWidget"))
        selectROIWidget.resize(300, 200)
        self.verticalLayout_2 = QtGui.QVBoxLayout(selectROIWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        
        #line 1: row entry label and line edit
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rowEntryLabel = QtGui.QLabel(selectROIWidget)
        self.rowEntryLabel.setObjectName(_fromUtf8("rowEntryLabel"))
        self.horizontalLayout_2.addWidget(self.rowEntryLabel)
        self.rowEntryLE = QtGui.QLineEdit(selectROIWidget)
        self.rowEntryLE.setMaximumSize(QtCore.QSize(75, 16777215))
        self.rowEntryLE.setObjectName(_fromUtf8("rowEntryLE"))
        self.horizontalLayout_2.addWidget(self.rowEntryLE)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        
        #line 2: column entry label and line edit
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.columnEntryLabel = QtGui.QLabel(selectROIWidget)
        self.columnEntryLabel.setObjectName(_fromUtf8("columnEntryLabel"))
        self.horizontalLayout_3.addWidget(self.columnEntryLabel)
        self.columnEntryLE = QtGui.QLineEdit(selectROIWidget)
        self.columnEntryLE.setMaximumSize(QtCore.QSize(75, 16777215))
        self.columnEntryLE.setObjectName(_fromUtf8("columnEntryLE"))
        self.horizontalLayout_3.addWidget(self.columnEntryLE)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        
        #error message 1 - invalid entry
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.errorLabel = QtGui.QLabel(selectROIWidget)
        self.horizontalLayout_5.addWidget(self.errorLabel)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.errorLabel.hide() #hides error message unless needed
        
        #error message 1 - too many ROIs
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem8)
        self.errorLabel2 = QtGui.QLabel(selectROIWidget)
        self.horizontalLayout_6.addWidget(self.errorLabel2)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.errorLabel2.hide() #hides error message unless needed
        
        #line 3: submit button
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.Submit = QtGui.QPushButton(selectROIWidget)
        self.Submit.setObjectName(_fromUtf8("Submit"))
        self.horizontalLayout_4.addWidget(self.Submit)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(selectROIWidget)
        QtCore.QMetaObject.connectSlotsByName(selectROIWidget)

    def retranslateUi(self, selectROIWidget):
        '''
        called in the setup method
        sets label/button text and window titles
        links buttons to other methods
        '''
        selectROIWidget.setWindowTitle(_translate("selectROIWidget", "ROI Select Options", None))
        self.rowEntryLabel.setText(_translate("selectROIWidget", "Enter number of rows: ", None))
        self.columnEntryLabel.setText(_translate("selectROIWidget", "Enter number of columns:", None))
        self.Submit.setText(_translate("selectROIWidget", "Submit",None))
        self.errorLabel.setText(_translate("selectROIWidget", "Error: Please enter valid integers.",None))
        self.errorLabel2.setText(_translate("selectROIWidget", "Error: Only 144 maximum ROIs are allowed. Please enter smaller values.",None))
    
        self.Submit.clicked.connect(self.submitClose) #connects submit button to method

    def submitClose(self):
        '''
        runs when 'submit' button is clicked
        checks user input to get # rows and columns
        once input is free of errors, closes window
        '''
        condition = False #two conditions must be met in order to close window
        condition2 = False
        
        try: #checks to make sure inputs are valid integers
            self.numRows=int(self.rowEntryLE.text()) #gets number of rows
            self.numColumns=int(self.columnEntryLE.text())  #gets number of columns
            condition = True #if integers, first condition is met
            self.errorLabel.hide()
            if self.numRows*self.numColumns<=144: #total # ROI can be no greater than 144
                condition2 = True #if below the maximum, second condition is met
                self.errorLabel2.hide()
            else:
                self.errorLabel2.show()
        
        except ValueError: #if bad input, show error message
            self.errorLabel.show()

        if condition and condition2:
            self.accept() #if user input is valid, close window

if __name__=='__main__':
    '''
    main function to test widget as a standalone
    '''
    app=QtGui.QApplication(sys.argv)
    ex=Ui_selectROIWidget()
    ex.show()
    sys.exit(app.exec_())

