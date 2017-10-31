#!/usr/bin/python

import os,sys,glob,re
import numpy as np
import scipy
import datetime
import time
from datetime import timedelta
from AnalyzedFish import AnalyzedFish # fish object
from scipy.stats import norm
import copy
import math
import matplotlib

import fileloading # prepares all the files
import statsandgraphs # has all the graphs that can be made
import setupfishgraphing # has all the graphs that can be made


approximate_frames_dict = {"0":range(2,30),
												"1":range(6,30), # Strong tap that is not high-speed
												"5":range(6,30), # Weak tap that is not high-speed
												"100a":range(4,25), # Weak tap that precedes the 100b
												"100b":range(98,119), # Strong tap 300 msec after weak tap
												"100c":range(98,119), # Strong tap 300 msec after weak tap that is not limited to those without 100a movement
												"100d":range(98,119), # Entire set for PPI, to see both events, the fullboutdata is the only info here of interest
												"112":range(98,119), # Strong tap at later time
												"101":range(4,25), # Weak tap
												"102":range(4,25), # Strong tap
												"103":range(6,270), # Dark flash
												"104":range(6,270), # Light flash
												"105":range(6,270), # Dark flash that waits 150 msec before a strong tap occurs
												"106":range(102,145), # This is a weak tap that is 300 msec after a 20 msec light flash
												"107":range(8,270), # Is this anything? No.
												"108":range(8,270), # Is this anything? No.
												"109":range(8,270), # Light flash for 20 msec
												"110":range(8,270), # Is this anything? No.
												"111":range(5,270)} # Many short light flashes, wanted to see if induced seizures, but doesn't appear to do much

approximate_end_dict = {"100a":75, # Weak tap that precedes the 100b
												"100b":169, # Strong tap 300 msec after weak tap
												"100c":169, # Strong tap 300 msec after weak tap that is not limited to those without 100a movement
												"100d":169, # Entire set for PPI, to see both events, the fullboutdata is the only info here of interest
												"112":193, # Strong tap at later time
												"101":75, # Weak tap
												"102":75, # Strong tap
												"103":280, # Dark flash
												"104":280, # Light flash
												"105":280, # Dark flash that waits 150 msec before a strong tap occurs
												"106":215, # This is a weak tap that is 300 msec after a 20 msec light flash
												"107":280, # Is this anything? No.
												"108":280, # Is this anything? No.
												"109":280, # Light flash for 20 msec
												"110":280, # Is this anything? No.
												"111":280} # Many short light flashes, wanted to see if induced seizures, but doesn't appear to do much




# formuala is square root of r1^2 + r2^2 - 2r1r2cos(theta1-theta2)
# Don't really need this now that I'm saving the x,y coordinates also, but will just keep anyway
def polar_to_distance(rho1, rho2, theta1, theta2):
	# DONT FORGET TO GET RID OF ANY POSITION WITH RHO > 5000
	# Large values of rho means that the fish has not moved yet
	if rho1 > 5000 or rho2 > 5000:
		dist = 0.0
	elif rho1 != rho2 or theta1 != theta2:
		dist = math.sqrt(rho1**2 + rho2**2 - 2*rho1*rho2*np.cos(theta1 - theta2))
		#dist = np.sqrt(rho1**2 + rho2**2 - 2*rho1*rho2*np.cos(theta1 - theta2))
		# Could try to do calculation without the loop by making two arrays for each item, but I don't know if it will save much time, since we save a lot by skipping all the values where the fish doesn't move
	else:
		dist = 0.0
	return dist

def cart_to_distance(x1, x2, y1, y2):
	if x1 < -4000 or x2 < -5000:
		dist = 0.0
	elif x1 != x2 or y1 != y2:
		dist = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
	else:
		dist = 0.0
	return abs(dist)

def PolyArea(x,y): # x and y are the coordinate lists for bout start to bout end
	pA = 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
	if pA < 300:
		# Get crazy high values sometimes, maybe not a complete polygon shape with all needed points
		return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
	else:
		return np.nan

def calculate_displacement(fish_list, all_fish_bouts):
	fish_displacements = {}
	for fish in fish_list:
		rhos = fish.rho_array
		thetas = fish.theta_array
		displacements = []
		for r in xrange(0, (len(all_fish_bouts[fish.idnumber]))):
			bout_start = all_fish_bouts[fish.idnumber][r][0]
			bout_end = all_fish_bouts[fish.idnumber][r][1]
			disp = polar_to_distance(rhos[bout_start], rhos[bout_end], thetas[bout_start], thetas[bout_end])
			displacements.append(disp)
		fish_displacements[fish.idnumber] = displacements
	return fish_displacements

def calculate_centerfrac(fish_list, all_fish_bouts):
	fish_fracs = {}
	for fish in fish_list:
		rhos = fish.rho_array
		rhomax = np.amax(rhos)
		centerfracs = []
		intercenterfracs = []
		averhofracs = []
		interaverhofracs = []
		halfpt = rhomax * 0.45
		for r in xrange(0, (len(all_fish_bouts[fish.idnumber]))):
			bout_start = all_fish_bouts[fish.idnumber][r][0]
			bout_end = all_fish_bouts[fish.idnumber][r][1]
			cmoments = 0
			intercmoments = 0
			tmoments = 0
			intertmoments = 0
			cfrac = 0.0
			intercfrac = 0.0
			averhofrac = 0.0
			interaverhofrac = 0.0
			totalrho = 0.0
			intertotalrho = 0.0
			for r3 in rhos[bout_start:(bout_end+1)]:
				totalrho = r3 + totalrho
				if r3 < halfpt:
					cmoments = cmoments + 1
				tmoments = tmoments + 1
			cfrac = cmoments / tmoments
			averhofrac = (totalrho / tmoments) / rhomax
			centerfracs.append(cfrac)
			averhofracs.append(averhofrac)
			if r == len(all_fish_bouts[fish.idnumber])-1:
				continue
			interboutend = all_fish_bouts[fish.idnumber][r+1][0]
			interboutstart = all_fish_bouts[fish.idnumber][r][1]
			for r2 in rhos[interboutstart:(interboutend+1)]:
				intertotalrho = r2 + intertotalrho
				if r2 < halfpt:
					intercmoments = intercmoments + 1
				intertmoments = intertmoments + 1
			intercfrac = intercmoments / intertmoments
			interaverhofrac = (intertotalrho / intertmoments) / rhomax
			intercenterfracs.append(intercfrac)
			interaverhofracs.append(interaverhofrac)
		fish_fracs[fish.idnumber] = (centerfracs, averhofracs, intercenterfracs, interaverhofracs)
	return fish_fracs

def hs_calculate_distance(fish_list):
	hs_fish_distances = {}
	for fish in fish_list:
		hs_dist = {}
		for timekey in fish.hs_pos_x:
			xlist = []
			ylist = []
			for x in range(0, len(fish.hs_pos_x[timekey])):
				xlist.append(fish.hs_pos_x[timekey][x])
				ylist.append(fish.hs_pos_y[timekey][x])
			hs_dist[timekey] = np.zeros(np.shape(np.asarray(xlist)), dtype=float)
			hs_dist[timekey][0] = 0.0
			for d in range(0, (len(xlist)-1)):
				if (xlist[d] - xlist[d+1] == 0.0) and (ylist[d] - ylist[d+1] == 0.0):
					hs_dist[timekey][d+1] = 0.0
				else:
					hs_dist[timekey][d+1] = cart_to_distance(xlist[d], xlist[d+1], ylist[d], ylist[d+1])
		hs_fish_distances[fish.idnumber] = hs_dist
	return hs_fish_distances

def calculate_distance(fish_list):
	fish_distances = {}
	# distance unit is in pixels
	for fish in fish_list:
		rhos = fish.rho_array
		thetas = fish.theta_array
		distances = np.zeros(np.shape(rhos), dtype=float)
		# at first the index the distance traveled is 0,0
		distances[0] = 0.0
		for r in range(0, (len(rhos)-1)):
			if (rhos[r] - rhos[r+1] == 0.0) and (thetas[r] - thetas[r+1] == 0.0):
				distances[r+1] = 0.0
			else:
				distances[r+1] = polar_to_distance(rhos[r], rhos[r+1], thetas[r], thetas[r+1])
		fish_distances[fish.idnumber] = distances
	return fish_distances

def findBoutIndices(fish_distances, timestamp_data_array, threshold, frames):
	# Could probably do this in a fancier way with np.where, but it's confusing
	boutstarts = []
	boutends = []
	previousdist = 0.0
	if fish_distances[0] >= threshold: # In case fish is moving right away, although unlikely
		boutstarts.append(d)
	previousdist = fish_distances[0]
	for d in range(1, len(fish_distances)):
		if fish_distances[d] >= threshold and float(previousdist) < threshold:
			boutstarts.append(d)
		elif fish_distances[d] < threshold and float(previousdist) >= threshold:
			boutends.append(d-1)
		previousdist = fish_distances[d]
	if fish_distances[len(fish_distances)-1] >=threshold:
		# if the bout was still happening when we stopped using camera
		boutends.append(len(fish_distances)-1)
	realboutlist = []
	for b in range(0, len(boutstarts)):
		if (boutends[b] - boutstarts[b]) >= frames:
			bouttime = timestamp_data_array[boutends[b]] - timestamp_data_array[boutstarts[b]]
			boutdistance = 0
			for c in range(boutstarts[b], boutends[b]):
				boutdistance = boutdistance + fish_distances[c]
			# IS THERE A NUMPY FUNCTION TO ADD UP ALL THE DATA BETWEEN TWO INDICES? WOULD BE CLEANER THAN LOOP.
			realboutlist.append((boutstarts[b], boutends[b],boutends[b]-boutstarts[b],bouttime.total_seconds(),boutdistance))
	return realboutlist


def identify_event_bout(dpix_movement, approximate_frames, threshold, highspeed, frame_threshold):
	bout_start_fr = 0
	bout_end_fr = 0
	#print dpix_movement[approximate_frames[0]:approximate_frames[len(approximate_frames)-1]]
	if dpix_movement[approximate_frames[0]] > threshold: # In case fish is moving right away
		#print "moving before start"
		return (bout_start_fr, bout_end_fr)
	else:
		for d in xrange(0, len(approximate_frames)):
			if dpix_movement[approximate_frames[d]] >= threshold:
				bout_start_fr = approximate_frames[d]
				break
		if highspeed == True:
			for b in xrange(bout_start_fr, len(dpix_movement) - 4):
				if b == 0:
					break
				if dpix_movement[b] < threshold and dpix_movement[b+1] < threshold and dpix_movement[b+2] < threshold:
					bout_end_fr = b - 1
					break
				bout_end_fr = b - 1 # NEED THIS IN CASE THE BOUT STARTS AND THEN WE DONT HAVE ENOUGH FRAMES TO FINISH IT, SO YOU DONT END UP WITH END BEING BEFORE START
			if bout_end_fr - bout_start_fr>frame_threshold:
			#	print "start and end: ", bout_start_fr, bout_end_fr
				return (bout_start_fr, bout_end_fr)
			else:
				return (0, 0)
		else:
			for b2 in xrange(bout_start_fr, approximate_frames[-1] + len(approximate_frames)):
			#	print "b2: ", b2
				if b2 == 0:
					break
				if dpix_movement[b2] < threshold:
					bout_end_fr = b2 - 1
					break
				bout_end_fr = b2 - 1 # NEED THIS IN CASE THE BOUT STARTS AND THEN WE DONT HAVE ENOUGH FRAMES TO FINISH IT, SO YOU DONT END UP WITH END BEING BEFORE START
			#bout_start_fr = bout_start_fr - 1 # Need this to help keep distance bouts that are only a single frame, no longer need it though if basing all on dpix
			#print "start and end: ", bout_start_fr, bout_end_fr
			return (bout_start_fr, bout_end_fr)


def identify_ppievent_bout(dpix_movement, approximate_frames, threshold, highspeed, frame_threshold):
	bout_start_fr = 0
	bout_end_fr = 0
	#print dpix_movement[approximate_frames[0]:approximate_frames[len(approximate_frames)-1]]
	if dpix_movement[approximate_frames[0]] > threshold: # In case fish is moving right away
		#print "moving before start"
		return (bout_start_fr, bout_end_fr)
	else:
		(dpix_bout_start100a, dpix_bout_end100a) = identify_event_bout(dpix_movement, approximate_frames_dict["100a"], threshold, True, frame_threshold)
		if dpix_bout_start100a != 0 or dpix_bout_end100a != 0:
			return (np.nan, np.nan)
		for d in xrange(0, len(approximate_frames)):
			if dpix_movement[approximate_frames[d]] >= threshold:
				bout_start_fr = approximate_frames[d]
				break
		for b in xrange(bout_start_fr, len(dpix_movement) - 4):
			if b == 0:
				break
			if dpix_movement[b] < threshold and dpix_movement[b+1] < threshold and dpix_movement[b+2] < threshold:
				bout_end_fr = b - 1
				break
			bout_end_fr = b - 1 # NEED THIS IN CASE THE BOUT STARTS AND THEN WE DONT HAVE ENOUGH FRAMES TO FINISH IT, SO YOU DONT END UP WITH END BEING BEFORE START
		if bout_end_fr - bout_start_fr>frame_threshold:
			#	print "start and end: ", bout_start_fr, bout_end_fr
			return (bout_start_fr, bout_end_fr)
		else:
			return (0, 0)
		return (bout_start_fr, bout_end_fr)

def event_bout_freq(hs_dict, hs_distances, events, fish_movement, fish_movement_dpix, timestamp_data_dict, timestamp_data_array, threshold, frame_threshold, dpix_threshold, dpix_frame_threshold, hs_pos_x, hs_pos_y, x_array, y_array):
	bout_data = {} # key is the type of event, then each will contain lists of freq, dist, and latency
	for ek in events.keys():
		# ek is basically like 100a or 102 in the ppi section
		#print "ek: ", ek
		if len(ek.split("_")) > 1:
			approximate_frames = approximate_frames_dict[ek.split("_")[0]]
		else:
			approximate_frames = approximate_frames_dict[ek]
		bout_freq_list = []
		bout_disp_list = []
		bout_lat_list = []
		#new_bout_disp = []
		new_bout_tdist = []
		new_bout_vel = []
		new_bout_speed = []
		new_bout_dispoverdist = []
		new_bout_time = []
		poly_areas = []
		poly_areas_div_dist = []
		peak_speed_list = []
		peak_dpix_list = []
		full_bout_data = [] # only necessary for fast events
		slow_full_bout_data = [] # only necessary for fast events
		dpix_full_bout_data = [] # only necessary for fast events
		slow_dpix_full_bout_data = [] # only necessary for fast events
		dpix_bout_freq_list = []
		dpix_bout_lat_list = []
		dpix_bout_cumdpix = []
		dpix_bout_time_list = []
		distbouts_dpix_over_dist = [] # making the assumption in this code that if there is a distance bout there will be a dpix bout
		for et in events[ek]:
			#print "et: ", et
			# et is effectively the timekey used in hs_distances
			if ek != "1" and ek != "0" and ek != "5":
		#		print "et: ", et
				startframe = approximate_frames[0]
				if len(ek.split("_")) > 1:
					endframe = approximate_end_dict[ek.split("_")[0]]
				else:
					endframe = approximate_end_dict[ek]
				if et in hs_distances.keys():
					if ek == "100b":
						(dpix_bout_start, dpix_bout_end) = identify_ppievent_bout(hs_dict[et], approximate_frames, dpix_threshold, True, dpix_frame_threshold)
					else:
						(dpix_bout_start, dpix_bout_end) = identify_event_bout(hs_dict[et], approximate_frames, dpix_threshold, True, dpix_frame_threshold)
					#dpix_bout_lat = (dpix_bout_start-startframe) * 3.5
					#bout_lat = (dpix_bout_start-startframe) * 3.5
					#bout_time = (dpix_bout_end - dpix_bout_start)*3.5
					#dpix_bout_time = (dpix_bout_end - dpix_bout_start)*3.5
					#bout_tdist = 0
					#if not np.isnan(dpix_bout_end):
			#		dpix_bout_lat = (dpix_bout_start-startframe) * 3.5
			#		bout_lat = (dpix_bout_start-startframe) * 3.5
			#		bout_time = (dpix_bout_end - dpix_bout_start)*3.5
			#		dpix_bout_time = (dpix_bout_end - dpix_bout_start)*3.5
			#		bout_tdist = 0
			#		peak_speed = 0
			#		dpix_bout_start = int(dpix_bout_start)
			#		dpix_bout_end = int(dpix_bout_end)
			#		for c0 in range(dpix_bout_start, dpix_bout_end):
			#			bout_tdist = bout_tdist + hs_distances[et][c0]
			#			if hs_distances[et][c0] > peak_speed:
			#				peak_speed = hs_distances[et][c0]
			#		peak_speed = peak_speed / 3.5
			#		bout_cumdpix = 0
			#		peak_dpix = 0
			#		for c1 in range(dpix_bout_start, dpix_bout_end):
			#			bout_cumdpix = bout_cumdpix + hs_dict[et][c1]
			#			if hs_dict[et][c1] > peak_dpix:
			#				peak_dpix = hs_dict[et][c1]
			#		realbout_disp = cart_to_distance(hs_pos_x[et][dpix_bout_start], hs_pos_x[et][dpix_bout_end], hs_pos_y[et][dpix_bout_start], hs_pos_y[et][dpix_bout_end])
			#		polyarea = PolyArea(hs_pos_x[et][dpix_bout_start:dpix_bout_end], hs_pos_y[et][dpix_bout_start:dpix_bout_end])
			#		if bout_tdist > 0:
			#			polyarea_div_dist = polyarea / bout_tdist
			#		else:
			#			polyarea_div_dist = polyarea
			#		if realbout_disp != 0:
			#			bout_dispoverdist = bout_tdist / realbout_disp
			#		else:
			#			bout_dispoverdist = 0
		#			if bout_time != 0:
		#				bout_vel = realbout_disp / bout_time
		#				bout_speed = bout_tdist / bout_time
		#			else:
		#				bout_vel = 0
		#				bout_speed = 0
			#		if dpix_bout_start == np.nan and dpix_bout_end == np.nan:
			#			bout_freq_list.append(np.nan)
			#			bout_disp_list.append(np.nan) # should prob append nan, not 0s
			#			bout_lat_list.append(np.nan) # same here about the zeros
			#			if ek != "100d":
			#				full_bout_data.append(np.full((endframe-startframe), np.nan))
			#			else:
			#				full_bout_data.append(np.full((endframe-(startframe-98)), np.nan))
			#			new_bout_tdist.append(np.nan)
			#			new_bout_vel.append(np.nan)
			#			new_bout_speed.append(np.nan)
			#			new_bout_dispoverdist.append(np.nan)
			#			new_bout_time.append(np.nan)
			#			poly_areas.append(np.nan)
			#			poly_areas_div_dist.append(np.nan)
			#			distbouts_dpix_over_dist.append(np.nan)
					if (dpix_bout_start == 0 and dpix_bout_end == 0) or (np.isnan(dpix_bout_end) or np.isnan(dpix_bout_start)):
					#if not np.isnan(dpix_bout_end):
					#elif dpix_bout_start == 0 and dpix_bout_end == 0:
						bout_freq_list.append(0)
						bout_disp_list.append(np.nan) # should prob append nan, not 0s
						bout_lat_list.append(np.nan) # same here about the zeros
						if ek != "100d":
							full_bout_data.append(np.full((endframe-startframe), np.nan))
						else:
							full_bout_data.append(np.full((endframe-(startframe-98)), np.nan))
						new_bout_tdist.append(np.nan)
						new_bout_vel.append(np.nan)
						new_bout_speed.append(np.nan)
						new_bout_dispoverdist.append(np.nan)
						new_bout_time.append(np.nan)
						poly_areas.append(np.nan)
						poly_areas_div_dist.append(np.nan)
						distbouts_dpix_over_dist.append(np.nan)
						peak_speed_list.append(np.nan)
						peak_dpix_list.append(np.nan)
						dpix_bout_freq_list.append(0)
						dpix_bout_cumdpix.append(np.nan)
						dpix_bout_lat_list.append(np.nan)
						dpix_bout_time_list.append(np.nan)
						if ek != "100d":
							dpix_full_bout_data.append(np.full((endframe-startframe), np.nan))
						else:
							dpix_full_bout_data.append(np.full((endframe-(startframe-98)), np.nan))
					else:
						dpix_bout_lat = (dpix_bout_start-startframe) * 3.5
						bout_lat = (dpix_bout_start-startframe) * 3.5
						bout_time = (dpix_bout_end - dpix_bout_start)*3.5
						dpix_bout_time = (dpix_bout_end - dpix_bout_start)*3.5
						bout_tdist = 0
						peak_speed = 0
						dpix_bout_start = int(dpix_bout_start)
						dpix_bout_end = int(dpix_bout_end)
						for c0 in range(dpix_bout_start, dpix_bout_end):
							bout_tdist = bout_tdist + hs_distances[et][c0]
							if hs_distances[et][c0] > peak_speed:
								peak_speed = float(hs_distances[et][c0])
						peak_speed = peak_speed / 3.5
						bout_cumdpix = 0
						peak_dpix = 0
						for c1 in range(dpix_bout_start, dpix_bout_end):
							bout_cumdpix = bout_cumdpix + hs_dict[et][c1]
							if hs_dict[et][c1] > peak_dpix:
								peak_dpix = float(hs_dict[et][c1])
						realbout_disp = cart_to_distance(hs_pos_x[et][dpix_bout_start], hs_pos_x[et][dpix_bout_end], hs_pos_y[et][dpix_bout_start], hs_pos_y[et][dpix_bout_end])
						polyarea = PolyArea(hs_pos_x[et][dpix_bout_start:dpix_bout_end], hs_pos_y[et][dpix_bout_start:dpix_bout_end])
						if bout_tdist > 0:
							polyarea_div_dist = polyarea / bout_tdist
						else:
							polyarea_div_dist = polyarea
						if realbout_disp != 0:
							bout_dispoverdist = bout_tdist / realbout_disp
						else:
							bout_dispoverdist = 0
						if bout_time != 0:
							bout_vel = realbout_disp / bout_time
							bout_speed = bout_tdist / bout_time
						else:
							bout_vel = 0
							bout_speed = 0
						bout_freq_list.append(1)
						# probably don't need the bout_disp, could just use new_bout_disp for everything, even if not a high-speed movement
						# in the high-speed case they are duplicated
						bout_disp_list.append(realbout_disp) # SHOULD PROB APPEND NAN, NOT 0S
						bout_lat_list.append(bout_lat) # SAME HERE ABOUT THE ZEROS
						new_bout_tdist.append(bout_tdist)
						new_bout_vel.append(bout_vel)
						new_bout_speed.append(bout_speed)
						new_bout_dispoverdist.append(bout_dispoverdist)
						new_bout_time.append(bout_time)
						poly_areas.append(polyarea)
						poly_areas_div_dist.append(polyarea_div_dist)
						if ek != "100d":
							full_bout_data.append(hs_distances[et][startframe:endframe]) # NNEED TO MOVE BOTH OF THESE TO AFTER DETERMINATION OF BOUT OR NO BOUT
						else:
							full_bout_data.append(hs_distances[et][(startframe-98):endframe]) # NNEED TO MOVE BOTH OF THESE TO AFTER DETERMINATION OF BOUT OR NO BOUT
						if bout_cumdpix > 0:
							distbouts_dpix_over_dist.append( bout_tdist / bout_cumdpix)
						else:
							distbouts_dpix_over_dist.append(0)
						peak_speed_list.append(peak_speed)
						peak_dpix_list.append(peak_dpix)
						dpix_bout_freq_list.append(1)
						dpix_bout_cumdpix.append(bout_cumdpix)
						dpix_bout_lat_list.append(dpix_bout_lat)
						dpix_bout_time_list.append(dpix_bout_time)
						if ek != "100d":
							dpix_full_bout_data.append(hs_dict[et][startframe:endframe])
						else:
							dpix_full_bout_data.append(hs_dict[et][(startframe-98):endframe])
				#	if dpix_bout_start == np.nan and dpix_bout_end == np.nan:
			#			dpix_bout_freq_list.append(np.nan)
		#				dpix_bout_cumdpix.append(np.nan)
		#				dpix_bout_lat_list.append(np.nan)
		#				dpix_bout_time_list.append(np.nan)
		#				if ek != "100d":
		#					dpix_full_bout_data.append(np.full((endframe-startframe), np.nan))
		#				else:
		#					dpix_full_bout_data.append(np.full((endframe-(startframe-98)), np.nan))
		#			elif dpix_bout_start == 0 and dpix_bout_end == 0:
		#				dpix_bout_freq_list.append(0)
		#				dpix_bout_cumdpix.append(np.nan)
		#				dpix_bout_lat_list.append(np.nan)
		#				dpix_bout_time_list.append(np.nan)
		#				if ek != "100d":
		#					dpix_full_bout_data.append(np.full((endframe-startframe), np.nan))
		#				else:
		#					dpix_full_bout_data.append(np.full((endframe-(startframe-98)), np.nan))
		#			else:
			#			dpix_bout_freq_list.append(1)
			#			dpix_bout_cumdpix.append(bout_cumdpix)
			#			dpix_bout_lat_list.append(dpix_bout_lat)
			#			dpix_bout_time_list.append(dpix_bout_time)
			#			if ek != "100d":
			#				dpix_full_bout_data.append(hs_dict[et][startframe:endframe])
			#			else:
			#				dpix_full_bout_data.append(hs_dict[et][(startframe-98):endframe])
				# currently hardcoding these slow speed events, previously was an else statement, but that meant that a time that is both fast and slow would only get the fast data
			else:
				if ek == "1" or ek == "5" or ek == "0":
					dpix_frame_threshold = 1
				# Not a high-speed movement
				# it doesn't make sense to get distance, velocity, speed, or time for a non-highspeed movement because they occur so quickly, but displacement does make sense
				# for the distance version at latest, for dpix you would just want the dpix value probably
				# latency doesn't really make sense either
				# The data we are not getting as of may 2017 is the velocity, speed, and dispoverdist, for the slow-speed movements
				# The distance and cumdpix and time and latency  also don't really make sense, but just getting it anyway
				# Need this try/except statement because of lost frames in the slow-speed data
				try:
					approximate_frames_slow = [x+timestamp_data_dict[et] for x in approximate_frames]
				except:
					print "the following frame is not available for this slow-speed event, just skipping event at the following time: ", et
					continue
				slowstartframe = approximate_frames_slow[0]
				slowendframe = approximate_frames_slow[-1]
				(dpix_bout_start, dpix_bout_end) = identify_event_bout(fish_movement_dpix, approximate_frames_slow, dpix_threshold, False, dpix_frame_threshold)
				bout_disp = cart_to_distance(x_array[dpix_bout_start], x_array[dpix_bout_end], y_array[dpix_bout_start], y_array[dpix_bout_end])
				bout_lat = (timestamp_data_array[dpix_bout_start] - timestamp_data_array[timestamp_data_dict[et]]).total_seconds() * 1000 # THIS LATENCY IS IN FRAMES . . . . LEAVE IT FOR NOW, BUT PERHAPS WILL CHANGE TO MSEC LATER - probably just leave as frames?
				bout_time = (timestamp_data_array[dpix_bout_end] - timestamp_data_array[dpix_bout_start]).total_seconds() * 1000 # THIS LATENCY IS IN FRAMES . . . . LEAVE IT FOR NOW, BUT PERHAPS WILL CHANGE TO MSEC LATER - probably just leave as frames?
				dpix_bout_time = (timestamp_data_array[dpix_bout_end] - timestamp_data_array[dpix_bout_start]).total_seconds() * 1000 # THIS LATENCY IS IN FRAMES . . . . LEAVE IT FOR NOW, BUT PERHAPS WILL CHANGE TO MSEC LATER - probably just leave as frames?
				dpix_bout_lat = (timestamp_data_array[dpix_bout_start] - timestamp_data_array[timestamp_data_dict[et]]).total_seconds() * 1000 # THIS LATENCY IS IN FRAMES . . . . LEAVE IT FOR NOW, BUT PERHAPS WILL CHANGE TO MSEC LATER - probably just leave as frames?
				bout_cumdpix = 0
				for c2 in range(dpix_bout_start, dpix_bout_end):
					bout_cumdpix = bout_cumdpix + fish_movement_dpix[c2]
				bout_tdist = 0
				for c3 in range(dpix_bout_start, dpix_bout_end):
				#for c3 in range(bout_start, bout_end):
					bout_tdist = bout_tdist + fish_movement[c3]
				if dpix_bout_start == 0 or dpix_bout_end == 0:
				#if bout_start == 0 or bout_end == 0:
					bout_freq_list.append(int(0))
					bout_disp_list.append(np.nan) # SAME HERE ABOUT THE ZEROS
					bout_lat_list.append(np.nan) # SAME HERE ABOUT THE ZEROS
					new_bout_time.append(np.nan) # SAME HERE ABOUT THE ZEROS
					new_bout_tdist.append(np.nan)
					distbouts_dpix_over_dist.append(np.nan)
					slow_full_bout_data.append(np.full((slowendframe-slowstartframe), np.nan))
				else:
					bout_freq_list.append(1)
					bout_disp_list.append(bout_disp) # SAME HERE ABOUT THE ZEROS
					bout_lat_list.append(bout_lat) # SAME HERE ABOUT THE ZEROS
					new_bout_time.append(bout_time) # SAME HERE ABOUT THE ZEROS
					new_bout_tdist.append(bout_tdist)
					if bout_cumdpix > 0:
						distbouts_dpix_over_dist.append( bout_tdist / bout_cumdpix)
					else:
						distbouts_dpix_over_dist.append(0)
					slow_full_bout_data.append(fish_movement[slowstartframe:slowendframe])
				if dpix_bout_start == 0 or dpix_bout_end == 0:
					dpix_bout_freq_list.append(0)
					dpix_bout_cumdpix.append(np.nan) # SAME HERE ABOUT THE ZEROS
					dpix_bout_lat_list.append(np.nan) # SAME HERE ABOUT THE ZEROS
					dpix_bout_time_list.append(np.nan) # SAME HERE ABOUT THE ZEROS
					slow_dpix_full_bout_data.append(np.full((slowendframe-slowstartframe), np.nan))
				else:
					dpix_bout_freq_list.append(1)
					dpix_bout_lat_list.append(dpix_bout_lat) # SAME HERE ABOUT THE ZEROS
					dpix_bout_cumdpix.append(bout_cumdpix)
					dpix_bout_time_list.append(bout_time) # SAME HERE ABOUT THE ZEROS
					slow_dpix_full_bout_data.append(fish_movement_dpix[slowstartframe:slowendframe])
		#print "dpix data"
		#print dpix_full_bout_data
		#print "notdpix data"
		#print "full bout data testing"
		#print np.shape(full_bout_data)
		#print full_bout_data
		#print "mean"
		#test = np.nanmean(full_bout_data, axis=0)
		#print test
		#print "done test"
		#bout_data[ek] = (bout_freq_list, bout_disp_list, bout_lat_list, new_bout_time, new_bout_tdist, new_bout_vel, new_bout_speed, poly_areas, dpix_bout_freq_list, dpix_bout_lat_list, dpix_bout_cumdpix, dpix_bout_time_list, distbouts_dpix_over_dist, full_bout_data, dpix_full_bout_data, slow_full_bout_data, slow_dpix_full_bout_data)
		#if ek == "1":
		#	print "bout_freq length: ", et, len(bout_freq_list)
		#	print bout_freq_list
		#print "freqs: ", ek, bout_freq_list
		#print "dpixfreqs: ", ek, dpix_bout_freq_list
		bout_data[ek] = (bout_freq_list, bout_disp_list, bout_lat_list, new_bout_time, new_bout_tdist, new_bout_vel, new_bout_speed, poly_areas, dpix_bout_freq_list, dpix_bout_lat_list, dpix_bout_cumdpix, dpix_bout_time_list, distbouts_dpix_over_dist, np.nanmean(full_bout_data, axis=0), np.nanmean(dpix_full_bout_data, axis=0), np.nanmean(slow_full_bout_data, axis=0), np.nanmean(slow_dpix_full_bout_data, axis=0), poly_areas_div_dist, peak_dpix_list, peak_speed_list)
	return bout_data

def determine_indices(timestamp_data_array, timeintervaldenom, timestart, timeend, timeintervalnum, timestamp_data_dict, dropped_indices):
	indexstart = 0
	indexend = 0
	tdelta = timeend - timestart
	intervalnumber = int(tdelta.total_seconds()) / timeintervaldenom # How many different chunks of time to break it into (ie, 10 minutes in active minutes per 10 minutes)
	intervalnumnumber = int(tdelta.total_seconds()) / timeintervalnum # How many different chunks of time to break it into for the numerator (ie, minutes if we want active minutes per 10 minutes)
	indexstart = timestamp_data_dict[timestart] # The index value for the first occurrence of the start time, so this is the inclusive value
	indexend = timestamp_data_dict[timeend] # The index value for the first occurrence of the start time, so this is the inclusive value
	intervalindices = []
	intervalnumindices = []
	intervalindices.append(indexstart)
	intervalnumindices.append(indexstart)
	timetest = timestart
	timestamp_data_dict_keys = timestamp_data_dict.keys()
	for z in xrange(0,intervalnumber):
		z = z+1
		timetest1 = timetest + datetime.timedelta(seconds=(timeintervaldenom * z)) #This is the same as the start time
		if timetest1 not in dropped_indices:
			indext = timestamp_data_dict[timetest1]
			intervalindices.append(indext-1) #The very last index of the end of the chunk
			intervalindices.append(indext) #The very first index of the next start of the chunk
	if timeintervalnum >= 1:
		for z2 in xrange(0,int(intervalnumnumber)):
			z2 = z2+1
			timetest1 = timetest + datetime.timedelta(seconds=(timeintervalnum * z2))
			if timetest1 not in dropped_indices:
				indext = timestamp_data_dict[timetest1]
				intervalnumindices.append(indext-1)
				intervalnumindices.append(indext)
	else: # If we are going to be doing every frame instead of by a set time, can't go less than second intervals using the time approach
		for indext in xrange(indexstart+1,indexend): # Need to add the one because I already put the first index in earlier
			intervalnumindices.append(indext)
	intervalnumindices = np.array(intervalnumindices, dtype=int)
	intervalindices = np.array(intervalindices, dtype=int) # searchsorted efficiency depends on having same datatype
	return intervalindices, intervalnumindices

def flexactivity2(timestamp_data_array, dp_data_array, threshold, intervalindices, intervalnumindices ):
	intervalactivities = []
	intervalstarttimes = []
	intervalstartindices = []
	n = 0
	n2 = 0
	for m in xrange(0,len(intervalindices)-1,2):
		activetime = 0
		printdata = []
		startindex = np.searchsorted(intervalnumindices, intervalindices[m])
		endindex = np.searchsorted(intervalnumindices, intervalindices[m+1]) + 1 # Add one because xrange below is non-inclusive
		shortarray = intervalnumindices[startindex:endindex]
		for m3 in xrange(0, len(shortarray)-1,2):
			activetimebool = False
			for m4 in xrange(shortarray[m3], shortarray[m3+1]+1):
				if dp_data_array[m4] > threshold:
					activetimebool = True
				if activetimebool == True:
					activetime = activetime + 1
					break
		intervalactivities.append( activetime )
		intervalstarttimes.append(timestamp_data_array[intervalindices[m]])
		intervalstartindices.append( intervalindices[m] )
	return (intervalactivities, intervalstarttimes, intervalstartindices)

def bout_flexactivity2(timestamp_data_array, all_bouts, dpix_all_bouts, displacements, timeintervaldenom, timestart, timeend, timestamp_data_dict, dropped_indices, fish_centerfracs):
	intervalactivities = []
	intervalstarttimes = []
	indexstart = 0
	indexend = 0
	tdelta = timeend - timestart
	intervalnumber = int(tdelta.total_seconds()) / timeintervaldenom # How many different chunks of time to break it into (ie, 10 minutes in active minutes per 10 minutes)
	indexstart = timestamp_data_dict[timestart] # The index value for the first occurrence of the start time, so this is the inclusive value
	indexend = timestamp_data_dict[timeend] # The index value for the first occurrence of the start time, so this is the inclusive value
	intervalindices = []
	intervalindices.append(indexstart)
	timetest = timestart

	bout_startsl = []
	dpix_bout_startsl = []
	bout_distancesl = []
	dpix_bout_cumdpixl = []
	bout_timesl = []
	dpix_bout_timesl = []
	interbout_interval = []
	dpix_interbout_interval = []
	long_interbout_interval = []
	dpix_long_interbout_interval = []

	for r in xrange(0, (len(all_bouts))):
		bout_startsl.append(all_bouts[r][0])
		if r != len(all_bouts)-1:
			interbout_interval.append((timestamp_data_array[all_bouts[r+1][0]] - timestamp_data_array[all_bouts[r][1]]).total_seconds()) # NEED TO CHECK WHETHER +1 WORKS HERE OR IF IT WILL FAIL
			if (timestamp_data_array[all_bouts[r+1][0]] - timestamp_data_array[all_bouts[r][1]]).total_seconds() >= 1.0:
				long_interbout_interval.append((timestamp_data_array[all_bouts[r+1][0]] - timestamp_data_array[all_bouts[r][1]]).total_seconds()) # NEED TO CHECK WHETHER +1 WORKS HERE OR IF IT WILL FAIL
			else:
				long_interbout_interval.append(np.nan)
		bout_distancesl.append(all_bouts[r][4])
		bout_timesl.append(float(all_bouts[r][3]) * 1000)
	# same thing as above, just for dpix
	for r in xrange(0, (len(dpix_all_bouts))):
		dpix_bout_startsl.append(dpix_all_bouts[r][0])
		if r != len(dpix_all_bouts)-1:
			dpix_interbout_interval.append((timestamp_data_array[dpix_all_bouts[r+1][0]] - timestamp_data_array[dpix_all_bouts[r][1]]).total_seconds()) # NEED TO CHECK WHETHER +1 WORKS HERE OR IF IT WILL FAIL
			if (timestamp_data_array[dpix_all_bouts[r+1][0]] - timestamp_data_array[dpix_all_bouts[r][1]]).total_seconds() >= 1.0:
				dpix_long_interbout_interval.append((timestamp_data_array[dpix_all_bouts[r+1][0]] - timestamp_data_array[dpix_all_bouts[r][1]]).total_seconds()) # NEED TO CHECK WHETHER +1 WORKS HERE OR IF IT WILL FAIL
			else:
				dpix_long_interbout_interval.append(np.nan)
		dpix_bout_cumdpixl.append(dpix_all_bouts[r][4])
		dpix_bout_timesl.append(float(dpix_all_bouts[r][3]) * 1000)

	bout_dist = np.array(bout_distancesl)
	bout_cumdpix = np.array(dpix_bout_cumdpixl)
	bout_time = np.array(bout_timesl)
	dpix_bout_time = np.array(dpix_bout_timesl)
	bout_dispoverdist = np.array(displacements) / bout_dist
	bout_speed = bout_dist / bout_time
	bout_vel = np.array(displacements) / bout_time
	centerfracs = np.array(fish_centerfracs[0])
	averhofracs = np.array(fish_centerfracs[1])
	intercenterfracs = np.array(fish_centerfracs[2])
	interaverhofracs = np.array(fish_centerfracs[3])
	#bout_distoverdpix = bout_dist / dpix_bout_cumdpixl

	for z in xrange(0,intervalnumber):
		z = z+1
		timetest1 = timetest + datetime.timedelta(seconds=(timeintervaldenom * z)) #This is the same as the start time
		if timetest1 not in dropped_indices:
			indext = timestamp_data_dict[timetest1]
			intervalindices.append(indext-1) #The very last index of the end of the chunk
			intervalindices.append(indext) #The very first index of the next start of the chunk
	bout_startsl = np.array(bout_startsl, dtype=int)
	dpix_bout_startsl = np.array(dpix_bout_startsl, dtype=int)

	# All of the features that will be returned
	numberofbouts = []
	dpix_numberofbouts = []
	bouttimes = []
	dpix_bouttimes = []
	dpixbouts_minus_distbouts = [] # quality control check to make sure the numbers are the same, shouldn't be really off from zero most of the time
	boutcumdist = []
	dpix_boutcumdpix = []
	boutcumdist_over_boutcumdpix = []
	boutdisp = []
	boutspeeds = []
	boutvelocities = []
	boutdispoverdist = []
	interboutinterval = []
	dpix_interboutinterval = []
	longinterboutinterval = []
	dpix_longinterboutinterval = []
	averhofrac = []
	centerfrac = []
	inter_averhofrac = []
	inter_centerfrac = []

	intervalindices = np.array(intervalindices, dtype=int)
	for m in xrange(0,len(intervalindices)-1,2):
		activetime = 0
		boutyorn = 0
		dpix_boutyorn = 0
		bouttimesinterval = []
		dpix_bouttimesinterval = []
		boutcumdistinterval = []
		dpix_boutcumdpixinterval = []
		boutdispinterval = []
		boutspeedsinterval = []
		boutvelocitiesinterval = []
		boutdispoverdistinterval = []
		boutcumdistovercumdpixinterval = []
		interboutintervalinterval = []
		dpix_interboutintervalinterval = []
		longinterboutintervalinterval = []
		dpix_longinterboutintervalinterval = []
		averhofracinterval = []
		interaverhofracinterval = []
		centerfracinterval = []
		intercenterfracinterval = []
		dpixbouts_minus_distbouts_interval = []

		testintarray_start = np.searchsorted(bout_startsl, intervalindices[m])
		dpixtestintarray_start = np.searchsorted(dpix_bout_startsl, intervalindices[m])
		testintarray_end = np.searchsorted(bout_startsl, intervalindices[m+1])# DO I ADD ONE HERE OR NO? SAME WITH FLEXACTIVITY2??
		dpixtestintarray_end = np.searchsorted(dpix_bout_startsl, intervalindices[m+1])# DO I ADD ONE HERE OR NO? SAME WITH FLEXACTIVITY2??
		for w in xrange(testintarray_start, testintarray_end):
			boutyorn = boutyorn + 1
			bouttimesinterval.append(bout_time[w])
			boutcumdistinterval.append(bout_dist[w])
			boutdispinterval.append(displacements[w])
			boutdispoverdistinterval.append(bout_dispoverdist[w])
			boutspeedsinterval.append(bout_speed[w])
			boutvelocitiesinterval.append(bout_vel[w])
			averhofracinterval.append(averhofracs[w])
			centerfracinterval.append(centerfracs[w])
			if w < (testintarray_end-1):
				interaverhofracinterval.append(interaverhofracs[w])
				intercenterfracinterval.append(intercenterfracs[w])
				interboutintervalinterval.append(interbout_interval[w])
				longinterboutintervalinterval.append(long_interbout_interval[w])
		for w2 in xrange(dpixtestintarray_start, dpixtestintarray_end):
			dpix_boutyorn = dpix_boutyorn + 1
			dpix_bouttimesinterval.append(dpix_bout_time[w2])
			dpix_boutcumdpixinterval.append(dpix_bout_cumdpixl[w2])
			if w2 < (dpixtestintarray_end-1):
				dpix_interboutintervalinterval.append(dpix_interbout_interval[w2])
				dpix_longinterboutintervalinterval.append(dpix_long_interbout_interval[w2])
		numberofbouts.append(boutyorn) # Should this one and the following 3 be means??
		dpix_numberofbouts.append(dpix_boutyorn)
		dpixbouts_minus_distbouts.append(dpix_boutyorn - boutyorn)
		boutcumdist_over_boutcumdpix.append(np.mean(np.array(boutcumdistinterval)) / np.mean(np.array(dpix_boutcumdpixinterval)))
		bouttimes.append(np.mean(bouttimesinterval))
		dpix_bouttimes.append(np.mean(dpix_bouttimesinterval))
		boutcumdist.append(np.mean(boutcumdistinterval))
		dpix_boutcumdpix.append(np.mean(dpix_boutcumdpixinterval))
		boutdisp.append(np.mean(boutdispinterval))
		boutdispoverdist.append(np.mean(boutdispoverdistinterval))
		boutspeeds.append(np.mean(boutspeedsinterval))
		boutvelocities.append(np.mean(boutvelocitiesinterval))
		averhofrac.append(np.mean(averhofracinterval))
		inter_averhofrac.append(np.mean(interaverhofracinterval))
		centerfrac.append(np.mean(centerfracinterval))
		inter_centerfrac.append(np.mean(intercenterfracinterval))
		interboutinterval.append(np.mean(interboutintervalinterval))
		dpix_interboutinterval.append(np.mean(dpix_interboutintervalinterval))
		longinterboutinterval.append(np.nanmean(longinterboutintervalinterval))
		dpix_longinterboutinterval.append(np.nanmean(dpix_longinterboutintervalinterval))
	# SHOULD MAKE A BOUT_DATA OBJECT FOR THIS, TO MAKE IT EASIER TO GET THEM OUT AFTER
	return (numberofbouts, dpix_numberofbouts, dpixbouts_minus_distbouts, bouttimes, dpix_bouttimes, boutcumdist, dpix_boutcumdpix, boutdisp, boutspeeds, boutvelocities, boutdispoverdist, averhofrac, inter_averhofrac, centerfrac, inter_centerfrac, interboutinterval, dpix_interboutinterval, longinterboutinterval, dpix_longinterboutinterval, boutcumdist_over_boutcumdpix)

def bout_data(timestamp_data_array, timestamp_data_dict, fish_distances, fish_list, dropped_indices, all_fish_bouts, dpix_all_fish_bouts, fish_displacements, fish_centerfracs):
	timestart = timestamp_data_array[0]
	timeend = timestamp_data_array[len(timestamp_data_array)-1]
	bout_data = {}
	for fish in fish_list:
		activity_list = []
		permintuple = ()
		per10mintuple = ()
		permintuple = bout_flexactivity2(timestamp_data_array, all_fish_bouts[fish.idnumber], dpix_all_fish_bouts[fish.idnumber], fish_displacements[fish.idnumber], 60, timestart, timeend, timestamp_data_dict, dropped_indices, fish_centerfracs[fish.idnumber])
		per10mintuple = bout_flexactivity2(timestamp_data_array, all_fish_bouts[fish.idnumber], dpix_all_fish_bouts[fish.idnumber], fish_displacements[fish.idnumber], 600, timestart, timeend, timestamp_data_dict, dropped_indices, fish_centerfracs[fish.idnumber])
		activity_list.append(permintuple)
		activity_list.append(per10mintuple)
		bout_data[fish.idnumber] = activity_list
	return bout_data

def activity_time_data(timestamp_data_array, timestamp_data_dict, fish_distances, fish_list, dropped_indices):
	timestart = timestamp_data_array[0]
	timeend = timestamp_data_array[len(timestamp_data_array)-1]
	(secminintervalindices, secminintervalnumindices) = determine_indices(timestamp_data_array, 60, timestart, timeend, 1, timestamp_data_dict, dropped_indices)
	(min10minintervalindices, min10minintervalnumindices) = determine_indices(timestamp_data_array, 600, timestart, timeend, 60, timestamp_data_dict, dropped_indices)
	activity_time_data = {}
	for fish in fish_list:
		activity_list = []
		secmintuple = ()
		dsecmintuple = ()
		min10mintuple = ()
		dmin10mintuple = ()
		secmintuple = flexactivity2(timestamp_data_array, fish_distances[fish.idnumber], 0, secminintervalindices, secminintervalnumindices)
		min10mintuple = flexactivity2(timestamp_data_array, fish_distances[fish.idnumber], 0, min10minintervalindices, min10minintervalnumindices)
		dsecmintuple = flexactivity2(timestamp_data_array, fish.dpix, 10.0, secminintervalindices, secminintervalnumindices)
		dmin10mintuple = flexactivity2(timestamp_data_array, fish.dpix, 10.0, min10minintervalindices, min10minintervalnumindices)
		activity_list.append(secmintuple)
		activity_list.append(dsecmintuple)
		activity_list.append(min10mintuple)
		activity_list.append(dmin10mintuple)
		activity_time_data[fish.idnumber] = activity_list
	return activity_time_data

def process_all_data():
	(fish_list, timestamp_data_array, timestamp_data_dict, dropped_indices, global_tuple_events) = fileloading.loading_procedures()
	fish_distances = calculate_distance(fish_list)
	hs_fish_distances = hs_calculate_distance(fish_list)
	all_fish_bouts = {}
	dpix_all_fish_bouts = {}
	for fish in fish_list:
		fish_distances_list = fish_distances[fish.idnumber]
		all_fish_bouts[fish.idnumber] = findBoutIndices(fish_distances_list, timestamp_data_array, 1.0, 1)
		dpix_all_fish_bouts[fish.idnumber] = findBoutIndices(fish.dpix, timestamp_data_array, 3.0, 3)
	fish_displacements = calculate_displacement(fish_list, all_fish_bouts)
	fish_centerfracs = calculate_centerfrac(fish_list, all_fish_bouts)
	# this contains list of tuples instead of list of single information, because it is centerfrac and then averhofrac
	activitytimedata = activity_time_data(timestamp_data_array, timestamp_data_dict, fish_distances, fish_list, dropped_indices)
	slowboutdata = bout_data(timestamp_data_array, timestamp_data_dict, fish_distances, fish_list, dropped_indices, all_fish_bouts, dpix_all_fish_bouts, fish_displacements, fish_centerfracs)
	fishevents = {}
	time_list = []
	for fish in fish_list:
		fishevents[fish.idnumber] = []
		for e in global_tuple_events[2]:
			if e.type != "time":
				# This is where the EventSection type becomes associated with a fish and starts containing real data
				#print "type, name: ", e.type, e.name
				bout_data_all = event_bout_freq(fish.hs_dict, hs_fish_distances[fish.idnumber], e.events, fish_distances[fish.idnumber], fish.dpix, timestamp_data_dict, timestamp_data_array, 0.9, 2, 3.0, 3, fish.hs_pos_x, fish.hs_pos_y, fish.x_array, fish.y_array)
				newe = copy.copy(e)
				newe.__dict__ = e.__dict__.copy()
				newe.add_bout_data_dist(bout_data_all)
				fishevents[fish.idnumber].append(newe)
			else:
				time_list.append((e.starttime, e.endtime, e.name))
		time_list = list(set(time_list))
	analyzed_fish_list = []
	for fish in fish_list:
		newanalyzedfish = AnalyzedFish(fish.idnumber, fish.genotype, fish.dpix, fish.rho_array, fish.theta_array, fish.x_array, fish.y_array, fish_distances[fish.idnumber], fish_displacements[fish.idnumber], all_fish_bouts[fish.idnumber], activitytimedata[fish.idnumber][0], activitytimedata[fish.idnumber][1], activitytimedata[fish.idnumber][2], activitytimedata[fish.idnumber][3], slowboutdata[fish.idnumber][0], slowboutdata[fish.idnumber][1], fishevents[fish.idnumber])
		analyzed_fish_list.append(newanalyzedfish)
	return analyzed_fish_list, timestamp_data_array, timestamp_data_dict, dropped_indices, time_list

(analyzed_fish_list, timestamp_data_array, timestamp_data_dict, dropped_indices, time_list) = process_all_data()
setupfishgraphing.time_plots(analyzed_fish_list, time_list, timestamp_data_dict)
setupfishgraphing.bout_plots(analyzed_fish_list, time_list, timestamp_data_dict)
setupfishgraphing.response_graphs(analyzed_fish_list)
setupfishgraphing.polar_plot(analyzed_fish_list, time_list, timestamp_data_dict)
statsandgraphs.all()
