#!/usr/bin/python -tt

"""
SCRIPT INSTRUCTIONS AND COMMENTS (ADD SOMEDAY)
"""
# IMPORT NECESSARY MODULES
import numpy as np
import cv2
from datetime import datetime, timedelta
import sys
import imageTools
from scipy.stats import mode
import glob,os

def calc_mode(deq, nump_arr):
	for j,k in enumerate(nump_arr[:,0]): #so k are the values, j are the indices
		nump_arr[j,:] = mode(np.array([x[j,:] for x in deq]))[0]
	return nump_arr

def imageMode():
	moviedeq = []
	i2=0
	movielist = ["hsmovieTue, Nov 8, 2016_1.avi", "hsmovieTue, Nov 8, 2016_2.avi", "hsmovieTue, Nov 8, 2016_3.avi", "hsmovieTue, Nov 8, 2016_4.avi", "hsmovieTue, Nov 8, 2016_5.avi", "hsmovieTue, Nov 8, 2016_6.avi"]
	for file in movielist:
	#for file in glob.glob(movielist):
	#for file in glob.glob("*avi"):
		#if i2 == 100:
		#	break
		#print "testing: ", videoStream.split('-')[x]
		cap = cv2.VideoCapture(file)
		#cap = cv2.VideoCapture(videoStream.split('-')[x])
		ret,frame = cap.read()
		storedFrame = imageTools.grayBlur(frame)
		totalFrames = 0
		while(cap.isOpened()):
			ret,frame = cap.read()
			if ret == False:
				print 'End of Video'
				break
			currentFrame = imageTools.grayBlur(frame)
			if totalFrames < 30:
				if totalFrames % 3 == 0:
					#print "adding frames: ", totalFrames
					moviedeq.append(currentFrame)
			totalFrames += 1
			storedFrame = currentFrame # comment out if nothing is in first frame
		i2 += 1
	testing = calc_mode(moviedeq, np.zeros([660,1088]))
	#print "saving mode.png"
	cv2.imwrite('mode.png', testing)
	#cv2.imwrite("mode_"+ movielist[0] + "_to_" + movielist[len(movielist)] + ".png", testing)
	cap.release()
	cv2.destroyAllWindows()

imageMode()
