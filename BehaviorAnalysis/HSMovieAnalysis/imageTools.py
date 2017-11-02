import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime, timedelta
import sys
import motionTools
import os
import glob
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import selectROIWidget
import setResolutionWidget


#### CAMERA PROPERTIES
def adjustResolution(cap,cameraType):

    if (cameraType == 1):
        xres=1088
        yres=660

    elif (cameraType == 2):
        xres=1088
        yres=660

    else:
        print 'Using default resolution'

    print 'Adjusting camera resolution to %s x %s' % (str(xres), str(yres))

    cap.set(3,xres)
    cap.set(4,yres)

    return cap

def setCameraResolution():
    dialog = setResolutionWidget.Ui_setResolutionWidget()
    if dialog.exec_():
        videoType=dialog.videoType

    return int(videoType)

#### VIDEO STREAM PROPERTIES

# Framerate
def getFrameRate(frameRate = 285): # <--- change this if necessary
	# assume fps = 30. Change if your video is different than this.
	return frameRate

# Pixel Threshold Adjustment
def getPixThreshold(pixThreshold = 0.03): # <--- change this if necessary
	#pixTheshold: what constitutes a real difference, vs. background noise?
    # expressed as percentage of width of video Frame
	return pixThreshold

def getVideoStream(systemArguments):
	if len(systemArguments) > 1:
		videoStream = systemArguments[1] # saved movie
		print 'reading ' + videoStream
		videoType = 'movie'
	else:
		print('Starting camera')
		videoStream = 0 # camera
		videoType = 'live'

	return videoStream

def getVideoStreamMode(systemArguments):
	videoStream = "test" # saved movie
	print 'reading ' + videoStream
	videoType = 'movie'

	return videoStream


def getVideoType(videoStream):
	if videoStream == 0:
		videoType = 'live'
		displayDiffs = 1
	else:
		videoType = 'movie'
		displayDiffs = 1

	return videoType, displayDiffs

#### General Image functions

def crop_image(image,upperLeft,lowerRight):
    cropped = image[upperLeft[0]:lowerRight[0], upperLeft[1]:lowerRight[1]]
    return cropped

def diffImage(storedFrame,currentFrame,pixThreshold,showIt):

    # find difference between current frame and stored frame
    diff = cv2.absdiff(storedFrame,currentFrame)
    _,diff = cv2.threshold(diff,pixThreshold,255,cv2.THRESH_BINARY)
    if showIt == 1:
        cv2.imshow('Press q to exit',diff) # check difference image
    diff = diff / 255
    return diff

def trackdiffImage(storedFrame,currentFrame,pixThreshold,showIt):
    # find difference between current frame and stored frame
		diff = cv2.absdiff(storedFrame,currentFrame)
		#print diff
		#diff = cv2.adaptiveThreshold(diff,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
		_,diff = cv2.threshold(diff,7,255,cv2.THRESH_BINARY)
		# There are some bubbles that come through with a value of 5, but any higher and the fish don't get captured
		# This actually might depend on the lighting in the movies themselves . . . .
		# Will be hard to make sure it is robust and stays robust
		#np.set_printoptions(threshold=np.nan) # printing entire array
		#print diff
		#if showIt == 1:
		#	cv2.imshow('Press q to exit',diff) # check difference image
		#diff = diff / 255
		return diff


def displayImage(image):
    cv2.namedWindow('Press Any Key To Close', cv2.WINDOW_NORMAL)
    cv2.imshow('Press Any Key To Close',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def Blur(image):

    # convert to grayscale
    # blur; in the nested parenthesis is the gaussian kernel size
    # needs to be positive, and odd. Higher values = more blurry
    return cv2.GaussianBlur(image,(7,7),0) # Ian's original is 7,7

def grayBlur(image):

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur; in the nested parenthesis is the gaussian kernel size
    # needs to be positive, and odd. Higher values = more blurry
    return cv2.GaussianBlur(gray,(7,7),0) # Ian's original is 7,7
    #return cv2.GaussianBlur(gray,(7,7),0) # Ian's original is 7,7

def resize_image(image, scale):

    (h, w) = image.shape[:2]
    newWidth = np.floor(scale * w)

    r = newWidth / w
    dim = (int(newWidth), int(h * r))

    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    return resized

def rotate_buffer(image, angle):
    """
    Rotates an OpenCV 2 / NumPy image about its center by the given angle
    The returned image will be large enough to hold the entire
    new image, with a black background
    modified from http://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
    """

    # Get the image size
    image_size = (image.shape[1], image.shape[0])
    image_center = tuple(np.array(image_size) / 2)

    # Convert the OpenCV 3x2 rotation matrix to 3x3
    rot_mat = np.vstack(
        [cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]]
    )

    rot_mat_notranslate = np.matrix(rot_mat[0:2, 0:2])

    # Shorthand for below calcs
    image_w2 = image_size[0] * 0.5
    image_h2 = image_size[1] * 0.5

    # Obtain the coordinates of the corners of the rotated image
    rotated_coords = [
        (np.array([-image_w2,  image_h2]) * rot_mat_notranslate).A[0],
        (np.array([ image_w2,  image_h2]) * rot_mat_notranslate).A[0],
        (np.array([-image_w2, -image_h2]) * rot_mat_notranslate).A[0],
        (np.array([ image_w2, -image_h2]) * rot_mat_notranslate).A[0]
    ]

    # Find the size of the new image
    x_coords = [pt[0] for pt in rotated_coords]
    x_pos = [x for x in x_coords if x > 0]
    x_neg = [x for x in x_coords if x < 0]

    y_coords = [pt[1] for pt in rotated_coords]
    y_pos = [y for y in y_coords if y > 0]
    y_neg = [y for y in y_coords if y < 0]

    right_bound = max(x_pos)
    left_bound = min(x_neg)
    top_bound = max(y_pos)
    bot_bound = min(y_neg)

    new_w = int(abs(right_bound - left_bound))
    new_h = int(abs(top_bound - bot_bound))

    # We require a translation matrix to keep the image centered
    trans_mat = np.matrix([
        [1, 0, int(new_w * 0.5 - image_w2)],
        [0, 1, int(new_h * 0.5 - image_h2)],
        [0, 0, 1]
    ])

    # Compute the tranform for the combined rotation and translation
    affine_mat = (np.matrix(trans_mat) * np.matrix(rot_mat))[0:2, :]

    # Apply the transform
    result = cv2.warpAffine(
        image,
        affine_mat,
        (new_w, new_h),
        flags=cv2.INTER_LINEAR
    )

    return result

def rotate_image(image,angle):

    # calculate the center of the image
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated


#### ROI Mask Functions

def greenThreshImage(mask):

	# find all of the pixels that are masked (equal to rectangle color above)
	mask[mask != (0,255,0)] = 0

	# convert to thresholded image
	gmask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	_,gmask = cv2.threshold(gmask,12,255,0)

	return gmask

def convertStoredImage(mask):
	vals = np.unique(mask)
	for i in range(len(vals)):
		mask[mask==vals[i]]=i
	mask = mask.astype(int)
	return mask

def convertMaskToWeights(mask):
	vals = np.unique(mask)
	#print "vals: ", vals, len(vals)
	for i in range(len(vals)):
		mask[mask==vals[i]]=i
	mask = mask.astype(int)
	w = mask.ravel() # convert to single row for weights in bincount
	return mask,w

def findAndNumberROIs (gmask):

    # find the ROIs and assign each a different number
    contours, hierarchy = cv2.findContours(gmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # assign pixel values to each ROI evenly across 255 (np.floor(x)) and save mask
    pixVals =  np.floor(np.linspace(10,255, len(contours) + 2))
    # or assign pixel values sequentially
    #pixVals = range(len(contours)+1)

    # draw the contours on the mask
    for h,cnt in enumerate(contours):
        cv2.drawContours(gmask,[cnt],0,pixVals[h+1],-1)

    # return mask, number of contours
    return gmask, len(contours), contours

def getCorners(c):

	# gets the lower left corners of contours, and returns them
	# as a list of tuples

	corners = []
	for i in range(len(c)):
		x = c[i][1][0]
		corners.append(tuple(x))

	return corners

def loadmodeImage(modefilename):
	# Load the setup image from this experiment
	try:
		e = mpimg.imread(modefilename)
	except:
		exit('Cannot open mode file')
	return(e)

def loadModeImage():
	# Load the setup image from this experiment
	try:
		e = mpimg.imread('mode.png')
	except:
		exit('Cannot open mode file')
	return(e)

def loadImageAndMask():
	# Load the setup image from this experiment
	try:
		i = mpimg.imread('image.png')
		m = mpimg.imread('mask.png')
	except:
		exit('Cannot open image and/or mask file')
	return(i,m)

def showROI():

	# Generate a figure showing the ROImask on image

	(img,m) = loadImageAndMask()

	f = plt.figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
	#pic = plt.subplot(1,2,1)
	pic = plt.subplot(1,1,1)

	pic.imshow(img) # show video image
	pic.hold(True)
	map = pic.imshow(m,alpha=0.3) # superimpose ROI mask

	numROI = str(len(np.unique(m)) - 1)
	plt.title('Number of ROI = ' + numROI)
	pic.xaxis.set_ticklabels([])
	pic.yaxis.set_ticklabels([])

	# color Bar
	labs = ['background']
	for a in range(1,len(np.unique(m))):
		labs.append(str(a))

	# labels for color bar; wishlist: reduce if > 16
	cbar = f.colorbar(map,ticks=np.unique(m))
	cbar.ax.get_yaxis().labelpad=20
	cbar.ax.set_yticklabels(labs)
	cbar.ax.invert_yaxis()
	cbar.set_label('ROI #', rotation = 270, size = 16)

	deleteData('roiMask*.png')
	savedRoiMask = 'roiMask' + numROI + '.png'
	plt.savefig(savedRoiMask)
	plt.show()

#function like above that works for GUI - does not display image
def saveROI():
    (img,m) = loadImageAndMask()
    f = plt.figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
    pic = plt.subplot(1,1,1)
    pic.imshow(img)
    pic.hold(True)
    map = pic.imshow(m,alpha=0.3)
    numROI = str(len(np.unique(m)) - 1)
    plt.title('Number of ROI = ' + numROI)
    pic.xaxis.set_ticklabels([])
    pic.yaxis.set_ticklabels([])

    # color Bar
    labs = ['background']
    for a in range(1,len(np.unique(m))):
        labs.append(str(a))

    cbar = f.colorbar(map,ticks=np.unique(m))
    cbar.ax.get_yaxis().labelpad=20
    cbar.ax.set_yticklabels(labs)
    cbar.ax.invert_yaxis()
    cbar.set_label('ROI #', rotation = 270, size = 16)

    deleteData('roiMask*.png')
    savedRoiMask = 'roiMask' + numROI + '.png'
    plt.savefig(savedRoiMask)
    plt.close()

def getNumROI():
	roiMasks = glob.glob('roiMask*')[0]
	return int(roiMasks.split('roiMask')[1].split('.')[0])

def getRowsCols(m):
    innerRects = 0 # 1 if want inner + outer rectangles

    while True:
        numRows = input('Enter number of Rows: ')
        numCols = input('Enter number of Columns: ')

        if innerRects == 0:
            maxNum = 144
        else:
            maxNum = 72

        if numRows*numCols<=maxNum:
            break
        else:
            print("Only 144 maximum ROIs are allowed. Please enter smaller values.")

    return gridROI(m,numRows,numCols,innerRects)

def UIRowsCols(m,innerRects):
    dialog2 = selectROIWidget.Ui_selectROIWidget()
    if dialog2.exec_():
        numRows=int(dialog2.numRows)
        numCols=int(dialog2.numColumns)
        gridROI(m,numRows,numCols,innerRects)

def getCornersOfRectangle(m):

	# find the corners of the rectangle
	#   as [x y] where 0 0 = lower left of image]
	ret,thresh = cv2.threshold(m,1,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	upperLeft = contours[0][1][0] # as [x y] where 0 0 = lower left of image]
	lowerRight = contours[0][3][0]

	return (upperLeft, lowerRight)

def addInnerRectangle(gridMask,roiNumber,currentX,currentY,xWidth,yWidth):
	proportion = 0.5 # 0.5 for exactly the same size
	xBuffer = proportion * (xWidth - (math.sqrt(0.5)*xWidth))
	yBuffer = proportion * (yWidth - (math.sqrt(0.5)*yWidth))
	gridMask[currentY+yBuffer:currentY+yWidth-yBuffer,currentX+xBuffer:currentX+xWidth-xBuffer] = roiNumber
	roiNumber += 1
	return (gridMask, roiNumber)

def gridROI(m,numRows,numCols,innerRect):
	wallSize = 0.1

	vals = np.unique(m)
	if len(vals) > 2:
		sys.exit('Mask has more than one shape!')

	(upperLeft, lowerRight) = getCornersOfRectangle(m)

	xspan = lowerRight[0] - upperLeft[0]
	yspan = upperLeft[1] - lowerRight[1]

	# Find dimensions of ROI's and walls
	xWidth = int(round (xspan / (numCols + (numCols * wallSize) - wallSize))) # algebra!
	yWidth = int(round (yspan / (numRows + (numRows * wallSize) - wallSize)))
	xWallWidth = int(np.floor(wallSize * xWidth))
	yWallWidth = int(np.floor(wallSize * yWidth))

	# these will print coordinates of large rectangle
	#print upperLeft
	#print lowerRight
	#print 'x width = ' + str(xWidth) + '; wallSize = ' + str(xWallWidth)
	#print 'y width = ' + str(yWidth) + '; wallSize = ' + str(yWallWidth)

	# make NEW MASK
	#   starting in upper left, find coordinates of each ROI
	#   and replace in plateMask current ROI number
	#   then move on to the next row and to the same thing

	gridMask = np.zeros(m.shape)
	roiNumber = 1
	xStart = int(upperLeft[0])
	currentX = xStart
	currentY = int(lowerRight[1])

	for r in range(numRows):

		for c in range(numCols):

			#print (roiNumber,currentX,currentY) # prints coordinates of upperLeft corner

			gridMask[currentY:currentY+yWidth,currentX:currentX+xWidth] = roiNumber
			roiNumber += 1

			''' replace region in plateMask with current ROI number
			when indexing, array origin is in upper left
			but image origin is lower left, so it's a bit confusing'''

			# now do an inner rectangle if necessary
			if innerRect == 1:
				(gridMask, roiNumber) = addInnerRectangle(gridMask,roiNumber,currentX,currentY,xWidth,yWidth)

			# done with this column, update x
			currentX = currentX + xWidth + xWallWidth


		# done with columns
		# now ready to start new row, update y and reset X
		currentX = xStart
		currentY = currentY + yWidth + yWallWidth

	# done generating ROIs
	gridMask = gridMask.astype(int)
	cv2.imwrite('mask.png',gridMask)

	return gridMask

def squareInSquare(m):

	bufferSize = 2

	vals = np.unique(m)
	if len(vals) > 2:
		sys.exit('Mask has more than one shape!')

	(upperLeft, lowerRight) = getCornersOfRectangle(m)
	squareMask = np.zeros(m.shape)

	xBig = lowerRight[0] - upperLeft[0]
	yBig = upperLeft[1] - lowerRight[1]

	# want inner rectangle area to be equal to
	# outer area - inner area ... MATH!
	xOffset = 0.5 * (xBig - round(math.sqrt(0.5) * xBig))
	yOffset = 0.5 * (yBig - round(math.sqrt(0.5) * yBig))

	# outer rectangle = ROI 1
	squareMask[lowerRight[1]:upperLeft[1],upperLeft[0]:lowerRight[0]]=1

	# buffer of zeros
	squareMask[lowerRight[1]+xOffset - bufferSize:upperLeft[1]-xOffset + bufferSize ,
		upperLeft[0]+yOffset - bufferSize:lowerRight[0]-yOffset + bufferSize]=0

	# inner rectangle = ROI 2
	squareMask[lowerRight[1]+xOffset + bufferSize:upperLeft[1]-xOffset - bufferSize ,
		upperLeft[0]+yOffset + bufferSize:lowerRight[0]-yOffset - bufferSize]=2

	# done generating ROIs
	squareMask = squareMask.astype(int)
	cv2.imwrite('mask.png',squareMask)

	return squareMask

#### File Management
def deleteData(searchType):
    filenames = glob.glob(searchType)
    for f in filenames:
        os.remove(f)

def removeFiles(fileList):
	for fileName in fileList:
		try:
			os.remove(fileName)
		except OSError:
			pass
