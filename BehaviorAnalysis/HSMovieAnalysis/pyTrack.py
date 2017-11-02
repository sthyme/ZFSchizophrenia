#!/usr/bin/python

import roiSelect
import deltaPix
import imageTools
import sys

pixThreshold = 0.005 # enter pixel threshold here
frameRate = 285 # enter frameRate here (usually 30 fps)

# determine video input (use camera if no movie file specified)
videoStream = imageTools.getVideoStream(sys.argv)

# launch roi select
# if you select one rectangle it will ask for # row and columns to grid
roiSelect.cmdLine(videoStream)
