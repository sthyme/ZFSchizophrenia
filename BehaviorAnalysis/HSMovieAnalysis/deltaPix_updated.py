#!/usr/bin/python -tt

"""
This script collects pixel differences between video frames
and saves these differences to a file or files with the extension '.npy'

USAGE: python deltaPix.py [videoFile]

If no video file is specified, live video is processed
If a video file is specified, this script runs through the video frame by frame

STUFF THAT CAN BE ADJUSTED:
pixel threshold  =   how many pixels is a real movement?
experiment length: this is only relevant for live video: see expDuration below
    experiment length can also be manually set by hitting 'q' during the video feed
frameRate = this is used to set the timestamps of each video frame
    estimated at 30 fps, but user may adjust
    This script will report how many frames were analyzed
    To set actual fps, run script to calculate # frames,
    and divide by running length of the video
    Enter this number into 'frameRate' below, and rerun this script

NEED:
1) the two output files automatically created by roiSelect.py: image.png and mask.png
2) the imageTools.py set of tools

NOTE:
Before this script runs, it will ask you if you want to
(a)append new data to the .npy file(s) already in the directory
(n)ew experiment: clear out old .npy files before running the analysis

"""

# IMPORT NECESSARY MODULES
import matplotlib.image as mpimg
import numpy as np
import cv2
from datetime import datetime, timedelta
import sys
import imageTools
import motionTools
#from collections import dequeue
from scipy.stats import mode

def calc_mode(deq, nump_arr):
	for j,k in enumerate(nump_arr[:,0]): #so k are the values, j are the indicies. all cols will be 1504. so j will reach 1504
		nump_arr[j,:] = mode(np.array([x[j,:] for x in deq]))[0]
	return nump_arr

def main(pixThreshold,frameRate,videoStream):

	expDuration = 600000 # duration of experiment, in seconds; only relevant for live feed
	saveFreq = 4500 # how often to save data, in frames
	i,m = imageTools.loadImageAndMask()
	m,w = imageTools.convertMaskToWeights(m)
	videoType, displayDiffs = imageTools.getVideoType(videoStream)
	cap = cv2.VideoCapture(videoStream)
	print 'Camera resolution is %s x %s' % (str(m.shape[1]),str(m.shape[0]))
	cap.set(3,m.shape[1])
	cap.set(4,m.shape[0])
	ret,frame = cap.read()
	storedFrame = imageTools.grayBlur(frame)
	pixThreshold = int(np.floor( pixThreshold * storedFrame.shape[0] ))
	print('PixelThreshold is %i') % pixThreshold
	pixData = np.zeros([ saveFreq, len(np.unique(w)) + 1])
	i = 0 # a counter for saving chunks of data
	totalFrames = 0
	startTime = datetime.now()
	oldTime = startTime
	elapsed = 0
	print('Analyzing motion data...')
	moviedeq = []
	while(cap.isOpened()):
		ret,frame = cap.read()
		if ret == False:
			print 'End of Video'
			break
		currentFrame = imageTools.grayBlur(frame)
		moviedeq.append(currentFrame)
		diff = imageTools.diffImage(storedFrame,currentFrame,pixThreshold,displayDiffs)
		timeDiff = 1. / frameRate
		elapsed = elapsed + timeDiff
		counts = np.bincount(w, weights=diff.ravel())
		pixData[i,:] = np.hstack((elapsed,counts))
		totalFrames += 1
		storedFrame = currentFrame # comment out if nothing is in first frame
		i += 1
	pixData = pixData[:i,:]
	pixData = pixData[:,2:] # get rid of timing column and background column
	file = open(videoStream + ".motion2",'w')
	file.write("12/8/2015" + '\015')
	for x in range(0,285):
		#print "x", x
		for y in range(0,96):
			file.write(str(int(pixData[x,:][y])) + '\n')

	cap.release()
	cv2.destroyAllWindows()
	vidInfo = {}
	return vidInfo

def cmdLine(pixThreshold,frameRate,videoStream):
	vidInfo = main(pixThreshold,frameRate,videoStream)
	return vidInfo

if __name__ == '__main__':
	pixThreshold = imageTools.getPixThreshold(0.032)
	frameRate = imageTools.getFrameRate() # default is 30
	videoStream = imageTools.getVideoStream(sys.argv)
	vidInfo = cmdLine(pixThreshold,frameRate,videoStream)
