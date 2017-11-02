#!/usr/bin/python -tt

"""
SCRIPT RUNNING NOTES, WILL ADD SOMEDAY
"""

# IMPORT NECESSARY MODULES
import matplotlib.image as mpimg
import numpy as np
import cv2
from datetime import datetime, timedelta
import os,sys,glob,re,argparse
import sys
import imageTools
import motionTools
#from collections import dequeue
from scipy.stats import mode
import math

numberofwells = 96
numberofrows = 8
numberofcols = 12
xdim = 1088
ydim = 660



parser = argparse.ArgumentParser(description='loading for fish behavior files')
parser.add_argument('-c', type=str, action="store", dest="centroidfile")
parser.add_argument('-m', type=str, action="store", dest="moviefile")
args = parser.parse_args()
centroidfile = args.centroidfile
videoStream = args.moviefile

#pixThreshold = imageTools.getPixThreshold(0.032)
pixThreshold = 3
frameRate = imageTools.getFrameRate() # default is 30

#well_conversion = {0:84,1:72,2:60,3:48,4:36,5:24,6:12,7:0,8:85,9:73,10:61,11:49,12:37,13:25,14:13,15:1,16:86,17:74,18:62,19:50,20:38,21:26,22:14,23:2,24:87,25:75,26:63,27:51,28:39,29:27,30:15,31:3,32:88,33:76,34:64,35:52,36:40,37:28,38:16,39:4,40:89,41:77,42:65,43:53,44:41,45:29,46:17,47:5,48:90,49:78,50:66,51:54,52:42,53:30,54:18,55:6,56:91,57:79,58:67,59:55,60:43,61:31,62:19,63:7,64:92,65:80,66:68,67:56,68:44,69:32,70:20,71:8,72:93,73:81,74:69,75:57,76:45,77:33,78:21,79:9,80:94,81:82,82:70,83:58,84:46,85:34,86:22,87:10,88:95,89:83,90:71,91:59,92:47,93:35,94:23,95:11}
well_conversion = {0:0,1:8,2:16,3:24,4:32,5:40,6:48,7:56,8:64,9:72,10:80,11:88,12:1,13:9,14:17,15:25,16:33,17:41,18:49,19:57,20:65,21:73,22:81,23:89,24:2,25:10,26:18,27:26,28:34,29:42,30:50,31:58,32:66,33:74,34:82,35:90,36:3,37:11,38:19,39:27,40:35,41:43,42:51,43:59,44:67,45:75,46:83,47:91,48:4,49:12,50:20,51:28,52:36,53:44,54:52,55:60,56:68,57:76,58:84,59:92,60:5,61:13,62:21,63:29,64:37,65:45,66:53,67:61,68:69,69:77,70:85,71:93,72:6,73:14,74:22,75:30,76:38,77:46,78:54,79:62,80:70,81:78,82:86,83:94,84:7,85:15,86:23,87:31,88:39,89:47,90:55,91:63,92:71,93:79,94:87,95:95}
#well_conversion = {0:0,1:12,2:24,3:36,4:48,5:60,6:72,7:84,8:1,9:13,10:25,11:37,12:49,13:61,14:73,15:85,16:2,17:14,18:26,19:38,20:50,21:62,22:74,23:86,24:3,25:15,26:27,27:39,28:51,29:63,30:75,31:87,32:4,33:16,34:28,35:40,36:52,37:64,38:76,39:88,40:5,41:17,42:29,43:41,44:53,45:65,46:77,47:89,48:6,49:18,50:30,51:42,52:54,53:66,54:78,55:90,56:7,57:19,58:31,59:43,60:55,61:67,62:79,63:91,64:8,65:20,66:32,67:44,68:56,69:68,70:80,71:92,72:9,73:21,74:33,75:45,76:57,77:69,78:81,79:93,80:10,81:22,82:34,83:46,84:58,85:70,86:82,87:94,88:11,89:23,90:35,91:47,92:59,93:71,94:83,95:95}

#def convert_ys(j2):
#	if 0 <= j2 <= 11:
#		num = 0
#	elif 12 <=j2 <= 23:
#		num = 1
#	elif 24 <=j2 <= 35:
#		num = 2
#	elif 36 <=j2 <= 47:
#	elif 48 <=j2 <= 59:
#	elif 60 <=j2 <= 23:

def calc_mode(deq, nump_arr):
	for j,k in enumerate(nump_arr[:,0]): #so k are the values, j are the indices
		nump_arr[j,:] = mode(np.array([x[j,:] for x in deq]))[0]
	return nump_arr

def imageMode(movielist, modename):
	moviedeq = []
	i2=0
	#movielist = ["hsmovieTue, Nov 8, 2016_1.avi", "hsmovieTue, Nov 8, 2016_2.avi", "hsmovieTue, Nov 8, 2016_3.avi", "hsmovieTue, Nov 8, 2016_4.avi", "hsmovieTue, Nov 8, 2016_5.avi", "hsmovieTue, Nov 8, 2016_6.avi"]
	#modename = ''.join(map(str,movielist))
	for filenumber in movielist:
	#for file in glob.glob(movielist):
	#for file in glob.glob("*avi"):
		#if i2 == 100:
		#	break
		#print "testing: ", videoStream.split('-')[x]
		#file = "*_" + str(filenumber) + ".avi"
		#file2 = glob.glob("*_" + str(filenumber) + ".avi")
		#print file2
		cap = cv2.VideoCapture(glob.glob("*_" + str(filenumber) + ".avi")[0])
		#cap = cv2.VideoCapture(file2)
		#cap = cv2.VideoCapture(videoStream.split('-')[x])
		ret,frame = cap.read()
		storedFrame = imageTools.grayBlur(frame)
		totalFrames = 0
		while(cap.isOpened()):
			ret,frame = cap.read()
			if ret == False:
				#print 'End of Video'
				break
			currentFrame = imageTools.grayBlur(frame)
			if totalFrames < 50:
				if totalFrames % 3 == 0:
					#print "adding frames: ", totalFrames
					moviedeq.append(currentFrame)
			totalFrames += 1
			storedFrame = currentFrame # comment out if nothing is in first frame
		i2 += 1
	testing = calc_mode(moviedeq, np.zeros([660,1088]))
	#print "saving mode.png"
	cv2.imwrite("mode_" + modename + ".png", testing)
	#cv2.imwrite("mode_"+ movielist[0] + "_to_" + movielist[len(movielist)] + ".png", testing)
	cap.release()
	cv2.destroyAllWindows()

def max_min():
	with open(centroidfile, 'rb') as fid:
	#with open("testlog.centroid1.Tue, Jun 21, 2016", 'rb') as fid:
		cen_data_array = np.fromfile(fid, '>u2')
	cen_data_array = cen_data_array.reshape(cen_data_array.size / (numberofwells*2), (numberofwells*2))
	cen_data_array[cen_data_array == 65535] = 0 # just setting to zero to make it easier to ignore
	maxxys = []
	minxys = []
	for n in range (0, numberofwells*2,2):
		maxtest = np.amax(cen_data_array[:,n])
		mintest = np.amin(cen_data_array[:,n])
		# Adds the x and y coordinates to the arrays in an interleaved manner for the next steps, ie, x1 then y1, x2 then y2
		if maxtest == mintest and maxtest == 0:
			maxxys.append(-100)
			maxxys.append(-100)
			minxys.append(-100)
			minxys.append(-100)
			# IF WELL IS EMPTY OR NOTHING EVER MOVES NEED A CHECK - ie, if MIN AND MAX ARE EQUAL?
		else:
			maxrealx = maxtest
			minrealx = np.amin(cen_data_array[:,n][np.nonzero(cen_data_array[:,n])])
			maxrealy = np.amax(cen_data_array[:,n+1])
			minrealy = np.amin(cen_data_array[:,n+1][np.nonzero(cen_data_array[:,n+1])])
			maxxys.append(maxrealx)
			maxxys.append(maxrealy)
			minxys.append(minrealx)
			minxys.append(minrealy)
	maxxysnp = np.array(maxxys)
	minxysnp = np.array(minxys)
	return( maxxysnp, minxysnp)

def main(pixThreshold,frameRate,videoStream):
	row={0:0,1:12,2:24,3:36,4:48,5:60,6:72,7:84}
	saveFreq = 4500 # how often to save data, in frames, just making sure this is really big, so I don't have any issues, would be important for memory considerations if I was doing a long movie
	#i,m = imageTools.loadImageAndMask()
	filenumber = videoStream.split('.')[0].split('_')[len(videoStream.split('.')[0].split('_'))-1]
	#print "testing: ", filenumber
#	if 1 <= int(filenumber) <= 20:
#		movielist = list(range(1,21))
#	if 21 <= int(filenumber) <= 40:
#		movielist = list(range(21,41))
#	if 41 <= int(filenumber) <= 60:
#		movielist = list(range(41,61))
#	if 61 <= int(filenumber) <= 70:
#		movielist = list(range(51,71))
#	if 71 <= int(filenumber) <= 80:
#		movielist = list(range(71,91))
#	if 81 <= int(filenumber) <= 478:
#		movielist = list(range(int(filenumber)-10,int(filenumber)+10))
#	if 479 <= filenumber <= 488:
#		movielist = list(range(468,488))
#	if 489 <= int(filenumber) <= 498:
#		movielist = list(range(489,509))
#	if 499 <= int(filenumber) <= 598:
#		movielist = list(range(int(filenumber)-10,int(filenumber)+10))
#	if 599 <= int(filenumber) <= 608:
#		movielist = list(range(599,609))
#	if 609 <= int(filenumber) <= 631:
#		movielist = list(range(609,632))
#	if 632 <= int(filenumber) <= 661:
#		movielist = list(range(632,662))
#	if 662 <= int(filenumber) <= 691:
#		movielist = list(range(662,692))
#	if 692 <= int(filenumber) <= 721:
#		movielist = list(range(692,722))
#	if 722 <= int(filenumber) <= 741:
#		movielist = list(range(722,742))
#	if 742 <= int(filenumber) <= 781:
#		movielist = list(range(742,782))
#	if 782 <= int(filenumber) <= 821:
#		movielist = list(range(782,822))
#	if 822 <= int(filenumber) <= 862:
#		movielist = list(range(822,862))
#	if 862 <= int(filenumber) <= 901:
#		movielist = list(range(862,901))
	if 1 <= int(filenumber) <= 20:
		movielist = list(range(1,21))
	if 21 <= int(filenumber) <= 40:
		movielist = list(range(21,41))
	if 41 <= int(filenumber) <= 60:
		movielist = list(range(41,61))
	if 61 <= int(filenumber) <= 70:
		movielist = list(range(61,71))
#	if 1 <= int(filenumber) <= 70:
#		movielist = list(range(71,111))
	if 71 <= int(filenumber) <= 100:
		movielist = list(range(71,111))
	if 101 <= int(filenumber) <= 448:
		movielist = list(range(int(filenumber)-20,int(filenumber)+20))
	if 449 <= int(filenumber) <= 488:
		movielist = list(range(448,488))
	if 489 <= int(filenumber) <= 528:
		movielist = list(range(489,529))
	if 529 <= int(filenumber) <= 568:
		movielist = list(range(529,569))
		#movielist = list(range(int(filenumber)-20,int(filenumber)+20))
	if 569 <= int(filenumber) <= 608:
		movielist = list(range(569,609))
	if 609 <= int(filenumber) <= 631:
		movielist = list(range(609,632))
	if 632 <= int(filenumber) <= 661:
		movielist = list(range(632,662))
	if 662 <= int(filenumber) <= 691:
		movielist = list(range(662,692))
	if 692 <= int(filenumber) <= 721:
		movielist = list(range(692,722))
	if 722 <= int(filenumber) <= 741:
		movielist = list(range(722,742))
	#if 632 <= int(filenumber) <= 741:
	#	movielist = list(range(609,632))
	if 742 <= int(filenumber) <= 781:
		movielist = list(range(742,782))
	if 782 <= int(filenumber) <= 821:
		movielist = list(range(782,822))
	if 822 <= int(filenumber) <= 862:
		movielist = list(range(822,862))
	if 862 <= int(filenumber) <= 901:
		movielist = list(range(862,901))

	modename = str(movielist[0]) + "to" + str(movielist[len(movielist)-1])
	#modename = ''.join(map(str,movielist))
	imageMode(movielist, modename)
	modefilename = "mode_" + modename + ".png"
	#print movielist
	try:
		mpimg.imread(modefilename)
		#print "mode file already generated"
	except:
		imageMode(movielist, modename)
	e = imageTools.loadmodeImage(modefilename)
	#e = imageTools.loadModeImage()
	roimask = np.zeros((660,1088))
	(maxxysnp, minxysnp) = max_min()
	maxxs = []
	minxs = []
	maxys = []
	minys = []
	for j in range (0, numberofwells*2,2):
		if maxxysnp[j] == -100:
			# if nothing ever moved in this well and there is no max or min value (could happen with a totally empty well)
			maxxs.append(np.nan)
			maxys.append(np.nan)
			minxs.append(np.nan)
			minys.append(np.nan)
		else:
			maxxs.append(maxxysnp[j])
			maxys.append(maxxysnp[j+1])
			minxs.append(minxysnp[j])
			minys.append(minxysnp[j+1])
	npmaxxs = np.asarray(maxxs)
	npmaxys = np.asarray(maxys)
	npminxs = np.asarray(minxs)
	npminys = np.asarray(minys)
	npmaxxs = np.reshape(npmaxxs, (numberofcols,numberofrows))
	npmaxys = np.reshape(npmaxys, (numberofcols,numberofrows)) #12,8
	npminxs = np.reshape(npminxs, (numberofcols,numberofrows))
	npminys = np.reshape(npminys, (numberofcols,numberofrows))
	#print npmaxxs
	#print npmaxys
	#print npminxs
	#print npminys
	cmaxxs = []
	cminxs = []
	cmaxys = []
	cminys = []
	for j2 in range (0, numberofwells):
		maxx = maxxs[well_conversion[j2]]
		maxy = maxys[well_conversion[j2]]
		miny = minys[well_conversion[j2]]
		minx = minxs[well_conversion[j2]]
		#print "j2: ", j2, well_conversion[j2], maxx, maxy, minx, miny
		#print "wcj2/8: ", well_conversion[j2]/8
		#print npmaxxs[well_conversion[j2]/8,:]
		#print npminxs[well_conversion[j2]/8,:]
		#print np.nanmean(npmaxxs[well_conversion[j2]/8,:])
		#print np.nanmean(npminxs[well_conversion[j2]/8,:])
		#print "j2/12: ", j2/12
		#print npmaxys[:,j2/12]
		#print npminys[:,j2/12]
		#print np.nanmean(npmaxys[:,j2/12])
		#print np.nanmean(npminys[:,j2/12])
		if minx == maxx:
			maxx = maxx + 2
		if miny == maxy:
			maxy = maxy + 2
		if math.isnan(float(maxx)): # could also add a condition if min and max are equal to each other
			#print "very first if statement"
			maxx = np.nanmean(npmaxxs[well_conversion[j2]/numberofrows,:])
			minx = np.nanmean(npminxs[well_conversion[j2]/numberofrows,:])
			maxy = np.nanmean(npmaxys[:,j2/numberofcols])
			miny = np.nanmean(npminys[:,j2/numberofcols])
			#print "new means: ", maxx, minx, maxy, miny
			# In the case that the entire row never gets any values in any wells and the mean is still NaN
			# not 100% sure that this is going to work, will get a runtime warning, so then can check it out??
			# mostly not sure about the well_conversions for the Xs
			if math.isnan(float(maxx)) and math.isnan(float(minx)):
		#		print "first if statement"
				if well_conversion[j2] < 8:
					#print "2nd if statement"
					minx = well_conversion[j2]
					maxx = well_conversion[j2]+85
				else:
		#			print "2nd else statement"
					minx = cminxs[well_conversion[j2]-8] + 85
					maxx = cmaxxs[well_conversion[j2]-8] + 85
				###if j2 <= 11:
		#			print "3rd if statement"
				###	miny = j2
				###	maxy = j2+60
				###	minx = j2
			if math.isnan(float(maxy)) and math.isnan(float(miny)):
				#print "4th if statement"
				if j2 < 12:
				#	print "5th if statement"
					miny = j2
					maxy = j2+85
				else:
				#	print "5th else statement"
					miny = cminys[j2-12] + 85
					maxy = cmaxys[j2-12] + 85
		# End of untested section
		cmaxxs.append(maxx)
		cmaxys.append(maxy)
		cminxs.append(minx)
		cminys.append(miny)
		#print miny, maxy, minx, maxx, j2, j2+1
		roimask[miny:maxy,minx:maxx] = j2+1
	np.set_printoptions(threshold=np.nan) # printing entire array
	cmaxxs.sort()
	cmaxys.sort()
	cminxs.sort()
	cminys.sort()
	rm,roimaskweights = imageTools.convertMaskToWeights(roimask)

	# start camera or open video
	videoType, displayDiffs = imageTools.getVideoType(videoStream)
	cap = cv2.VideoCapture(videoStream)

	# adjust video resolution if necessary (sized to mask)
	print 'Camera resolution is %s x %s' % (str(roimask.shape[1]),str(roimask.shape[0]))
	cap.set(3,roimask.shape[1])
	cap.set(4,roimask.shape[0])
	# Set Pixel Threshold
	ret,frame = cap.read()
	storedImage = np.array(e * 255, dtype = np.uint8)
	# have to convert the float32 to uint8
	storedMode = imageTools.Blur(storedImage)
	storedFrame = imageTools.grayBlur(frame)
	#pixThreshold = int(np.floor( pixThreshold * storedFrame.shape[0] ))
	print('PixelThreshold is %i') % pixThreshold
	#cenData = np.zeros([ saveFreq, len(np.unique(roimaskweights))*2])
	cenData = np.zeros([ saveFreq, len(np.unique(roimaskweights))*2 -2])
	#print "cenData shape: ", np.shape(cenData)
	pixData = np.zeros([ saveFreq, len(np.unique(roimaskweights))])
	#pixData = np.zeros([ saveFreq, len(np.unique(roimaskweights))])
	i = 0 # a counter for saving chunks of data
	totalFrames = 0
	startTime = datetime.now()
	print('Analyzing motion data...')
	frame_roi = []
	while(cap.isOpened()):
		ret,frame = cap.read()
		if ret == False:
			print 'End of Video'
			break
		currentFrame = imageTools.grayBlur(frame)
		currentFrame2 = imageTools.grayBlur(frame)
		diffpix = imageTools.diffImage(storedFrame,currentFrame2,pixThreshold,displayDiffs)
		diff = imageTools.trackdiffImage(storedMode,currentFrame,pixThreshold,displayDiffs)
		#cv2.imwrite(videoStream + '_diffimage_' + str(i) + ".png", diff)
		diff.dtype = np.uint8
		_,contours,hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		MIN_THRESH = 20.0
		MIN_THRESH_P = 20.0
		roi_dict = {}
		for r in range(0,numberofwells):
			roi_dict[r+1] = []
		for cs in range(0,len(contours)):
			#print "area and lenght: ", cv2.contourArea(contours[cs]), cv2.arcLength(contours[cs], True)
			if cv2.contourArea(contours[cs]) < 1.0:
				continue
			if cv2.arcLength(contours[cs],True) < 1.0:
				continue
			if cv2.contourArea(contours[cs]) > MIN_THRESH or cv2.arcLength(contours[cs],True) > MIN_THRESH_P:
				M = cv2.moments(contours[cs])
				#print M
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				#print "cX, cY :", cX, cY
				r=1
				c=1
				for x in range(0,len(cmaxxs)):
					#print "cmaxxs: ", cmaxxs[x]
					if cX > cmaxxs[x]:
						r=x+1
						#print "r: ", r
				#print "r: ", r
				for y in range(0, len(cmaxys)):
					#print "cmaxys: ", cmaxys[x]
					if cY > cmaxys[y]:
						c=y+1
					#	print "c: ", c
				if c == numberofwells:
					c = c-1
				if r == numberofwells:
					r = r-1
				area = cv2.contourArea(contours[cs])
				perim = cv2.arcLength(contours[cs],True)
				#print c, numberofcols, c/numberofcols
				if not roi_dict[r/numberofrows+1+row[c/numberofcols]]:
					roi_dict[r/numberofrows+1+row[c/numberofcols]].append((area*perim,cX,cY))
				else:
					if roi_dict[r/numberofrows+1+row[c/numberofcols]] < area*perim:
						roi_dict[r/numberofrows+1+row[c/numberofcols]][0] = (area*perim,cX,cY)
		frame_roi.append(roi_dict)

		pixcounts = []
		pixcounts = np.bincount(roimaskweights, weights=diffpix.ravel())
		pixData[i,:] = np.hstack((pixcounts))
		counts = []
		keys = roi_dict.keys()
		keys.sort()
		for k in keys:
			#print "k: ", k
			x = -10000
			y = -10000
			if roi_dict[k]:
				x = roi_dict[k][0][1]
				y = roi_dict[k][0][2]
			counts.append(x)
			counts.append(y)
			cv2.line(storedImage,(x,y),(x,y),(255,255,255),2)
		if i == 284:
			cv2.imwrite(videoStream + '_trackedimagewithlines_' + str(i) + ".png", storedImage)
		cenData[i,:] = np.asarray(counts)
		totalFrames += 1
		storedFrame = currentFrame
		i += 1

	file = open(videoStream + ".centroid2",'w')
	for x in range(0,285):
		for y in range(0,192):
			file.write(str(int(cenData[x,:][y])) + '\n')
	pixData = pixData[:i,:]
	pixData = pixData[:,1:] # get rid of background column
	file = open(videoStream + ".motion2",'w')
	#file.write("12/8/2015" + '\015')
	for x in range(0,285):
		for y in range(0,numberofwells):
			file.write(str(int(pixData[x,:][y])) + '\n')
#	vidInfo = {}
	# release camera
	cap.release()
	cv2.destroyAllWindows()
#	return vidInfo

#def cmdLine(pixThreshold,frameRate,videoStream):
main(pixThreshold,frameRate,videoStream)
#vidInfo = main(pixThreshold,frameRate,videoStream)
#	return vidInfo

#if __name__ == '__main__':
#	pixThreshold = imageTools.getPixThreshold(0.032)
#	frameRate = imageTools.getFrameRate() # default is 30
#	videoStream = imageTools.getVideoStream(sys.argv)
#	vidInfo = cmdLine(pixThreshold,frameRate,videoStream)
