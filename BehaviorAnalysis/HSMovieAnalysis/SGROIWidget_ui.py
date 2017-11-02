#-----------------------
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'ShowGroupROIWidget.ui'
# Created: Thu Feb 19 14:00:52 2015 by: PyQt4 UI code generator 4.11.3
#
# Created by Emily Conklin
# February 2015
# This program is called from main widget (NeuroGUI.py) and is a sub-user interface
# Allows the user to show and group the previously selected regions of interest
#------------------------

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import imageTools
import sys
import glob

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

class Ui_ShowGroupWidget(QtGui.QDialog):
    '''
    sub-window class - QDialog type
    '''
    def __init__(self):
        '''
        initializes the dialog, data members
        '''
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.roiGroups = {}
        self.numROI=imageTools.getNumROI()
    
    def setupUi(self, ShowGroupWidget):
        '''
        called in the initialization method
        sets up each layout, labels, buttons, etc. 
        '''
        #sets up dialog, basic layout
        ShowGroupWidget.setObjectName(_fromUtf8("ShowGroupWidget"))
        ShowGroupWidget.resize(594, 546)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ShowGroupWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        
        #sets selected ROI picture
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pic = QtGui.QLabel(ShowGroupWidget)
        self.pic.setMaximumSize(QtCore.QSize(600, 400))
        self.pic.setEnabled(True)
        self.pic.setText(_fromUtf8(""))
        self.pic.setPixmap(QtGui.QPixmap(_fromUtf8(glob.glob("roiMask*")[0])))
        self.pic.setScaledContents(True)
        self.pic.setObjectName(_fromUtf8("pic"))
        self.horizontalLayout.addWidget(self.pic)
        
        #sets label and line edit for prompt to enter number of groups
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.EnterGroupNum = QtGui.QLabel(ShowGroupWidget)
        self.EnterGroupNum.setMaximumSize(QtCore.QSize(16777215, 50))
        self.EnterGroupNum.setObjectName(_fromUtf8("EnterGroupNum"))
        self.horizontalLayout_2.addWidget(self.EnterGroupNum)
        self.EnterGroupNumLE = QtGui.QLineEdit(ShowGroupWidget)
        self.EnterGroupNumLE.setObjectName(_fromUtf8("EnterGroupNumLE"))
        self.horizontalLayout_2.addWidget(self.EnterGroupNumLE)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        
        #error message if invalid number of groups entered (must be between 1-3 inclusive)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.numGroupError = QtGui.QLabel(ShowGroupWidget)
        self.numGroupError.setObjectName(_fromUtf8("numGroupError"))
        self.horizontalLayout_5.addWidget(self.numGroupError)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.numGroupError.hide() #hides error message unless needed
        
        #instructions for entering group names and members
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.Instructions = QtGui.QLabel(ShowGroupWidget)
        self.Instructions.setObjectName(_fromUtf8("Instructions"))
        self.horizontalLayout_9.addWidget(self.Instructions)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        
        #setup for entering group names and members
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        #1 group
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(-1)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.group1 = QtGui.QLabel(ShowGroupWidget)
        self.group1.setObjectName(_fromUtf8("group1"))
        self.horizontalLayout_7.addWidget(self.group1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.groupname1 = QtGui.QLabel(ShowGroupWidget)
        self.groupname1.setObjectName(_fromUtf8("groupname1"))
        self.horizontalLayout_7.addWidget(self.groupname1)
        self.groupname1LE = QtGui.QLineEdit(ShowGroupWidget)
        self.groupname1LE.setObjectName(_fromUtf8("groupname1LE"))
        self.horizontalLayout_7.addWidget(self.groupname1LE)
        self.groupmem1 = QtGui.QLabel(ShowGroupWidget)
        self.groupmem1.setObjectName(_fromUtf8("groupmem1"))
        self.horizontalLayout_7.addWidget(self.groupmem1)
        self.groupmem1LE = QtGui.QLineEdit(ShowGroupWidget)
        self.groupmem1LE.setObjectName(_fromUtf8("groupmem1LE"))
        self.horizontalLayout_7.addWidget(self.groupmem1LE)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        
        #hiding group 1
        self.hideG1()
        
        #2 groups
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.group2 = QtGui.QLabel(ShowGroupWidget)
        self.group2.setObjectName(_fromUtf8("group2"))
        self.horizontalLayout_6.addWidget(self.group2)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.group2name = QtGui.QLabel(ShowGroupWidget)
        self.group2name.setObjectName(_fromUtf8("group2name"))
        self.horizontalLayout_6.addWidget(self.group2name)
        self.group2nameLE = QtGui.QLineEdit(ShowGroupWidget)
        self.group2nameLE.setObjectName(_fromUtf8("group2nameLE"))
        self.horizontalLayout_6.addWidget(self.group2nameLE)
        self.group2mem = QtGui.QLabel(ShowGroupWidget)
        self.group2mem.setObjectName(_fromUtf8("group2mem"))
        self.horizontalLayout_6.addWidget(self.group2mem)
        self.group2memLE = QtGui.QLineEdit(ShowGroupWidget)
        self.group2memLE.setObjectName(_fromUtf8("group2memLE"))
        self.horizontalLayout_6.addWidget(self.group2memLE)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        
        #hiding group 2
        self.hideG2()
        
        #3 groups
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(-1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.group3 = QtGui.QLabel(ShowGroupWidget)
        self.group3.setObjectName(_fromUtf8("group3"))
        self.horizontalLayout_3.addWidget(self.group3)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.group3name = QtGui.QLabel(ShowGroupWidget)
        self.group3name.setObjectName(_fromUtf8("group3name"))
        self.horizontalLayout_3.addWidget(self.group3name)
        self.group3nameLE = QtGui.QLineEdit(ShowGroupWidget)
        self.group3nameLE.setObjectName(_fromUtf8("group3nameLE"))
        self.horizontalLayout_3.addWidget(self.group3nameLE)
        self.group3mem = QtGui.QLabel(ShowGroupWidget)
        self.group3mem.setObjectName(_fromUtf8("group3mem"))
        self.horizontalLayout_3.addWidget(self.group3mem)
        self.group3memLE = QtGui.QLineEdit(ShowGroupWidget)
        self.group3memLE.setObjectName(_fromUtf8("group3memLE"))
        self.horizontalLayout_3.addWidget(self.group3memLE)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.Submit = QtGui.QPushButton(ShowGroupWidget)
        self.Submit.setObjectName(_fromUtf8("Submit"))
        self.horizontalLayout_4.addWidget(self.Submit)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        
        #hiding group 3
        self.hideG3()
        
        #error message if bad group member input (invalid integers)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.groupMemError = QtGui.QLabel(ShowGroupWidget)
        self.groupMemError.setObjectName(_fromUtf8("groupMemError"))
        self.horizontalLayout_8.addWidget(self.groupMemError)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.groupMemError.hide() #hides error message unless needed
        
        #error message if wrong group members entered
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem10)
        self.wrongGroupMem = QtGui.QLabel(ShowGroupWidget)
        self.wrongGroupMem.setObjectName(_fromUtf8("wrongGroupMem"))
        self.horizontalLayout_9.addWidget(self.wrongGroupMem)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem11)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.wrongGroupMem.hide() #hides error message unless needed
        
        #hiding instructions and submit button until needed
        self.Instructions.hide()
        self.Submit.hide()
        
        #connects submit button to corresponding function
        self.Submit.clicked.connect(self.Submitclose)
        
        self.retranslateUi(ShowGroupWidget)
        QtCore.QMetaObject.connectSlotsByName(ShowGroupWidget)

    def retranslateUi(self, ShowGroupWidget):
        '''
        called in the setup method
        sets label/button text and window titles
        links buttons to other methods
        '''
        #below sets text for all labels, text boxes, etc.
        ShowGroupWidget.setWindowTitle(_translate("ShowGroupWidget", "Show/Group ROI", None))
        self.EnterGroupNum.setText(_translate("ShowGroupWidget", "Enter number of ROI groups (3 max):", None))
        self.Instructions.setText(_translate("ShowGroupWidget", "Enter group members as integers seperated by a comma.", None))
        self.numGroupError.setText(_translate("ShowGroupWidget", "Error: Please enter an integer between 1 and 3.", None))
        self.groupMemError.setText(_translate("ShowGroupWidget", "Error: Please enter group members as comma-seperated integers.", None))
        self.wrongGroupMem.setText(_translate("ShowGroupWidget", "Error: Make sure all ROI are included.", None))
        self.group1.setText(_translate("ShowGroupWidget", "1st Group:", None))
        self.groupname1.setText(_translate("ShowGroupWidget", "Group name:", None))
        self.groupmem1.setText(_translate("ShowGroupWidget", "Group members:", None))
        self.group2.setText(_translate("ShowGroupWidget", "2nd Group:", None))
        self.group2name.setText(_translate("ShowGroupWidget", "Group name:", None))
        self.group2mem.setText(_translate("ShowGroupWidget", "Group members:", None))
        self.group3.setText(_translate("ShowGroupWidget", "3rd Group:", None))
        self.group3name.setText(_translate("ShowGroupWidget", "Group name:", None))
        self.group3mem.setText(_translate("ShowGroupWidget", "Group members:", None))
        self.Submit.setText(_translate("ShowGroupWidget", "Submit", None))
        
        #runs numGroups when text has been entered in the corresponding line edit
        self.EnterGroupNumLE.textEdited.connect(self.numGroups)

    def numGroups(self):
        '''
        gets number of ROI groups as input from user
        maximum number of three groups
        '''
        numGroups=self.EnterGroupNumLE.text()
        if numGroups !="": #once something has been entered in the box
            try: #if input is a valid integer
                numGroups = int(numGroups)
                if 0<int(numGroups)<4:
                    #shows submit button
                    self.Submit.show()
                    self.numGroupError.hide()
                    #shows name/member input rows based on number of groups
                    if numGroups==1:
                        self.Instructions.hide()
                        self.hideG1()
                        self.group1.show()
                        self.groupname1.show()
                        self.groupname1LE.show()
                        self.hideG2()
                        self.hideG3()
                    elif numGroups==2:
                        self.Instructions.show()
                        self.showG1()
                        self.showG2()
                        self.hideG3()
                    elif numGroups==3:
                        self.Instructions.show()
                        self.showG1()
                        self.showG2()
                        self.showG3()
                else: #if input is not between 1 and 3 inclusive, display error
                    self.numGroupError.show()
            except ValueError: #if input is not a valid integer, display error
                self.numGroupError.show()

    def showG1(self):
        '''
        shows first name/member input line
        '''
        self.group1.show()
        self.groupname1.show()
        self.groupname1LE.show()
        self.groupmem1.show()
        self.groupmem1LE.show()

    def hideG1(self):
        '''
        hides first name/member input line
        '''
        self.group1.hide()
        self.groupname1.hide()
        self.groupname1LE.hide()
        self.groupmem1.hide()
        self.groupmem1LE.hide()

    def showG2(self):
        '''
        shows second name/member input line
        '''
        self.group2.show()
        self.group2name.show()
        self.group2nameLE.show()
        self.group2mem.show()
        self.group2memLE.show()
    
    def hideG2(self):
        '''
        hides second name/member input line
        '''
        self.group2.hide()
        self.group2name.hide()
        self.group2nameLE.hide()
        self.group2mem.hide()
        self.group2memLE.hide()
    
    def showG3(self):
        '''
        shows third name/member input line
        '''
        self.group3.show()
        self.group3name.show()
        self.group3nameLE.show()
        self.group3mem.show()
        self.group3memLE.show()
    
    def hideG3(self):
        '''
        hides third name/member input line
        '''
        self.group3.hide()
        self.group3name.hide()
        self.group3nameLE.hide()
        self.group3mem.hide()
        self.group3memLE.hide()

    def Submitclose(self):
        '''
        runs when 'submit' button is clicked
        checks and compiles user input into roiGroup dictionary {name: members}
        once input is free of errors, closes window
        '''
        #both conditions must be met in order for window to close
        condition = False
        condition2 = False
        
        #gets groups names from user input
        groupName1=str(self.groupname1LE.text())
        groupName2=str(self.group2nameLE.text())
        groupName3=str(self.group3nameLE.text())
        
        #set up list of group names
        groupNameList=[groupName1,groupName2,groupName3]
        #removes all empty strings from group namelist
        groupNameList = filter(lambda a: a!="", groupNameList)
        
        #gets a list based on number of ROIs
        roiList = []
        for i in range(1,self.numROI+1):
            roiList.append(i)
        
        #if only one group, sets members equal to numbers of all roi
        if len(groupNameList)==1:
            self.roiGroups[groupNameList[0]]=roiList
            condition = True
            condition2 = True
        
        #if there are two or three groups
        else:   
            groupMem1=str(self.groupmem1LE.text())
            groupMem2=str(self.group2memLE.text())
            groupMem3=str(self.group3memLE.text())
        
            #set up list of group members
            groupMemList=[groupMem1,groupMem2,groupMem3]
            #removes all empty strings from group memlist
            groupMemList = filter(lambda a: a!="", groupMemList)
        
            try:
                testList=[]
                for i in range(len(groupMemList)):
                    groupMemList[i] = groupMemList[i].split(",")    #splits group members by commas
                    for j in range(len(groupMemList[i])):
                        groupMemList[i][j]=int(groupMemList[i][j])
                        testList.append(groupMemList[i][j])
                    self.roiGroups[groupNameList[i]]=groupMemList[i]
                    self.groupMemError.hide()
                    condition = True    #first condition is met if user input is correctly formatted
                if sorted(roiList)==sorted(testList):   #if compiled list contains all roi members
                    self.wrongGroupMem.hide()
                    condition2 = True       #second condition is met
                else:
                    self.wrongGroupMem.show()   #if not, show error message
    
            except ValueError: #if bad input, show error message
                self.groupMemError.show()

        if condition and condition2:
            self.accept()   #if user input is valid, close window


if __name__=='__main__':
    '''
    main function to test widget as a standalone
    '''
    app=QtGui.QApplication(sys.argv)
    ex=Ui_ShowGroupWidget()
    ex.show()
    sys.exit(app.exec_())

