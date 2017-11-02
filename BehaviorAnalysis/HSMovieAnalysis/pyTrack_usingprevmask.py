#!/usr/bin/python

import deltaPix
import imageMode
import centroidTracking
import imageTools
import sys

pixThreshold = 0.005 # enter pixel threshold here
frameRate = 285 # enter frameRate here (usually 30 fps)
videoStream = imageTools.getVideoStream(sys.argv)
vidInfo = deltaPix.cmdLine(pixThreshold,frameRate,videoStream)
try:
	mpimg.imread('mode.png')
	print "mode file already generated"
except:
	print "generating mode file"
	vidInfo = imageMode.cmdLine(pixThreshold,frameRate,videoStream)
vidInfo = centroidTracking.cmdLine(pixThreshold,frameRate,videoStream)
