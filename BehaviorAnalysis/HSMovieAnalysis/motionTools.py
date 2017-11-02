import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
import os
from scipy import stats


def getFrameRate(frameRate=286):
	# change frameRate up there if necessary
	return frameRate

def loadData(path):
    # concatenate all data into a single array
    print('Loading files from %s') % path

    filenames = glob.glob(path + '*.npy')

    if len(filenames) > 0: # checks to see if there are any files
        firstFile = filenames.pop(0)
    else:
        sys.exit('No .npy files to analyze')

    data = np.load(firstFile)

    if len(filenames) > 0:
        for f in filenames:
            d = np.load(f)
            data = np.vstack((data,d))

    # separate timeStamps from delta pix
    timeStamps = data[:,0]

    # ROI data is column 2 of data (column 0 = timeStamp, column 1 = background)
    deltaPix = data[:,1:]

    # frames per second
    fps = np.floor ( len(timeStamps) / (timeStamps[-1] - timeStamps[0]) )

    return (timeStamps, deltaPix, fps)

def motionInROI(timeStamps, deltaPix):

	# Plot with y-axis = time, x-axis = ROI number
	# Frames with activity are shown as a dot
	fps = getFrameRate()

	##print np.shape(deltaPix)
	deltaPix = deltaPix[:,1:] # get rid of background column
	##print np.shape(deltaPix)

	t = np.linspace(1,timeStamps.shape[0],timeStamps.shape[0])
	rows,cols = deltaPix.shape

	for c in np.arange(0,cols,1):

		#toGet =  cols - c - 1 # go in reverse order
		toGet = c

		# find non-zero points in this ROI
		thisCol = deltaPix[:,toGet]
		times = t[thisCol > 0]

		# make a vector containing ROI number
		colPlot = np.ones(times.shape[0])
		colPlot = colPlot * c + 1

		#plot dots
	plt.plot(colPlot,times / fps,'ko', markersize = 2)
	plt.hold(True)

    # show a horizontal line at maze completion
    #t = t / frameRate
    #plt.axhline(y=t[-1], color ='r', linestyle='--', linewidth=2)

    # label this line
    #plt.text(1,t[-1] + 1, 'Time to Complete Maze', fontsize=24)
    #plt.ylim(0, t[-1] + 6)

    ## labeling lights and stuff
    #plt.axhline(y=t[40], color ='r', linestyle='--', linewidth=2)
    #plt.text(1,t[30], 'Lights off', fontsize=18)
    #plt.axhline(y=t[190], color ='b', linestyle='--', linewidth=2)
    #plt.text(1,t[200], 'Lights on', fontsize=18)
    #plt.ylim(0,291)

    # show the plot
	plt.ylabel('Time (seconds)', fontsize=24)
	plt.xlabel('ROI', fontsize=24)

	plt.tick_params(axis='both', which='major', labelsize=18)

	plt.xlim(0.5,cols + 0.5)
	if cols < 16:
		plt.xticks(np.arange(1, cols+1, 1))
	elif cols < 21:
		plt.xticks(np.arange(1, cols+1, 5))
	else:
		plt.xticks(np.arange(1, cols+1, 10))

	f = plt.gcf()
	f.set_facecolor('w')

	plt.show()

def barTimeInROI(deltaPix):

    # bar graph of total time and pixels in each ROI
    deltaPix = deltaPix[:,1:] # get rid of background columns

    frameRate = getFrameRate()

    rows,cols = deltaPix.shape

    pixSums = np.sum(deltaPix, axis=0)
    deltaPix[deltaPix>0]=1 # convert pixels to time moving
    timeSums = np.sum(deltaPix, axis=0) / frameRate

    f, (ax1, ax2) = plt.subplots(2, sharex=True)

    #f = figure(num=None, figsize=(4, 8), dpi=80, facecolor='w', edgecolor='w')

    ax1.bar(np.arange(cols) + 1, pixSums, align='center')
    ax2.bar(np.arange(cols) + 1, timeSums, align='center')

    #ax1.bar(np.arange(cols) + 1, sums[::-1], align='center') # reverse order of ROI
    plt.xlabel('ROI number', fontsize=18)
    plt.xlim(0,cols+1)

    ax1.set_ylabel('Locomotion \n(displaced pixels)', fontsize=18, va='center')
    ax1.yaxis.labelpad = 25
    ax2.set_ylabel('Locomotion  \n(seconds with motion)', fontsize=18, va='center')
    ax2.yaxis.labelpad = 25

    f.set_facecolor('w')
    plt.tick_params(axis='both', which='major', labelsize=18)

    if cols < 21:
        plt.xticks(np.arange(1, cols+1, 1))
    else:
        plt.xticks(np.arange(1, cols+1, 5))
    plt.show()

def binActivity(timeStamps,data,fps,binSize,roiGroups):

    # given binSize in seconds
    #   from this and timeStamps, figure out how many frames in a bin
    #   convert time column in matlab to np.arange(0,end,1.0/15) for 15 fps
    #   save cv2 data as seconds.milliseconds
    framesInBin = binSize * fps

    print ('fps = %i; frames in each bin = %i') % (fps, framesInBin)
    print ('Raw data matrix is %s frames by %s ROI') % (str(data.shape[0]),
    	str(data.shape[1]-1))

    numBins = int(np.floor(data.shape[0] / framesInBin))
    currentRow = 0
    times = np.zeros(numBins)
    binnedPixels = np.zeros((numBins,data.shape[1]))
    binnedTimes = np.zeros(binnedPixels.shape)

    #   slice, and sum time moved (or pixels moved) in bin
    for i in range(numBins):

        chunk = data[currentRow+1:currentRow+framesInBin,:]

    	# add up number of pixels moved in this time period
        binnedPixels[i,:] = np.sum(chunk,axis=0)

        # assign a value of 1 to any frame with motion
        chunk[chunk>0] = 1
        binnedTimes[i,:] = np.sum(chunk,axis=0)

        times[i] = timeStamps[currentRow]
        currentRow = currentRow + framesInBin

    # convert seconds to minutes
    binnedTimes = binnedTimes
    binnedPixels = binnedPixels
    times = times / 60.0

    print('After binning, data matrix is %i bins by %i ROI') % (binnedTimes.shape[0],
    binnedTimes.shape[1]-1)
    binnedTimes = binnedTimes / fps # convert frames to seconds

    activityPlot(times, binnedTimes, roiGroups)
    #activityPlot(times, binnedPixels, roiGroups)

    np.savetxt('binnedTimes.csv',binnedTimes,delimiter=',', fmt = '%i')
    np.savetxt('binnedPixels.csv',binnedPixels,delimiter=',', fmt = '%i')

    return (times,binnedPixels,binnedTimes)

def activityPlot(t, data, roiGroups):

    # from tracker data (binned or not)
    #   calculate average (and error) within ROI group
    #   plot time vs. average activity (+/- error)
    # 	plot boxplots of average activity across total time

    colorvals = colorsToPlot()
    ax1 = plt.subplot(121)

    boxData = []
    boxLabels = []
    boxColors = []

    # line +/- error plots
    for n,g in enumerate(sorted(roiGroups.keys())):
		#print g
		print ('Group %s is %s') % (g, str(roiGroups[g]))
		#print data.shape
		#print colorvals[n]

		# collect data to plot.
		# This is going to be a vector of activity (1 entry per frame or frame bin)
		# averaged over this ROI group

		toPlot = np.mean(data[:,roiGroups[g]] , axis=1)

		plt.plot(t, toPlot, color = colorvals[n], label=g, linewidth=2) # standard plot

		#error bars: stderror = std / sqrt(n)
		s = np.std(data[:,roiGroups[g]] , axis=1)
		se = s / np.sqrt(len(roiGroups[g]))
		#plt.errorbar(times, toPlot, yerr=se, color = colorvals[n] ) # with error bars
		plt.fill_between(t, toPlot-se, toPlot+se, alpha = 0.3,
						 facecolor=colorvals[n], edgecolor=colorvals[n])

		# Also, collect the data for the boxplots
		# in the boxes, I want average activity for this bin over ROIs
		boxData.append(np.mean(data[:,roiGroups[g]], axis = 0))

		#boxLabels.append(g)
		boxColors.append(colorvals[n])

    plt.xlabel('Time (minutes)', fontsize=18)
    plt.legend(loc=0, prop={'size':18}) # 0 is 'best'
    plt.tick_params(axis='both', which='major', labelsize=18)

    # boxplots
    ax2 = plt.subplot(122, sharey=ax1)
    plt.ylabel('Seconds moved per minute', fontsize = 18)
    plt.tick_params(axis='both', which='major', labelsize=18)
    bp = plt.boxplot(boxData, widths=0.5)

    if len(boxData) == 2:
    	(t,p) = stats.ttest_ind(boxData[0],boxData[1])
    	plt.xlabel('p = %1.3f by t-test' % p, fontsize = 18)

    xt = ax2.set_xticklabels(boxLabels)
    plt.setp(xt, fontsize=18)

    # format box colors
    boxColors = boxColors * 2
    for n,box in enumerate(bp['boxes']):
        box.set( color=boxColors[n], linewidth=3)

    for n,med in enumerate(bp['medians']):
        med.set( color=boxColors[n], linewidth=2)

    for n,whisk in enumerate(bp['whiskers']):
        whisk.set( color=(0.1,0.1,0.1), linewidth=2, alpha = 0.5)

    f = plt.gcf()
    f.set_facecolor('w')
    plt.show()

def colorsToPlot():

    colorvals = [ (0,0,0), (0.8,0,0), (0.5,0,0.5), (0,0.5,0), (1,0.6,0.1),
        (0,0.52,0.55), (0.8,0.53,0.25), (0.6,0.6,1), (1,0.3,0.3), (0,0.3,0),
        (0.3,0,0), (0,0,0.3) ]

    return colorvals
