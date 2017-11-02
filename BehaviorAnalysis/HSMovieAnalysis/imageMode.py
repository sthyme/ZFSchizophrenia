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

def keepOrAppend(clearData):
	# check to see if clear existing data
	# or append this data to existing data
    if clearData == 'n':
    	print "Actually not clearing data, but need to make a new file anyway"
			#imageTools.deleteData('*.npy')
    else:
		print "Keeping existing data ..."

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
import glob,os

def calc_mode(deq, nump_arr):
	for j,k in enumerate(nump_arr[:,0]): #so k are the values, j are the indicies. all cols will be 1504. so j will reach 1504
		nump_arr[j,:] = mode(np.array([x[j,:] for x in deq]))[0]
	return nump_arr

def main(pixThreshold,frameRate,videoStream):

	expDuration = 600000 # duration of experiment, in seconds; only relevant for live feed
	saveFreq = 4500 # how often to save data, in frames

	i,m = imageTools.loadImageAndMask()

	# convert mask to integer values for bincount weights
	m,w = imageTools.convertMaskToWeights(m)
	#print m,w

	moviedeq = []
	i2=0
	for file in glob.glob("*_4*avi"):
		if i2 == 15:
			break
	#for x in range(0,5):

		# start camera or open video
		videoType, displayDiffs = imageTools.getVideoType(videoStream)
	#	print "testing: ", file
		#print "testing: ", videoStream.split('-')[x]
		cap = cv2.VideoCapture(file)
		#cap = cv2.VideoCapture(videoStream.split('-')[x])

		# adjust video resolution if necessary (sized to mask)
	#	print 'Camera resolution is %s x %s' % (str(m.shape[1]),str(m.shape[0]))
	#	cap.set(3,m.shape[1])
	#	cap.set(4,m.shape[0])

		# Set Pixel Threshold
		ret,frame = cap.read()
		storedFrame = imageTools.grayBlur(frame)
		#pixThreshold = int(np.floor( pixThreshold * storedFrame.shape[0] ))
		#print('PixelThreshold is %i') % pixThreshold

		# Acquire data
		if saveFreq / frameRate > expDuration: # do shorter of expDuration vs. saveFreq
				saveFreq = expDuration * frameRate

		pixData = np.zeros([ saveFreq, len(np.unique(w)) + 1])

		#i = 0 # a counter for saving chunks of data
		totalFrames = 0
		startTime = datetime.now()
		oldTime = startTime
		elapsed = 0

		print('Analyzing motion data...')

		#moviedeq = []

		while(cap.isOpened()):

			ret,frame = cap.read()

			if ret == False:
				print 'End of Video'
				break

			currentFrame = imageTools.grayBlur(frame)
			moviedeq.append(currentFrame)

			# stop experiment if user presses 'q' or if experiment duration is up
			if ( cv2.waitKey(1) & 0xFF == ord('q') or
				len(sys.argv) == 1 and datetime.now() > startTime + timedelta(seconds = expDuration)
				):
				break

			# record pixel differences in all of the ROIs
			#diff = imageTools.diffImage(storedFrame,currentFrame,pixThreshold,0)

			timeDiff = 1. / frameRate
			elapsed = elapsed + timeDiff
		#	print elapsed

			# calculate and record pixel differences
			#counts = np.bincount(w, weights=diff.ravel())
		#	print counts # output
			#pixData[i,:] = np.hstack((elapsed,counts))
			totalFrames += 1

			storedFrame = currentFrame # comment out if nothing is in first frame
			#oldTime = newTime
		i2 += 1

		# done recording. Remove empty rows (those bigger than i) from PixData
		#pixData = pixData[:i,:]
		#print pixData

	testing = calc_mode(moviedeq, np.zeros([660,1088]))
	print "saving mode.png"
	cv2.imwrite('mode.png', testing)

	# Save info (elapsed time and framerate) for later use
	vidInfo = {}
#	analysisTime = timeStamp - startTime
#	vidInfo['analysisTime'] = float(str(analysisTime.seconds) + '.' + str(analysisTime.microseconds))
#	vidInfo['TotalFrames'] = totalFrames
#	vidInfo['fps'] = int(totalFrames/vidInfo['analysisTime'])
#	#vidInfo['pixThreshold']=pixThreshold
#	vidInfo['CameraResolution']='%s x %s' % (str(m.shape[1]),str(m.shape[0]))
	#vidInfo['NamePrefix'] =  videoStream.split('-')[x]
	#vidInfo['NamePrefix'] =  videoStream.split('.')[0]

#	print ('Analyzed %i frames in %f seconds') % (vidInfo['TotalFrames'],vidInfo['analysisTime'])
#	print('FrameRate is about %i fps') % vidInfo['fps']
#	print 'Motion threshold is %i pixels' % int(pixThreshold)
#	print 'Camera resolution is %s' % vidInfo['CameraResolution']

	# release camera
	cap.release()
	cv2.destroyAllWindows()

	return vidInfo

def cmdLine(pixThreshold,frameRate,videoStream):
	#keepOrAppend('n')
	#keepOrAppend(raw_input("(a)ppend this new data, or (n)ew experiment?   >:"))
	vidInfo = main(pixThreshold,frameRate,videoStream)
	return vidInfo

if __name__ == '__main__':
	pixThreshold = imageTools.getPixThreshold(0.032)
	frameRate = imageTools.getFrameRate() # default is 30
	videoStream = imageTools.getVideoStreamMode(sys.argv)
	#videoStream = imageTools.getVideoStream(sys.argv)
	vidInfo = cmdLine(pixThreshold,frameRate,videoStream)


