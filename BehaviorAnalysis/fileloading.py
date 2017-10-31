#!/usr/bin/python

import os,sys,glob,re,argparse
import numpy as np
import scipy
import datetime
import time
from datetime import timedelta
from Fish import Fish # fish object
from EventSection import EventSection # event section object


#numberofwells = 96 # type of plate being used, basically number of ROIs

well_conversion = {0:0,1:8,2:16,3:24,4:32,5:40,6:48,7:56,8:64,9:72,10:80,11:88,12:1,13:9,14:17,15:25,16:33,17:41,18:49,19:57,20:65,21:73,22:81,23:89,24:2,25:10,26:18,27:26,28:34,29:42,30:50,31:58,32:66,33:74,34:82,35:90,36:3,37:11,38:19,39:27,40:35,41:43,42:51,43:59,44:67,45:75,46:83,47:91,48:4,49:12,50:20,51:28,52:36,53:44,54:52,55:60,56:68,57:76,58:84,59:92,60:5,61:13,62:21,63:29,64:37,65:45,66:53,67:61,68:69,69:77,70:85,71:93,72:6,73:14,74:22,75:30,76:38,77:46,78:54,79:62,80:70,81:78,82:86,83:94,84:7,85:15,86:23,87:31,88:39,89:47,90:55,91:63,92:71,93:79,94:87,95:95}
well_conversion24 = {0:0,1:4,2:8,3:12,4:16,5:20,6:1,7:5,8:9,9:13,10:17,11:21,12:2,13:6,14:10,15:14,16:18,17:22,18:3,19:7,20:11,21:15,22:19,23:23}

parser = argparse.ArgumentParser(description='loading for fish behavior files')
parser.add_argument('-t', type=str, action="store", dest="tstampfile")
parser.add_argument('-e', type=str, action="store", dest="eventsfile")
parser.add_argument('-c', type=str, action="store", dest="centroidfile")
parser.add_argument('-d', type=str, action="store", dest="dpixfile")
parser.add_argument('-m', type=str, action="store", dest="movieprefix")
parser.add_argument('-g', type=str, action="store", dest="genotypefile")
parser.add_argument('-s', type=str, action="store", dest="sectionsfile")
parser.add_argument('-n', type=str, action="store", dest="numberofwells", default=96)
args = parser.parse_args()
tstampfile = args.tstampfile
eventsfile = args.eventsfile
centroidfile = args.centroidfile
dpixfile = args.dpixfile
movieprefix = args.movieprefix
genotypefile = args.genotypefile
sectionsfile = args.sectionsfile
numberofwells = int(args.numberofwells)

def faststrptime(val):
	#Example
	#6/18/201612:59:34 PM
	splits1 = val.split("/")
	splits2 = splits1[2].split(":")
	return datetime.datetime(
		int(splits1[2][0:4]), # %Y
		int(splits1[0]), # %m
		int(splits1[1]), # %d
		int(splits2[0][4:len(splits2[0])]), # %H
		int(splits2[1]), # %M
		int(splits2[2][0:2]), # %s
	)


def load_movie_motion_pos(hs_pos, thistime, counter):
	# At this point I actually don't care if the data is centered
	# All I want it for is distances
	moviename = movieprefix + str(counter) + ".avi.centroid2"
	cenfile = open(moviename, 'r')
	hscen_data_list = []
	lines = cenfile.readlines()
	for line in lines:
		hscen_data_list.append(int(line))
	hscen_data_array = np.array(hscen_data_list)
	hscen_data_array = hscen_data_array.reshape(hscen_data_array.size / (numberofwells*2), (numberofwells*2))
	hs_pos[thistime] = hscen_data_array


def load_movie_motion(hs_dpix, thistime, counter):
	moviename = movieprefix + str(counter) + ".avi.motion2"
	firstdpix = open(moviename, 'r')
	hsdp_data_list = []
	lines = firstdpix.readlines()
	for line in lines:
		hsdp_data_list.append(int(line))
	hsdp_data_array = np.array(hsdp_data_list)
	hsdp_data_array = hsdp_data_array.reshape(hsdp_data_array.size / numberofwells, numberofwells)
	hs_dpix[thistime] = hsdp_data_array

def load_event_data(startdate):
	# Load in the original events file
	# NOT 100% SURE HOW THE DATE CHANGING WILL WORK ON THE END AND BEGINNING OF THE MONTH, WE WILL SEE
	lastAMorPM0 = None
	lastAMorPMcounter0 = 0
	hs_dpix = {}
	hs_pos = {}
	events = []
	#hs_dpix is a dictionary of numpy array for each high-speed movie event
	s = open(sectionsfile, 'r')
	slines = s.readlines()
	for sline in slines:
		eventsection = EventSection(sline.strip(), startdate)
		events.append(eventsection)
	f = open(eventsfile, 'r')
	lines = f.readlines()
	counter = 1
	#1:06:24\tPM\t0\t2\n'
	for line in lines:
		TAPES = line.split()
		startdate2 = startdate.split("-")[1] + "/" + startdate.split("-")[2] + "/" + startdate.split("-")[0]
		dateplustime = startdate2 + TAPES[0][0:len(TAPES[0])]
		thistime = faststrptime(dateplustime)
		thisAMorPM0 = TAPES[1]
		if lastAMorPM0 != None:
			if thisAMorPM0 != lastAMorPM0:
				if thisAMorPM0 == "AM":
					lastAMorPMcounter0 = lastAMorPMcounter0 + 1
		if thistime.hour == 12:
			if thisAMorPM0 == "AM":
				thistime = thistime + datetime.timedelta(hours = -12)
				#THIS CODE MAY FAIL IF THE PROTOCOL STARTS IN THE MIDNIGHT BLOCK, BUT I CAN'T IMAGINE THAT EVER HAPPENING
		elif thisAMorPM0 == "PM":
			thistime = thistime + datetime.timedelta(hours = 12)
		lastAMorPM0 = thisAMorPM0
		thistime = thistime + datetime.timedelta(days=(lastAMorPMcounter0))
		# END BLOCK FOR AM PM SITUATION

		for e in events:
			if e.starttime <= thistime <= e.endtime:
				if TAPES[2] == "103":
					#print TAPES[2], TAPES[3]
					#print thistime, lasttime
					if thistime.hour == lasttime.hour and thistime.minute == lasttime.minute:
						print "september file: ", thistime, lasttime
						continue
				#if e.name[-9:] == "darkflash":
				#	for et in e.events[TAPES[2]]:
				#		print et
				#		if thistime.hour == et.hour and thistime.minute == et.minute:
				#			print "continue:"
				#			continue
				e.add_event(TAPES[2], TAPES[3], thistime)
		# All high-speed events are currently labeled with ids of 100 or over
		lasttime = thistime
		if int(TAPES[2]) > 99:
		#	print int(TAPES[2]), TAPES[3], "loading high-speed data", counter, thistime
			load_movie_motion(hs_dpix, thistime, counter)
			load_movie_motion_pos(hs_pos, thistime, counter)
			counter = counter + 1
	# all data is added correctly
	#for e in events:
	#	print "e: ", e.name, e.type, e.events
	return (hs_dpix, hs_pos, events)

def convert_to_ms_time(timestamp_data_array, timestamp_data_dict):
	mstimestamp_data_array = []
	mstimestamp_data_array = timestamp_data_array
	startt = timestamp_data_array[0]
	seccounter = 0
	for position in range(0, len(timestamp_data_array) - 1):
		if timestamp_data_array[position] == timestamp_data_array[position + 1]:
			seccounter = seccounter + 1
		else:
			startpos = position - seccounter
			msec = 1000.0 / ((position - startpos) + 1)
			for i in xrange(startpos, position + 1):
				newsec = timestamp_data_array[i] + datetime.timedelta(milliseconds = msec*(i-startpos))
				mstimestamp_data_array[i] = newsec
			seccounter = 0
	return mstimestamp_data_array

def load_timestamp_file():
	# Loading in the timestamp file data and getting rid of the ^M character that is between the times
	timestamp_data_array = []
	dropped_indices = []
	for file in glob.glob(tstampfile):
		f = open(file, 'r')
		lines = f.readlines()
		f.close()
		timestamp_data_array = [] #Currently this analysis only works on a single file, will also input file with options in future as well
		for line in lines:
			timestamp_data_array = re.split('\015',line)
		timestamp_data_array.pop()
	n = 0
	timestamp_data_dict = {}
	lasttime = None

	lastAMorPMcounter0 = 0
	lastAMorPM0 = None
	for t in timestamp_data_array:
		thistime = faststrptime(t)
		thisAMorPM0 = t.split()[len(t.split())-1]
		if lastAMorPM0 != None:
			if thisAMorPM0 != lastAMorPM0:
				if thisAMorPM0 == "AM":
					lastAMorPMcounter0 = lastAMorPMcounter0 + 1
		if thistime.hour == 12:
			if thisAMorPM0 == "AM":
				thistime = thistime + datetime.timedelta(hours = -12)
				#THIS CODE MAY FAIL IF THE PROTOCOL STARTS IN THE MIDNIGHT BLOCK, BUT I CAN'T IMAGINE THAT EVER HAPPENING
		elif thisAMorPM0 == "PM":
			thistime = thistime + datetime.timedelta(hours = 12)
		lastAMorPM0 = thisAMorPM0
		#END BLOCK AMPM SITUATION
		#NEED TO MAKE SURE DATE STAYS CORRECT!!! I THINK IT DOES AND THERE WAS A BUG, BUT IM NOT SURE

		timestamp_data_array[n] = thistime
		timestamp_data_dict[thistime] = n
		if n == 0:
			n = n +1
			lasttime = thistime
			continue
		# This step is important later for the fast slicing of the data
		# Essentially giving a unique number for each second in the timestamp file
		tdelta1 = thistime - lasttime
		testtime = thistime - datetime.timedelta(seconds = tdelta1.total_seconds())
		if thistime != lasttime:
			timestamp_data_dict[thistime] = n
			if tdelta1.total_seconds() > 1:
				for x in range(0,int(tdelta1.total_seconds()-1)):
					print "DROPPED A SECOND: ", thistime, lasttime, testtime, testtime + datetime.timedelta(seconds=1), timestamp_data_array[n], n-1, timestamp_data_array[n-1]
					dropped_indices.append(testtime + datetime.timedelta(seconds=1))
					testtime = testtime + datetime.timedelta(seconds=1)
			lasttime = thistime
		n = n + 1
	mstimestamp_data_array = convert_to_ms_time(timestamp_data_array, timestamp_data_dict)
	return (mstimestamp_data_array, timestamp_data_dict, dropped_indices)

def cart2pol(x, y):
	rho = np.sqrt(x**2 + y**2)
	theta = np.arctan2(y, x)
	return(rho, theta)

#find max and min value for each fish in order to identify well edges
def max_min(cen_data_array):
	maxxys = []
	minxys = []
	for n in range (0, numberofwells*2,2):
		maxtest = np.amax(cen_data_array[:,n])
		mintest = np.amin(cen_data_array[:,n])
		if maxtest == mintest and maxtest == 0:
			maxxys.append(0)
			maxxys.append(0)
			minxys.append(0)
			minxys.append(0)
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

def convert_to_polar(cen_data_array):
	(maxxysnp, minxysnp) = max_min(cen_data_array)
	midcoords = (maxxysnp + minxysnp) / 2
	midcoords = midcoords.astype(np.int16)
	cen_data_array = cen_data_array.astype(np.int16)
	cen_data_array[cen_data_array == 0] = -10000 # just setting to very low value to make it easier to ignore
	# subtract middle coordinate to get everything centered about 0
	zerodcoords = np.zeros(np.shape(cen_data_array))
	for i in range (0, numberofwells*2):
		# CURRENTLY I AM NOT DEALING WITH THIS ISSUE YET OF THE VERY NEGATIVE NUMBERS THAT MEAN IT ISN'T MOVING YET
		zerodcoords[:,i] = cen_data_array[:,i] - midcoords[i]
	zerodcoords[zerodcoords < -5000 ] = 0
	# zerodcoords currently contains negative numbers, which I think mean that the fish hasn't moved yet
	# crap, after subtracting there is negative numbers, so need a case to keep them zero
	thetadata = np.zeros((len(cen_data_array), numberofwells))
	rhodata = np.zeros((len(cen_data_array), numberofwells))
	xzerod = np.zeros((len(cen_data_array), numberofwells))
	yzerod = np.zeros((len(cen_data_array), numberofwells))
	for i in range (0, numberofwells):
		(rhodata[:,i], thetadata[:,i]) = cart2pol(zerodcoords[:,2*i], zerodcoords[:,2*i+1])
		xzerod[:,i] = zerodcoords[:,2*i]
		yzerod[:,i] = zerodcoords[:,2*i+1]
	return (rhodata, thetadata, xzerod, yzerod)

def generate_fish_objects(dp_data_array, rho_array, theta_array, x_array, y_array, hs_dpix, hs_pos, genotypefile):
	for file in glob.glob(genotypefile):
		f = open(file, 'r')
		lines = f.readlines()
		f.close()
		genotype_list = {}
		genotype_dict = {"controlgroup": "wt", "testgroup": "hom"}
		# just doing this so I don't need to go through all the code and change "wt" and "hom"
		for line in lines:
			# The file must use "controlgroup: #,#,#" and "testgroup: #,#,#,#" to emphasize to users that only two are allowed
			dictkey = genotype_dict[line.split(':')[0]]
			fishidslist = line.split(':')[1].strip().split(',')
			inputids = []
			for id in fishidslist:
				inputids.append(int(id)-1)
			genotype_list[dictkey] = inputids
	fish_list = []
	# WT IS REALLY HET
	for n in range(0, numberofwells):
		split_hs_dpix = {}
		split_hs_pos_x = {}
		split_hs_pos_y = {}
		for d in hs_dpix.keys():
			split_hs_dpix[d] = hs_dpix[d][:,n]
			split_hs_pos_x[d] = hs_pos[d][:,2*n]
			split_hs_pos_y[d] = hs_pos[d][:,2*n+1]
		for x in genotype_list.keys():
			if n in genotype_list[x]:
				if numberofwells == 96:
					newfish = Fish(n, x, dp_data_array[:,well_conversion[n]], rho_array[:,well_conversion[n]], theta_array[:,well_conversion[n]], x_array[:,well_conversion[n]], y_array[:,well_conversion[n]], split_hs_dpix, split_hs_pos_x, split_hs_pos_y) # WHAT ABOUT timestamp_data_array and timestamp_data_dict, they are the same for all fish
				elif numberofwells == 24:
					newfish = Fish(n, x, dp_data_array[:,well_conversion24[n]], rho_array[:,well_conversion24[n]], theta_array[:,well_conversion24[n]], x_array[:,well_conversion24[n]], y_array[:,well_conversion24[n]], split_hs_dpix, split_hs_pos_x, split_hs_pos_y) # WHAT ABOUT timestamp_data_array and timestamp_data_dict, they are the same for all fish
				fish_list.append(newfish)
	return fish_list

def loading_procedures():
	tuple_timestuff = load_timestamp_file()
	print "Done loading timestamp file"

	with open(dpixfile, 'rb') as fid:
		dp_data_array = np.fromfile(fid, dtype = '>u2')
	dp_data_array = dp_data_array.reshape(dp_data_array.size / numberofwells, numberofwells)
	print "Done loading dpix"

	with open(centroidfile, 'rb') as fid:
		cen_data_array = np.fromfile(fid, '>u2')
	cen_data_array = cen_data_array.reshape(cen_data_array.size / (numberofwells*2), (numberofwells*2))
	cen_data_array[cen_data_array == 65535] = 0 # just setting to zero to make it easier to ignore
	# This is because they are all values of -16 and the initial type of the array is unsigned int, but it should be clear that it means the fish hasn't moved yet
	# At this point I'm not 100% sure whether or not the -1 means the fish hasn't been captured yet because it hasn't moved or whether it means something else
	# converting them to zero for now so that it makes it easier to deal with the downstream max/min tests
	tuple_rho_theta = convert_to_polar(cen_data_array)
	print "Done converting to polar coordinates"

	startdate = str(tuple_timestuff[0][0].year) + "-" + str(tuple_timestuff[0][0].month) + "-" + str(tuple_timestuff[0][0].day)
	global_tuple_events = load_event_data(startdate)
	print "Done loading events"

	fish_list = generate_fish_objects(dp_data_array, tuple_rho_theta[0], tuple_rho_theta[1], tuple_rho_theta[2], tuple_rho_theta[3], global_tuple_events[0], global_tuple_events[1], genotypefile)
	return (fish_list, tuple_timestuff[0], tuple_timestuff[1], tuple_timestuff[2], global_tuple_events)
