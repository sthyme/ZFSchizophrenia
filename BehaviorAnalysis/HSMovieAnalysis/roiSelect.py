#!/usr/bin/python -tt

"""
This script allows you to select rectangular ROIs on an image,
and shows the resulting ROI mask superimposed on the image

USAGE: python roiSelect.py [opt: videoFile]

If no video file is specified, the image is a frame from live video
If a video file is specified, the image is the first frame of the video

If several ROIs are drawn, they are numbered sequentially from Bottom to Top
(and then Left to Right)

NEED:
1) a saved movie or an attached camera
2) the imageTools.py module of tools
"""

import cv2
import sys
import imageTools

## function for selecting ROIS with mouse
def draw_roi(event,x,y,flags,params):

	global ix,iy,drawing, img

	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		ix,iy = x,y

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			cv2.rectangle(img,(ix,iy),(x,y),(0,255,0,0.5),-1) #GREEN

	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False

def main(videoStream):

	global ix, iy, drawing, img

	# Setup drawing of ROI's
	drawing = False
	ix,iy = -1,-1

	imageName = 'image.png'
	maskName = 'mask.png'

	# remove old images and masks, if present
	imageTools.removeFiles([imageName,maskName])

	cap = cv2.VideoCapture(videoStream)
	# TEST if bigger than screen size and adjust resolution if necessary
	videoType = 0 # comment OFF If adjusting resolution
	#videoType = imageTools.setCameraResolution() # comment ON if adjusting resolution
	if videoType != 0:
		cap = imageTools.adjustResolution(cap,videoType)

	# Grab a frame from the video
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			img = frame
			img[img>250]=250 # remove saturated pixels
			cv2.imwrite(imageName,img)
			break
		else:
			sys.exit("Failure to capture image")
			break

	cap.release()
	cv2.destroyAllWindows()

	## add ROIs onto the image
	roiWindowName = 'Select ROI, press Esc when finished'
	cv2.namedWindow(roiWindowName)
	cv2.setMouseCallback(roiWindowName,draw_roi)

	while(1):
		cv2.imshow(roiWindowName,img)
		k = cv2.waitKey(1) & 0xFF
		if  k == 27:
			# save current image with green rectangles
			cv2.imwrite('rects.png',img)
			mask = img;
			break
	cv2.destroyAllWindows()

	# make a binary image of the ROI mask based on GREEN rectangle
	gmask = imageTools.greenThreshImage(mask)

	# find the shapes (ROIs) in the image, count them
	(gmask, numROI, contours)= imageTools.findAndNumberROIs(gmask)
	cv2.imwrite(maskName,gmask)

	return (gmask,numROI)

def cmdLine(videoStream):
	(gmask,numROI) = main(videoStream)
	if numROI == 1:
		gmask = imageTools.getRowsCols(gmask) # to make GRID
		#gmask = imageTools.squareInSquare(gmask) # to make equal area rectangles
	imageTools.showROI()

if __name__ == '__main__':

	videoStream = imageTools.getVideoStream(sys.argv)
	cmdLine(videoStream)




