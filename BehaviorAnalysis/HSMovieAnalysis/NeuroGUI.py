#-----------------------
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'NeuroGUI2.ui'
# Created: Tue Feb 10 21:29:43 2015 by: PyQt4 UI code generator 4.11.3
#
# Created by Emily Conklin
# February 2015
# This program is the main user interface for a motion detecting program
# It calls programs that take video input and obtain a difference video through frame differences
# And functions that perform data analysis based on user input
#-----------------------

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import numpy as np
import motionTools
import roiSelect
import imageTools
import deltaPix
import setResolutionWidget
import SGROIWidget_ui
import binSize_ui

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

class Ui_ROIGUI(QtGui.QWidget):
    '''
    main window widget class - QWidget type
    '''
    def __init__(self):
        '''
        initializes the widget, certain defaults
        '''
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.roiGroups={}
        self.binSize=6
        self.filenames=(str(os.path.dirname(os.path.realpath(__file__))))
        self.pixThreshold=0.03
        self.frameRate=30.0
        self.vidFile=""
        self.dataCondition=False
        self.numROI=0
        self.innerRects=0

    def setupUi(self, ROIGUI):
        '''
        called in the initialization method
        sets up each layout, tab, button, etc. on widget interface
        '''
        #sets up widget, tabs, basic layout
        ROIGUI.setObjectName(_fromUtf8("ROIGUI"))
        ROIGUI.resize(518, 413)
        self.verticalLayout_5 = QtGui.QVBoxLayout(ROIGUI)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.Tabs = QtGui.QTabWidget(ROIGUI)
        self.Tabs.setObjectName(_fromUtf8("Tabs"))

        #TAB ONE: VIDEO SETUP
        #line one: video input select, live feed, recorded video
        self.VideoSetup = QtGui.QWidget()
        self.VideoSetup.setObjectName(_fromUtf8("VideoSetup"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.VideoSetup)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.VideoInputSelect = QtGui.QLabel(self.VideoSetup)
        self.VideoInputSelect.setObjectName(_fromUtf8("VideoInputSelect"))
        self.horizontalLayout_3.addWidget(self.VideoInputSelect)
        self.LiveFeed = QtGui.QRadioButton(self.VideoSetup)
        self.LiveFeed.setObjectName(_fromUtf8("LiveFeed"))
        self.LiveFeed.setChecked(True)
        self.horizontalLayout_3.addWidget(self.LiveFeed)
        self.RecordedVideo = QtGui.QRadioButton(self.VideoSetup)
        self.RecordedVideo.setObjectName(_fromUtf8("RecordedVideo"))
        self.horizontalLayout_3.addWidget(self.RecordedVideo)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        #line two: pixel difference threshold, frame rate
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.PixThresholdLabel = QtGui.QLabel(self.VideoSetup)
        self.PixThresholdLabel.setObjectName(_fromUtf8("PixThresholdLabel"))
        self.horizontalLayout_11.addWidget(self.PixThresholdLabel)
        self.pixThresholdLE = QtGui.QLineEdit(self.VideoSetup)
        self.pixThresholdLE.setMaximumSize(QtCore.QSize(75, 16777215))
        self.pixThresholdLE.setObjectName(_fromUtf8("pixThresholdLE"))
        self.horizontalLayout_11.addWidget(self.pixThresholdLE)
        self.frameRateLabel = QtGui.QLabel(self.VideoSetup)
        self.frameRateLabel.setObjectName(_fromUtf8("frameRateLabel"))
        self.horizontalLayout_11.addWidget(self.frameRateLabel)
        self.frameRateLE = QtGui.QLineEdit(self.VideoSetup)
        self.frameRateLE.setMaximumSize(QtCore.QSize(75, 16777215))
        self.frameRateLE.setObjectName(_fromUtf8("frameRateLE"))
        self.horizontalLayout_11.addWidget(self.frameRateLE)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        #line three: set inner recetangles
        self.horizontalLayoutRect = QtGui.QHBoxLayout()
        self.horizontalLayoutRect.setObjectName(_fromUtf8("horizontalLayoutRect"))
        self.innerRectLabel = QtGui.QLabel(self.VideoSetup)
        self.innerRectLabel.setObjectName(_fromUtf8("innerRectLabel"))
        self.horizontalLayoutRect.addWidget(self.innerRectLabel)
        self.innerRectCheck = QtGui.QCheckBox(self.VideoSetup)
        self.innerRectCheck.setObjectName(_fromUtf8("innerRectCheck"))
        self.horizontalLayoutRect.addWidget(self.innerRectCheck)
        spacerItemRect = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayoutRect.addItem(spacerItemRect)
        self.verticalLayout_4.addLayout(self.horizontalLayoutRect)

        #line four: parameter setup, select ROI, show/group ROI
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.ParameterSetup = QtGui.QLabel(self.VideoSetup)
        self.ParameterSetup.setObjectName(_fromUtf8("ParameterSetup"))
        self.horizontalLayout_5.addWidget(self.ParameterSetup)
        self.SelectROI = QtGui.QPushButton(self.VideoSetup)
        self.SelectROI.setObjectName(_fromUtf8("SelectROI"))
        self.horizontalLayout_5.addWidget(self.SelectROI)
        self.ShowGroupROI = QtGui.QPushButton(self.VideoSetup)
        self.ShowGroupROI.setObjectName(_fromUtf8("ShowGroupROI"))
        self.ShowGroupROI.setDisabled(True) #initially sets show/group button to disabled
        self.horizontalLayout_5.addWidget(self.ShowGroupROI)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        #line five: data setup, create new data, append to existing data
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.DataSteupLabel = QtGui.QLabel(self.VideoSetup)
        self.DataSteupLabel.setObjectName(_fromUtf8("DataSteupLabel"))
        self.horizontalLayout_10.addWidget(self.DataSteupLabel)
        self.newDataRB = QtGui.QRadioButton(self.VideoSetup)
        self.newDataRB.setObjectName(_fromUtf8("newDataRB"))
        self.newDataRB.setChecked(True)
        self.horizontalLayout_10.addWidget(self.newDataRB)
        self.appendDataRB = QtGui.QRadioButton(self.VideoSetup)
        self.appendDataRB.setObjectName(_fromUtf8("appendDataRB"))
        self.horizontalLayout_10.addWidget(self.appendDataRB)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        #line six: begin recording, run
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.label = QtGui.QLabel(self.VideoSetup)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_6.addWidget(self.label)
        self.RunRecording = QtGui.QPushButton(self.VideoSetup)
        self.RunRecording.setMinimumSize(QtCore.QSize(175, 0))
        self.RunRecording.setMaximumSize(QtCore.QSize(200, 16777215))
        self.RunRecording.setObjectName(_fromUtf8("RunRecording"))
        self.RunRecording.setDisabled(True) #initially sets run button to disabled
        self.horizontalLayout_6.addWidget(self.RunRecording)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        #sets up two button groups so that video input select and data setup can both be selected
        self.buttonGroup3 = QtGui.QButtonGroup(self.VideoSetup)
        self.buttonGroup3.addButton(self.LiveFeed)
        self.buttonGroup3.addButton(self.RecordedVideo)
        self.buttonGroup4 = QtGui.QButtonGroup(self.VideoSetup)
        self.buttonGroup4.addButton(self.newDataRB)
        self.buttonGroup4.addButton(self.appendDataRB)

        #TAB TWO: ANALYZE
        #line one: analysis options
        self.Tabs.addTab(self.VideoSetup, _fromUtf8(""))
        self.AnalyzeDisplay = QtGui.QWidget()
        self.AnalyzeDisplay.setEnabled(True)
        self.AnalyzeDisplay.setObjectName(_fromUtf8("AnalyzeDisplay"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.AnalyzeDisplay)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.AnalysisOptions = QtGui.QLabel(self.AnalyzeDisplay)
        self.AnalysisOptions.setMaximumSize(QtCore.QSize(200, 100))
        self.AnalysisOptions.setObjectName(_fromUtf8("AnalysisOptions"))
        self.verticalLayout_8.addWidget(self.AnalysisOptions)

        #analysis option pictures and radio buttons
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.totalPic = QtGui.QLabel(self.AnalyzeDisplay)
        self.totalPic.setMaximumSize(QtCore.QSize(50, 50))
        self.totalPic.setText(_fromUtf8(""))
        self.totalPic.setPixmap(QtGui.QPixmap(_fromUtf8("totalROIpic.png")))
        self.totalPic.setScaledContents(True)
        self.totalPic.setObjectName(_fromUtf8("totalPic"))
        self.horizontalLayout.addWidget(self.totalPic)
        self.ROITotalActivity = QtGui.QRadioButton(self.AnalyzeDisplay)
        self.ROITotalActivity.setObjectName(_fromUtf8("ROITotalActivity"))

        self.horizontalLayout.addWidget(self.ROITotalActivity)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.AnalyzeDisplay)
        self.label_2.setMaximumSize(QtCore.QSize(50, 50))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("barROIpic.png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.ROITimeVActivity = QtGui.QRadioButton(self.AnalyzeDisplay)
        self.ROITimeVActivity.setObjectName(_fromUtf8("ROITimeVActivity"))
        self.horizontalLayout_2.addWidget(self.ROITimeVActivity)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.AnalyzeDisplay)
        self.label_3.setMaximumSize(QtCore.QSize(50, 50))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8("groupedROIpic.png")))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.GroupedTimeVActivity = QtGui.QRadioButton(self.AnalyzeDisplay)
        self.GroupedTimeVActivity.setObjectName(_fromUtf8("GroupedTimeVActivity"))
        self.horizontalLayout_4.addWidget(self.GroupedTimeVActivity)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        #set up button group for analysis options
        self.buttonGroup = QtGui.QButtonGroup(self.AnalyzeDisplay)
        self.buttonGroup.addButton(self.ROITotalActivity,1) #Total activity signal = 1
        self.buttonGroup.addButton(self.ROITimeVActivity,2) #Time V Activity signal = 2
        self.buttonGroup.addButton(self.GroupedTimeVActivity,3) #Grouped signal = 3

        #select directory, browse
        self.verticalLayout_7.addLayout(self.verticalLayout_8)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.SelectFileToAnalyze = QtGui.QLabel(self.AnalyzeDisplay)
        self.SelectFileToAnalyze.setObjectName(_fromUtf8("SelectFileToAnalyze"))
        self.horizontalLayout_7.addWidget(self.SelectFileToAnalyze)
        self.lineEdit = QtGui.QLineEdit(self.AnalyzeDisplay)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_7.addWidget(self.lineEdit)
        self.Browse = QtGui.QPushButton(self.AnalyzeDisplay)
        self.Browse.setObjectName(_fromUtf8("Browse"))
        self.Browse.setCheckable(True)
        self.horizontalLayout_7.addWidget(self.Browse)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        #display
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.Display = QtGui.QPushButton(self.AnalyzeDisplay)
        self.Display.setMaximumSize(QtCore.QSize(175, 16777215))
        self.Display.setObjectName(_fromUtf8("Display"))
        self.horizontalLayout_8.addWidget(self.Display)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        #analysis option error - only shows up when no radio button is selected
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.analysisOptionError = QtGui.QLabel(self.AnalyzeDisplay)
        self.analysisOptionError.setObjectName(_fromUtf8("analysisOptionError"))
        self.verticalLayout_9.addWidget(self.analysisOptionError)
        self.verticalLayout_7.addLayout(self.verticalLayout_9)
        self.Tabs.addTab(self.AnalyzeDisplay, _fromUtf8(""))
        self.verticalLayout_5.addWidget(self.Tabs)
        #end tab 2

        self.retranslateUi(ROIGUI)
        QtCore.QMetaObject.connectSlotsByName(ROIGUI)

    def retranslateUi(self, ROIGUI):
        '''
        called in the setup method
        sets label/button text and window titles
        links buttons to other methods
        '''
        #below sets text for all labels, text boxes, etc.
        ROIGUI.setWindowTitle(_translate("ROIGUI", "PyTracker!", None))
        self.VideoInputSelect.setText(_translate("ROIGUI", "Video Input Select:", None))
        self.LiveFeed.setText(_translate("ROIGUI", "Live Feed", None))
        self.RecordedVideo.setText(_translate("ROIGUI", "Recorded Video", None))
        self.PixThresholdLabel.setText(_translate("ROIGUI", "Pixel Difference Threshold: ", None))
        self.pixThresholdLE.setText("0.03")
        self.frameRateLabel.setText(_translate("ROIGUI", "Frame Rate: ", None))
        self.frameRateLE.setText("30.0")
        self.innerRectLabel.setText(_translate("ROIGUI", "Split ROI into inner and outer rectangles?", None))
        self.ParameterSetup.setText(_translate("ROIGUI", "Parameter Setup:", None))
        self.SelectROI.setText(_translate("ROIGUI", "Select ROI", None))
        self.ShowGroupROI.setText(_translate("ROIGUI", "Show/Group ROI", None))
        self.DataSteupLabel.setText(_translate("ROIGUI", "Data Setup:", None))
        self.newDataRB.setText(_translate("ROIGUI", "Create new data", None))
        self.appendDataRB.setText(_translate("ROIGUI", "Append to existing data",None))
        self.label.setText(_translate("ROIGUI", "Begin Recording:", None))
        self.RunRecording.setText(_translate("ROIGUI", "Run", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.VideoSetup), _translate("ROIGUI", "Video Setup", None))
        self.AnalysisOptions.setText(_translate("ROIGUI", "Analysis Options:", None))
        self.ROITotalActivity.setText(_translate("ROIGUI", "Motion in each ROI vs. time", None))
        self.ROITimeVActivity.setText(_translate("ROIGUI", "Bar graphs of total motion in each ROI", None))
        self.GroupedTimeVActivity.setText(_translate("ROIGUI", "Average activity over binned frames (grouped ROI)", None))
        self.SelectFileToAnalyze.setText(_translate("ROIGUI", "Select directory:", None))
        self.Browse.setText(_translate("ROIGUI", "Browse...", None))
        self.lineEdit.setText(str(os.path.dirname(os.path.realpath(__file__))))
        self.Display.setText(_translate("ROIGUI", "Display", None))
        self.analysisOptionError.setText(_translate("ROIGUI", "ERROR: No analysis option selected", None))
        self.LiveFeed.setChecked(True)

        #hides error message until needed
        self.analysisOptionError.hide()
        self.Tabs.setTabText(self.Tabs.indexOf(self.AnalyzeDisplay), _translate("ROIGUI", "Analyze", None))

        #linking begins here
        self.LiveFeed.clicked.connect(self.liveFeedMethod)
        self.RecordedVideo.clicked.connect(self.recordedVideoMethod)
        self.pixThresholdLE.textEdited.connect(self.getPixThreshold)
        self.frameRateLE.textEdited.connect(self.getFrameRate)
        self.innerRectCheck.clicked.connect(self.getInnerRects)
        self.SelectROI.clicked.connect(self.selectROImethod)
        self.ShowGroupROI.clicked.connect(self.showGroupROImethod)
        self.newDataRB.clicked.connect(self.newData)
        self.appendDataRB.clicked.connect(self.appendData)
        self.RunRecording.clicked.connect(self.runRecordingMethod)
        self.Browse.clicked.connect(self.fileSelect)
        self.Display.clicked.connect(self.readSignal)

    #tab 1 functions begin here

    def liveFeedMethod(self):
        '''
        runs when live feed is selected
        leaves selected file blank so that the program will search for a camera
        '''
        self.vidFile=""

    def recordedVideoMethod(self):
        '''
        runs when recorded video is selected
        opens a file browsing dialog, then saves selected file as a string
        '''
        self.vidFile = ['movie',str(QFileDialog.getOpenFileName())] #updates self.vidFile to filename

    def getPixThreshold(self):
        '''
        runs when the user edits the pixel threshold
        resets pixThreshold from default (0.03) to user input
        '''
        self.pixThreshold=float(self.pixThresholdLE.text()) #updates self.pixThreshold to user input float

    def getFrameRate(self):
        '''
        runs when the user edits the frame rate
        resets frameRate from default (30.0) to user input
        '''
        self.frameRate=float(self.frameRateLE.text()) #updates self.frameRate to user input float

    def getInnerRects(self):
        '''
        sets inner rectangles either on (1) or off (0)
        depending on if box is checked
        '''
        if self.innerRectCheck.isChecked():
            self.innerRects=1
        else:
            self.innerRects=0

    def selectROImethod(self):
        '''
        runs when select ROI is selected
        passes a video file (either live feed or user selected file) to program 'imageTools'
        passes resulting video stream to program 'roiSelect'
        '''
        self.videoStream = imageTools.getVideoStream(self.vidFile) #gets videostream given video file
        gmask, numROI = roiSelect.main(self.videoStream)
        if numROI == 1:
            imageTools.UIRowsCols(gmask,self.innerRects)
        self.ShowGroupROI.setDisabled(False) #ungreys show/group ROI button

    def showGroupROImethod(self):
        '''
        runs when Show/Group ROI is selected
        runs another widget allowing user to define ROI groups
        saves input in dictionary form {group name: group members}
        '''
        imageTools.saveROI()
        dialog = SGROIWidget_ui.Ui_ShowGroupWidget() #opens new subwidget
        if dialog.exec_():
            self.roiGroups=dialog.roiGroups #updates self.roiGroups when new subwidget is closed
        self.RunRecording.setDisabled(False) #ungreys run button

    def newData(self):
        '''
        runs when New Data is selected
        saves data condition as a boolean (False) for use in method 'runRecordingMethod'
        '''
        self.dataCondition=False

    def appendData(self):
        '''
        runs when Append Data is selected
        saves data condition as a boolean (False) for use in method 'runRecordingMethod'
        '''
        self.dataCondition=True

    def runRecordingMethod(self):
        '''
        runs when Run is clicked
        if user has selected New Data, old data is deleted
        runs program 'deltaPix' and passes it pixel threshold, frame rate, and video stream
        '''
        if self.dataCondition==False:
            imageTools.deleteData('*.npy')
        deltaPix.main(self.pixThreshold,self.frameRate,self.videoStream)

    #tab 2 functions begin here

    def fileSelect(self):
        '''
        runs when Browse is clicked
        opens a browser to let user select a directory
        sets the name of this directory to the text box
        '''
        self.filenames = str(QFileDialog.getExistingDirectory(self)) #opens directory browser
        self.lineEdit.setText(self.filenames)   #sets text to selected directory
        QApplication.instance().processEvents() #updates text

    def readSignal(self):
        '''
        runs when one of the analysis option buttons is selected and display is clicked
        runs a different 'motionTools' function depending on the analysis option button
        '''
        signal = self.buttonGroup.checkedId() #reads integer signal from analysis options
        timeStamps,deltaPix,fps=motionTools.loadData(self.filenames+"/")

        if signal == 1:
            motionTools.motionInROI(timeStamps,deltaPix)
        elif signal == 2:
            motionTools.barTimeInROI(deltaPix)
        elif signal == 3:
            dialog2 = binSize_ui.Ui_BinSize() #runs subwidget to get bin size from user
            if dialog2.exec_(): #updates when subwidget closes
                self.binsize=int(dialog2.binSizeOut)
                motionTools.binActivity(timeStamps,deltaPix,self.frameRate,self.binSize,self.roiGroups)
        elif signal == -1:
            self.analysisOptionError.show()


if __name__=='__main__':
    '''
    runs the program itself and displays the widget
    '''
    app=QtGui.QApplication(sys.argv)
    ex=Ui_ROIGUI()
    ex.show()
    sys.exit(app.exec_())
