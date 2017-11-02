#!/usr/bin/python

import highspeedmovieanalysis
import imageTools
import sys

pixThreshold = 0.005 # enter pixel threshold here
frameRate = 285 # enter frameRate here (usually 30 fps)
videoStream = imageTools.getVideoStream(sys.argv)
#vidInfo = deltaPix.cmdLine(pixThreshold,frameRate,videoStream)
#vidInfo = deltaPix_updated.cmdLine(pixThreshold,frameRate,videoStream)
vidInfo = highspeedmovieanalysis.cmdLine(pixThreshold,frameRate,videoStream)
