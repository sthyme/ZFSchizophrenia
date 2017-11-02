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

def calc_mode(deq, nump_arr):
	for j,k in enumerate(nump_arr[:,0]): #so k are the values, j are the indicies. all cols will be 1504. so j will reach 1504
		nump_arr[j,:] = mode(np.array([x[j,:] for x in deq]))[0]
	return nump_arr

def main(pixThreshold,frameRate,videoStream):

	#elate_loc={(1,1):1, (1,2):2, (1,3):3, (1,4):4, (1:5):5, (1,6):6, (1,7):7, (1,8):8, (1,9):9,(1,10):10,(1,11):11,(1,12):12,(2,1):13,(2,2):14,(2,3):15,(2,4):16,(2:5):17,(2,6):18,(2,7):19,(2,8):20,(2,9):21,(2,10):22,(2,11):23,(2,12):24,(3,1):25,(3,2):26,(3,3):27,(3,4):28,(3,5):29,(3,6):30,(3,7)}
	col={1:0,2:12,3:24,4:36,5:48,6:60,7:72,8:84}

	expDuration = 600000 # duration of experiment, in seconds; only relevant for live feed
	saveFreq = 4500 # how often to save data, in frames

	i,m = imageTools.loadImageAndMask()
	e = imageTools.loadModeImage()

	#print e
	#cv2.imwrite('testinge.jpg', e)
	#cv2.imwrite('testingm.jpg', m)
	#cv2.imwrite('testingi.jpg', i)
	# convert mask to integer values for bincount weights
	np.set_printoptions(threshold=np.nan) # printing entire array
	#print "mask1: ", np.shape(m), m
	m,w = imageTools.convertMaskToWeights(m)
	#print "mask2: ", np.shape(m), m
	unique = np.unique(m)
	#print np.shape(m)
	minr = set()
	minc = set()
	maxr = set()
	maxc = set()
	for x in unique:
		#print "x: ", x
		if x == 0:
			continue
		#print np.shape(np.where(m==x))
		#print np.where(m==x)
		maxdimc = np.amax(np.where(m==x)[0])
		maxc.add(maxdimc)
		#print "max dimc: ", np.amax(np.where(m==x)[0])
		maxdimr = np.amax(np.where(m==x)[1])
		maxr.add(maxdimr)
		#print "max dimr: ", np.amax(np.where(m==x)[1])
		mindimc = np.amin(np.where(m==x)[0])
		minc.add(mindimc)
		#print "min dimc: ", np.amin(np.where(m==x)[0])
		mindimr = np.amin(np.where(m==x)[1])
		minr.add(mindimr)
		#print "min dimr: ", np.amin(np.where(m==x)[1])
	#print minr, maxr, minc, maxc
	lminx = list(minr)
	lminx.sort()
	lmaxx = list(maxr)
	lmaxx.sort()
	lminy = list(minc)
	lminy.sort()
	lmaxy = list(maxc)
	lmaxy.sort()
	#print lminr, lmaxr, lminc, lmaxc
	#print np.where(m==75)
	#for x in len(m):
		#print m[x]
	#print "mask2: ", np.shape(m), m
	#print "mask: ", np.nonzero(m)
	#print m,w


	# start camera or open video
	videoType, displayDiffs = imageTools.getVideoType(videoStream)
	cap = cv2.VideoCapture(videoStream)

	# adjust video resolution if necessary (sized to mask)
	print 'Camera resolution is %s x %s' % (str(m.shape[1]),str(m.shape[0]))
	cap.set(3,m.shape[1])
	cap.set(4,m.shape[0])

	# Set Pixel Threshold
	ret,frame = cap.read()
	storedImage = np.array(e * 255, dtype = np.uint8)
	# have to convert the float32 to uint8, hopefully this is doing it correctly (found online)
	storedFrame = imageTools.Blur(storedImage)
	#storedFrame = imageTools.grayBlur(frame)
	pixThreshold = int(np.floor( pixThreshold * storedFrame.shape[0] ))
	print('PixelThreshold is %i') % pixThreshold

	# Acquire data
	if saveFreq / frameRate > expDuration: # do shorter of expDuration vs. saveFreq
			saveFreq = expDuration * frameRate

	pixData = np.zeros([ saveFreq, len(np.unique(w))*2 -2])

	i = 0 # a counter for saving chunks of data
	totalFrames = 0
	startTime = datetime.now()
	oldTime = startTime
	elapsed = 0

	print('Analyzing motion data...')

	moviedeq = []

	frame_roi = []

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

		diff = imageTools.trackdiffImage(storedFrame,currentFrame,pixThreshold,displayDiffs)
		diff.dtype = np.uint8
		_,contours,hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		MIN_THRESH = 20.0
		MIN_THRESH_P = 20.0
		#if cv2.contourArea(contours[0]) > MIN_THRESH:
		#	M = cv2.moments(contours[0])
		#	cX = int(M["m10"] / M["m00"])
		#	cY = int(M["m01"] / M["m00"])
	#		print cX,cY
		roi_dict = {}
		for r in range(0,96):
			roi_dict[r+1] = []
		for cs in range(0,len(contours)):
			if cv2.contourArea(contours[cs]) > MIN_THRESH or cv2.arcLength(contours[cs],True) > MIN_THRESH_P:
			#if cv2.contourArea(contours[cs]) > MIN_THRESH and cv2.arcLength(contours[cs],True) > MIN_THRESH_P:
				M = cv2.moments(contours[cs])
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				#print i, " cX and cY:", cX, cY
				#print lmaxx
				#print lmaxy
				r=1
				c=1
				for x in range(0,len(lmaxx)):
					if cX > lmaxx[x]:
						r=x+2
				#		print x, cX, lmaxx[x], lminx[x]
				for y in range(0, len(lmaxy)):
					if cY > lmaxy[y]:
						c=y+2
				#		print y, cY, lmaxy[y], lminy[y]
				area = cv2.contourArea(contours[cs])
				perim = cv2.arcLength(contours[cs],True)
				if not roi_dict[r+col[c]]:
				#	roi_dict[r+col[c]].append((area*perim))
					roi_dict[r+col[c]].append((area*perim,cX,cY))
					#roi_dict[r+col[c]].append((area*perim,contours[cs]))
				else:
					if roi_dict[r+col[c]] < area*perim:
						roi_dict[r+col[c]][0] = (area*perim,cX,cY)
		frame_roi.append(roi_dict)

		timeDiff = 1. / frameRate
		elapsed = elapsed + timeDiff

		counts = []
		keys = roi_dict.keys()
		keys.sort()
		for k in keys:
			x = -10000
			y = -10000
			if roi_dict[k]:
				x = roi_dict[k][0][1]
				y = roi_dict[k][0][2]
			counts.append(x)
			counts.append(y)
			cv2.line(storedImage,(x,y),(x,y),(255,255,255),2)
		cv2.imwrite('withlines' + str(i) + ".png", storedImage)
		pixData[i,:] = np.asarray(counts)
		totalFrames += 1

	file = open(videoStream + ".centroid2",'w')
	for x in range(0,285):
		for y in range(0,192):
			file.write(str(int(pixData[x,:][y])) + '\n')

	# Save info (elapsed time and framerate) for later use
	vidInfo = {}
	analysisTime = timeStamp - startTime
	vidInfo['analysisTime'] = float(str(analysisTime.seconds) + '.' + str(analysisTime.microseconds))
	vidInfo['TotalFrames'] = totalFrames
	vidInfo['fps'] = int(totalFrames/vidInfo['analysisTime'])
	vidInfo['pixThreshold']=pixThreshold
	vidInfo['CameraResolution']='%s x %s' % (str(m.shape[1]),str(m.shape[0]))
	vidInfo['NamePrefix'] =  videoStream
	#vidInfo['NamePrefix'] =  videoStream.split('.')[0]

	print ('Analyzed %i frames in %f seconds') % (vidInfo['TotalFrames'],vidInfo['analysisTime'])
	print('FrameRate is about %i fps') % vidInfo['fps']
	print 'Motion threshold is %i pixels' % int(pixThreshold)
	print 'Camera resolution is %s' % vidInfo['CameraResolution']

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
	videoStream = imageTools.getVideoStream(sys.argv)
	vidInfo = cmdLine(pixThreshold,frameRate,videoStream)


