#!/usr/bin/python -tt

"""
SCRIPT RUNNING NOTES, WILL ADD SOMEDAY
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

numberofwells = 96
xdim = 1088
ydim = 660

def max_min():
	#with open(centroidfile, 'rb') as fid:
	with open("testlog.centroid1.Tue, Jun 21, 2016", 'rb') as fid:
		cen_data_array = np.fromfile(fid, '>u2')
	cen_data_array = cen_data_array.reshape(cen_data_array.size / (numberofwells*2), (numberofwells*2))
	cen_data_array[cen_data_array == 65535] = 0 # just setting to zero to make it easier to ignore
	maxxys = []
	minxys = []
	for n in range (0, numberofwells*2,2):
		#print "fish: ", n
		maxtest = np.amax(cen_data_array[:,n])
		mintest = np.amin(cen_data_array[:,n])
		# Adds the x and y coordinates to the arrays in an interleaved manner for the next steps, ie, x1 then y1, x2 then y2
		if maxtest == mintest and maxtest == 0:
			maxxys.append(0)
			maxxys.append(0)
			minxys.append(0)
			minxys.append(0)
			#maxxs.append(0)
			#maxys.append(0)
			#minxs.append(0)
			#minys.append(0)
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
			#maxxs.append(maxrealx)
			#maxys.append(maxrealy)
			#minxs.append(minrealx)
			#minys.append(minrealy)
	#print len(maxxs), len(maxys), len(minxs), len(minys)
	#for x in maxxs:
	#maxxys = np.array([maxxs, maxys])
	#minxys = np.array([minxs, minys])
	maxxysnp = np.array(maxxys)
	minxysnp = np.array(minxys)
	#print np.shape(maxxys)
	return( maxxysnp, minxysnp)

def main(pixThreshold,frameRate,videoStream):
	#elate_loc={(1,1):1, (1,2):2, (1,3):3, (1,4):4, (1:5):5, (1,6):6, (1,7):7, (1,8):8, (1,9):9,(1,10):10,(1,11):11,(1,12):12,(2,1):13,(2,2):14,(2,3):15,(2,4):16,(2:5):17,(2,6):18,(2,7):19,(2,8):20,(2,9):21,(2,10):22,(2,11):23,(2,12):24,(3,1):25,(3,2):26,(3,3):27,(3,4):28,(3,5):29,(3,6):30,(3,7)}
	rowold={1:0,2:12,3:24,4:36,5:48,6:60,7:72,8:84}
	row={0:0,1:12,2:24,3:36,4:48,5:60,6:72,7:84}

	expDuration = 600000 # duration of experiment, in seconds; only relevant for live feed
	saveFreq = 4500 # how often to save data, in frames

	i,m = imageTools.loadImageAndMask()
	e = imageTools.loadModeImage()
	roimask = np.zeros((660,1088))
	(maxxysnp, minxysnp) = max_min()
	print "maxxysnp: ", maxxysnp
	print "minxysnp: ", minxysnp
	maxxs = []
	minxs = []
	maxys = []
	minys = []
	for j in range (0, numberofwells*2,2):
		maxx = maxxysnp[j]
		maxxs.append(maxxysnp[j])
		maxy = maxxysnp[j+1]
		maxys.append(maxxysnp[j+1])
		minx = minxysnp[j]
		minxs.append(minxysnp[j])
		miny = minxysnp[j+1]
		minys.append(minxysnp[j+1])
		roimask[miny:maxy,minx:maxx] = j+1
	maxxs.sort()
	maxys.sort()
	minxs.sort()
	minys.sort()
	#smaxxs = []
	#sminxs = []
	#smaxys = []
	#sminys = []
	#rx = 8
	#cy = 12
	#realmaxx = 0
	#realmaxxs = []
	#for z in range(0, len(maxxs)):
	#	if z == cy - 1:
	#		realmaxxs.append(realmaxx)
	#		realmaxx = 0
	#	if maxxs[z] > realmaxx:
	#		realmaxx = maxxs[z]
	np.set_printoptions(threshold=np.nan) # printing entire array
	print roimask
	#	print maxx,maxy,minx,miny
	#print e
	#cv2.imwrite('testinge.jpg', e)
	#cv2.imwrite('testingm.jpg', m)
	#cv2.imwrite('testingi.jpg', i)
	# convert mask to integer values for bincount weights
	#print "mask1: ", np.shape(m), m
	m,w = imageTools.convertMaskToWeights(m)
	rm,roimaskweights = imageTools.convertMaskToWeights(roimask)
	#print "mask2: ", np.shape(m), m
	#print "weights: ", np.shape(w), w
	unique = np.unique(m)
	print "unique: ", unique
	unique2 = np.unique(rm)
	print "unique2: ", unique2
	#print np.shape(m)
	rminr = set()
	rminc = set()
	rmaxr = set()
	rmaxc = set()

	for x in unique2:
		#print "x: ", x
		#if x == 0:
		#	continue
		#print np.shape(np.where(m==x))
		#print np.where(m==x)
		rmaxdimc = np.amax(np.where(rm==x)[0])
		rmaxc.add(rmaxdimc)
		#print "max dimc: ", np.amax(np.where(m==x)[0])
		rmaxdimr = np.amax(np.where(rm==x)[1])
		rmaxr.add(rmaxdimr)
		#print "max dimr: ", np.amax(np.where(m==x)[1])
		rmindimc = np.amin(np.where(rm==x)[0])
		rminc.add(rmindimc)
		#print "min dimc: ", np.amin(np.where(m==x)[0])
		rmindimr = np.amin(np.where(rm==x)[1])
		rminr.add(rmindimr)
		#print "min dimr: ", np.amin(np.where(m==x)[1])
	rlminx = list(rminr)
	rlminx.sort()
	rlmaxx = list(rmaxr)
	rlmaxx.sort()
	rlminy = list(rminc)
	rlminy.sort()
	rlmaxy = list(rmaxc)
	rlmaxy.sort()
	print rlminx, rlmaxx, rlminy, rlmaxy


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
	print "real mask: ", lminx, lmaxx, lminy, lmaxy
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
	# have to convert the float32 to uint8
	storedMode = imageTools.Blur(storedImage)
	storedFrame = imageTools.grayBlur(frame)
	pixThreshold = int(np.floor( pixThreshold * storedFrame.shape[0] ))
	print('PixelThreshold is %i') % pixThreshold
	cenData = np.zeros([ saveFreq, len(np.unique(w))*2 -2])
	pixData = np.zeros([ saveFreq, len(np.unique(w)) + 1])
	i = 0 # a counter for saving chunks of data
	totalFrames = 0
	startTime = datetime.now()
	oldTime = startTime
	elapsed = 0
	print('Analyzing motion data...')
	frame_roi = []
	while(cap.isOpened()):
		#print "frames", totalFrames
		ret,frame = cap.read()
		if ret == False:
			print 'End of Video'
			break
		currentFrame = imageTools.grayBlur(frame)
		currentFrame2 = imageTools.grayBlur(frame)
		diffpix = imageTools.diffImage(storedFrame,currentFrame2,pixThreshold,displayDiffs)
		#print np.shape(diffpix)
		#print diffpix # This is 660x1088
		diff = imageTools.trackdiffImage(storedMode,currentFrame,pixThreshold,displayDiffs)
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
		for r in range(0,numberofwells):
			roi_dict[r+1] = []
		for cs in range(0,len(contours)):
			if cv2.contourArea(contours[cs]) > MIN_THRESH or cv2.arcLength(contours[cs],True) > MIN_THRESH_P:
			#if cv2.contourArea(contours[cs]) > MIN_THRESH and cv2.arcLength(contours[cs],True) > MIN_THRESH_P:
				M = cv2.moments(contours[cs])
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				print i, " cX and cY:", cX, cY
				#print lmaxx
				#print lmaxy
				r=1
				c=1
				for x in range(0,len(lmaxx)):
					if cX > lmaxx[x]:
						r=x+2
						print "Lx,cX,lmaxx[x],lmin[x] ",x, cX, lmaxx[x], lminx[x]
				for y in range(0, len(lmaxy)):
					if cY > lmaxy[y]:
						c=y+2
						print "Ly,cY,maxy[y],lmin[x],r,c ",y, cY, lmaxy[y], lminy[y],r,c
				area = cv2.contourArea(contours[cs])
				perim = cv2.arcLength(contours[cs],True)
				perim = cv2.arcLength(contours[cs],True)
				print "L r + c + row[c]: ", r, c, rowold[c]," final well: ", r + rowold[c]
				if not roi_dict[r+rowold[c]]:
				#	roi_dict[r+row[c]].append((area*perim))
					roi_dict[r+rowold[c]].append((area*perim,cX,cY))
					#roi_dict[r+rowold[c]].append((area*perim,contours[cs]))
				else:
					if roi_dict[r+rowold[c]] < area*perim:
						roi_dict[r+rowold[c]][0] = (area*perim,cX,cY)
				print len(maxxs), maxxs, maxys, minxs, minys
				for x in range(0,len(maxxs)):
					if cX > maxxs[x]:
						r=x+1 # maybe DONT ADD TWO?
						#r=x+2 # maybe DONT ADD TWO?
						print "x,cX,maxx[x],minx[x],r,c: ",x, cX, maxxs[x], minxs[x],r,c
				for y in range(0, len(maxys)):
					if cY > maxys[y]:
						c=y+1
						#c=y+2
						print "y,cY,maxy[y].miny[y],r,c", y, cY, maxys[y], minys[y],r,c
				area = cv2.contourArea(contours[cs])
				perim = cv2.arcLength(contours[cs],True)
				print "r + c + r/8+1 + c/12: ", r, c, r/8+1, c/12, " row[c/12]: ", row[c/12], " final well: ", r/8 + 1 + row[c/12]
				if not roi_dict[r/8+1+row[c/12]]:
				#	roi_dict[r+row[c]].append((area*perim))
					roi_dict[r/8+1+row[c/12]].append((area*perim,cX,cY))
					#roi_dict[r+row[c]].append((area*perim,contours[cs]))
				else:
					if roi_dict[r/8+1+row[c/12]] < area*perim:
						roi_dict[r/8+1+row[c/12]][0] = (area*perim,cX,cY)
		frame_roi.append(roi_dict)

		timeDiff = 1. / frameRate
		elapsed = elapsed + timeDiff
		pixcounts = []
		pixcounts = np.bincount(w, weights=diffpix.ravel())
		pixData[i,:] = np.hstack((elapsed,pixcounts))

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
		if i == 284:
			cv2.imwrite('trackedimagewithlines_' + str(i) + ".png", storedImage)
		cenData[i,:] = np.asarray(counts)
		totalFrames += 1
		storedFrame = currentFrame
		i += 1

	file = open(videoStream + ".centroid2",'w')
	for x in range(0,285):
		for y in range(0,192):
			file.write(str(int(cenData[x,:][y])) + '\n')
	pixData = pixData[:i,:]
	pixData = pixData[:,2:] # get rid of timing column and background column
	file = open(videoStream + ".motion2",'w')
	file.write("12/8/2015" + '\015')
	for x in range(0,285):
		#print "x", x
		for y in range(0,numberofwells):
			file.write(str(int(pixData[x,:][y])) + '\n')
	vidInfo = {}
	# release camera
	cap.release()
	cv2.destroyAllWindows()
	return vidInfo

def cmdLine(pixThreshold,frameRate,videoStream):
	vidInfo = main(pixThreshold,frameRate,videoStream)
	return vidInfo

if __name__ == '__main__':
	pixThreshold = imageTools.getPixThreshold(0.032)
	frameRate = imageTools.getFrameRate() # default is 30
	videoStream = imageTools.getVideoStream(sys.argv)
	vidInfo = cmdLine(pixThreshold,frameRate,videoStream)
