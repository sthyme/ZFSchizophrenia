#!/usr/bin/python

import os,sys,glob,re
import numpy as np
import scipy
import datetime
import time
from datetime import timedelta
from AnalyzedFish import AnalyzedFish # fish object
from scipy import stats
from scipy.stats import norm
from scipy.stats import mstats

import fileloading # prepares all the files
import savedata # has all the graphs that can be made - NO, now just saves data, probably don't need separate file for this . . .  .

import pandas as pd
import statsmodels.api as sm

# Should just get rid of the savedata.py and move this to here, and then move heatmap function to statsandgraphs.py
# But not important right now, so just leaving
#def savedata(array1, array2, type, xlabel, ylabel, t = None):
#	ribgraphname = "ribgraph_mean_" + type + ".png"
#	np.savetxt(ribgraphname + "_a1_data", np.array(array1,dtype=np.float64), delimiter = ',')
#	np.savetxt(ribgraphname + "_a2_data", np.array(array2,dtype=np.float64), delimiter=',')

def listtoNanarray(list):
	nparray = np.asarray(list,dtype=np.float32)
	nparray[nparray==0.0]=np.nan
	return nparray

def hist_plot_latency(wtarray, mutarray, graphtitle, xaxis, yaxis):
	wts = []
	muts = []
	flatwt0 = np.array(wtarray).flatten()
	flatwt = flatwt0[np.logical_not(np.isnan(flatwt0))]
	flatmut0 = np.array(mutarray).flatten()
	flatmut = flatmut0[np.logical_not(np.isnan(flatmut0))]
	totaldata = np.concatenate([flatwt, flatmut])
	hist, bin_edges = np.histogram(totaldata, bins=21)
	for f0 in wtarray:
		f0 = np.array(f0)
		f = f0[np.logical_not(np.isnan(f0))]
		wts.append(np.array(np.histogram(f, bins=bin_edges)[0]))
	for mf0 in mutarray:
		mf0 = np.array(mf0)
		mf = mf0[np.logical_not(np.isnan(mf0))]
		muts.append(np.array(np.histogram(mf, bins=bin_edges)[0]))
	bin_centers = []
	for n in range(0, len(bin_edges)-1):
		bin_centers.append((bin_edges[n] + bin_edges[n+1])/2)
	savedata.activity_ribbongraph2(np.array(wts), np.array(muts), "histgraph_latency_21frames_" + graphtitle, xaxis, yaxis, bin_centers)

def hist_plot(wtarray, mutarray, graphtitle, xaxis, yaxis):
	wts = []
	denswts = []
	muts = []
	densmuts = []
	wtsnotave = []
	mutsnotave = []
	# You are going to end up with different max values here . . . .
	# Then it won't work out because you'll have different numbers of bins
	# Need to precalculate based on the max from all arrays being compared
	# This actually won't work as well because each fish has a different max . . . .
	#wtarray = wtarray[np.logical_not(np.isnan(wtarray))]
	#mutarray = mutarray[np.logical_not(np.isnan(mutarray))]
	flatwt0 = np.array(wtarray).flatten()
	flatwt = flatwt0[np.logical_not(np.isnan(flatwt0))]
	flatmut0 = np.array(mutarray).flatten()
	flatmut = flatmut0[np.logical_not(np.isnan(flatmut0))]
	totaldata = np.concatenate([flatwt, flatmut])
	#print "shape of total data: ", np.shape(totaldata), np.shape(flatwt), np.shape(flatmut)
	##hist = np.histogram(totaldata, bins=10)
	hist, bin_edges = np.histogram(totaldata, bins='sturges')
	#hist, bin_edges = np.histogram(totaldata, bins=10)
	###hist, bin_edges = np.histogram(totaldata, bins=np.arange(0, max(totaldata) + 1, 1))
	#print "total_data: ", totaldata
	#print "bin_edges: ", bin_edges
	#print "hist: ", hist
	for f0 in wtarray:
		f0 = np.array(f0)
		#print f0
		#print np.isnan(f0)
		#print np.logical_not(np.isnan(f0))
		f = f0[np.logical_not(np.isnan(f0))]
		#print "wthist: ", np.array(np.histogram(f, bins=bin_edges)[0])
		#wts.append(np.array(np.histogram(f, bins=10)[0]))
		wts.append(np.array(np.histogram(f, bins=bin_edges)[0]))
		#print "wthistdens: ", np.array(np.histogram(f, bins=bin_edges, density=True)[0])
		#denswts.append(np.array(np.histogram(f, bins=10, density=True)[0]))
		denswts.append(np.array(np.histogram(f, bins=bin_edges, density=True)[0]))
		#wts.append(np.histogram(f,bins=numpy.arange(0, max(f) + 1, 1))[0])
	#print "wts: ", wts
	for mf0 in mutarray:
		mf0 = np.array(mf0)
		mf = mf0[np.logical_not(np.isnan(mf0))]
		#muts.append(np.array(np.histogram(mf, bins=10)[0]))
		muts.append(np.array(np.histogram(mf, bins=bin_edges)[0]))
		#densmuts.append(np.array(np.histogram(mf, bins=10, density=True)[0]))
		densmuts.append(np.array(np.histogram(mf, bins=bin_edges, density=True)[0]))
		#muts.append(np.histogram(mf,bins=numpy.arange(0, max(mf) + 1, 1))[0])
	#wts.append(np.histogram(wtarray,bins=numpy.arange(0, max(wtarray) + 1, 1),range=(rangea,rangeb))[0])
	#muts.append(np.histogram(mutarray,bins=binnum,range=(rangea,rangeb))[0])
	#weights_wt = np.ones_like(flatwt)/float(len(flatwt))
	#weights_mut = np.ones_like(flatmut)/float(len(flatmut))
	#print np.array(wts)
	#print bin_edges
	bin_centers = []
	for n in range(0, len(bin_edges)-1):
		bin_centers.append((bin_edges[n] + bin_edges[n+1])/2)
	#savedata.activity_ribbongraph2(np.array(wts), np.array(muts), "histgraph_" + graphtitle, xaxis, yaxis, bin_centers)
	# The ones without density normalized have issues where they show significant differences where there shouldn't be because of different numbers of fish/events
	savedata.activity_ribbongraph2(np.array(denswts), np.array(densmuts), "histgraph_densitytrue_" + graphtitle, xaxis, yaxis, bin_centers)
	#print "shapes00: ", np.shape(np.array(wts))
	#print "shapes0: ", np.shape(np.array(np.histogram(flatwt, bins=bin_edges, density=True)))
	#print "test: ", np.array(np.histogram(flatwt, bins=bin_edges, density=True))
	#print "shapes: ", np.shape(np.array(np.histogram(flatwt, bins=bin_edges, density=True)[0]))
	#savedata.activity_ribbongraph2(np.array(np.histogram(flatwt, bins=10, density=True)[0]), np.array(np.histogram(flatmut, bins=10, density=True)[0]), "histgraph_alldatanoave_" + graphtitle, xaxis, yaxis)
	# not very useful because can't calculate any stats on it
	####savedata.activity_ribbongraph2(np.array(np.histogram(flatwt, bins=bin_edges, density=True)[0]), np.array(np.histogram(flatmut, bins=bin_edges, density=True)[0]), "histgraph_alldatanoave_" + graphtitle, xaxis, yaxis, bin_centers)

def find_indices(timestart, timeend, timestamp_data_dict, startindices):
	startindex = timestamp_data_dict[timestart]
	endindex = timestamp_data_dict[timeend]
	shortstartindex = np.searchsorted(startindices, startindex)
	shortendindex = np.searchsorted(startindices, endindex)
	return shortstartindex, shortendindex

def time_plots(analyzed_fish_list, timelist, timestamp_data_dict):
	for times in timelist:
		timestart = times[0]
		timeend = times[1]
		graphtitle = times[2]
		indexstart = timestamp_data_dict[timestart] # The index value for the first occurrence of the start time, so this is the inclusive value
		indexend = timestamp_data_dict[timeend] # The index value for the first occurrence of the start time, so this is the inclusive value
		wts_dsecpermin = []
		wts_secpermin = []
		wts_dminper10min = []
		wts_minper10min = []
		muts_dsecpermin = []
		muts_secpermin = []
		muts_dminper10min = []
		muts_minper10min = []
		(minshortstartindex, minshortendindex) = find_indices(timestart, timeend, timestamp_data_dict, analyzed_fish_list[0].secmintuple[2])
		(tenminshortstartindex, tenminshortendindex) = find_indices(timestart, timeend, timestamp_data_dict, analyzed_fish_list[0].min10mintuple[2])
		for afish in analyzed_fish_list:
			if afish.genotype == 'wt':
				wts_dsecpermin.append(afish.dsecmintuple[0][minshortstartindex:minshortendindex])
				wts_secpermin.append(afish.secmintuple[0][minshortstartindex:minshortendindex])
				wts_dminper10min.append(afish.dmin10mintuple[0][tenminshortstartindex:tenminshortendindex])
				wts_minper10min.append(afish.min10mintuple[0][tenminshortstartindex:tenminshortendindex])
			if afish.genotype == 'hom':
				muts_dsecpermin.append(afish.dsecmintuple[0][minshortstartindex:minshortendindex])
				muts_secpermin.append(afish.secmintuple[0][minshortstartindex:minshortendindex])
				muts_dminper10min.append(afish.dmin10mintuple[0][tenminshortstartindex:tenminshortendindex])
				muts_minper10min.append(afish.min10mintuple[0][tenminshortstartindex:tenminshortendindex])
		savedata.activity_ribbongraph2(np.array(wts_dsecpermin), np.array(muts_dsecpermin), "ribbon_dpixsecper_min_" + graphtitle, "Time (Minute)", "Active Second / Minute")
		savedata.activity_ribbongraph2(np.array(wts_secpermin), np.array(muts_secpermin), "ribbon_distsecper_min_" + graphtitle, "Time (Minute)", "Active Second / Minute")
		savedata.activity_ribbongraph2(np.array(wts_dminper10min), np.array(muts_dminper10min), "ribbon_dpixminper_10min_" + graphtitle, "Time (10 Minute)", "Active Minute / 10 Minute")
		savedata.activity_ribbongraph2(np.array(wts_minper10min), np.array(muts_minper10min), "ribbon_distminper_10min_" + graphtitle, "Time (10 Minute)", "Active Minute / 10 Minute")
		# Just keeping the heatmaps because they are potentially interesting to check out, not calculating anything with them
	#	savedata.activity_heatmap(wts_dsecpermin, "wts_dpixsecper_min_"+graphtitle)
#		savedata.activity_heatmap(wts_secpermin, "wts_distsecper_min_"+graphtitle)
#		savedata.activity_heatmap(wts_dminper10min, "wts_dpixminper_10min_"+graphtitle)
#		savedata.activity_heatmap(wts_minper10min, "wts_distminper_10min_"+graphtitle)
#		savedata.activity_heatmap(muts_dsecpermin, "muts_dpixsecper_min_"+graphtitle)
#		savedata.activity_heatmap(muts_secpermin, "muts_distsecper_min_"+graphtitle)
#		savedata.activity_heatmap(muts_dminper10min, "muts_dpixminper_10min_"+graphtitle)
#		savedata.activity_heatmap(muts_minper10min, "muts_distminper_10min_"+graphtitle)

def bout_plots(analyzed_fish_list, timelist, timestamp_data_dict):
	#return (numberofbouts, dpix_numberofbouts, dpixbouts_minus_distbouts, bouttimes, dpix_bouttimes, boutcumdist, dpix_boutcumdpix, boutdisp, boutspeeds, boutvelocities, boutdispoverdist, averhofrac, inter_averhofrac, centerfrac, inter_centerfrac, interboutinterval, dpix_interboutinterval, longinterboutinterval, dpix_longinterboutinterval, boutcumdist_over_boutcumdpix)
	for times in timelist:
		timestart = times[0]
		timeend = times[1]
		graphtitle = times[2]
		indexstart = timestamp_data_dict[timestart] # The index value for the first occurrence of the start time, so this is the inclusive value
		indexend = timestamp_data_dict[timeend] # The index value for the first occurrence of the start time, so this is the inclusive value
		wt_bouts = []
		dpix_wt_bouts = []
		wt_dpixbouts_minus_distbouts = []
		wt_times = []#.append(bouttimes)
		dpix_wt_times = []#.append(bouttimes)
		wt_dists = []#.append(boutcumdist)
		dpix_wt_cumdpix = []#.append(boutcumdist)
		wt_cumdist_over_cumdpix = []#.append(boutcumdist)
		wt_disps = []#.append(boutdisp)
		wt_speeds = []#.append(boutspeeds)
		wt_vels = []#.append(boutvelocities)
		wt_dispoverdist = []#.append(boutdispoverdist)
		wt_averhofrac = []#.append(boutdispoverdist)
		wt_inter_averhofrac = []#.append(boutdispoverdist)
		wt_centerfrac = []#.append(boutdispoverdist)
		wt_inter_centerfrac = []#.append(boutdispoverdist)
		wt_interboutinterval = []#.append(boutdispoverdist)
		wt_dpix_interboutinterval = []#.append(boutdispoverdist)
		wt_longinterboutinterval = []#.append(boutdispoverdist)
		wt_dpix_longinterboutinterval = []#.append(boutdispoverdist)
		mut_bouts = []
		dpix_mut_bouts = []
		mut_dpixbouts_minus_distbouts = []
		mut_times = [] #.append(bouttimes)
		dpix_mut_times = [] #.append(bouttimes)
		mut_dists = []#.append(boutcumdist)
		dpix_mut_cumdpix = []#.append(boutcumdist)
		mut_cumdist_over_cumdpix = []#.append(boutcumdist)
		mut_disps = []#.append(boutdisp)
		mut_speeds = [] #.append(boutspeeds)
		mut_vels = []#.append(boutvelocities)
		mut_dispoverdist = []#.append(boutdispoverdist)
		mut_averhofrac = []#.append(boutdispoverdist)
		mut_inter_averhofrac = []#.append(boutdispoverdist)
		mut_centerfrac = []#.append(boutdispoverdist)
		mut_inter_centerfrac = []#.append(boutdispoverdist)
		mut_interboutinterval = []#.append(boutdispoverdist)
		mut_dpix_interboutinterval = []#.append(boutdispoverdist)
		mut_longinterboutinterval = []#.append(boutdispoverdist)
		mut_dpix_longinterboutinterval = []#.append(boutdispoverdist)
		wt10_bouts = []
		dpix_wt10_bouts = []
		wt10_dpixbouts_minus_distbouts = []
		wt10_times = []#.append(bouttimes)
		dpix_wt10_times = []#.append(bouttimes)
		wt10_dists = []#.append(boutcumdist)
		dpix_wt10_cumdpix = []#.append(boutcumdist)
		wt10_cumdist_over_cumdpix = []#.append(boutcumdist)
		wt10_disps = []#.append(boutdisp)
		wt10_speeds = []#.append(boutspeeds)
		wt10_vels = []#.append(boutvelocities)
		wt10_dispoverdist = []#.append(boutdispoverdist)
		wt10_averhofrac = []#.append(boutdispoverdist)
		wt10_inter_averhofrac = []#.append(boutdispoverdist)
		wt10_centerfrac = []#.append(boutdispoverdist)
		wt10_inter_centerfrac = []#.append(boutdispoverdist)
		wt10_interboutinterval = []#.append(boutdispoverdist)
		wt10_dpix_interboutinterval = []#.append(boutdispoverdist)
		wt10_longinterboutinterval = []#.append(boutdispoverdist)
		wt10_dpix_longinterboutinterval = []#.append(boutdispoverdist)
		mut10_bouts = []
		dpix_mut10_bouts = []
		mut10_dpixbouts_minus_distbouts = []
		mut10_times = [] #.append(bouttimes)
		dpix_mut10_times = [] #.append(bouttimes)
		mut10_dists = []#.append(boutcumdist)
		dpix_mut10_cumdpix = []#.append(boutcumdist)
		mut10_cumdist_over_cumdpix = []#.append(boutcumdist)
		mut10_disps = []#.append(boutdisp)
		mut10_speeds = [] #.append(boutspeeds)
		mut10_vels = []#.append(boutvelocities)
		mut10_dispoverdist = []#.append(boutdispoverdist)
		mut10_averhofrac = []#.append(boutdispoverdist)
		mut10_inter_averhofrac = []#.append(boutdispoverdist)
		mut10_centerfrac = []#.append(boutdispoverdist)
		mut10_inter_centerfrac = []#.append(boutdispoverdist)
		mut10_interboutinterval = []#.append(boutdispoverdist)
		mut10_dpix_interboutinterval = []#.append(boutdispoverdist)
		mut10_longinterboutinterval = []#.append(boutdispoverdist)
		mut10_dpix_longinterboutinterval = []#.append(boutdispoverdist)
		# CAN USE THE SAME AS FOR THE TIME PLOTS TO GET THE INDICES
		(minshortstartindex, minshortendindex) = find_indices(timestart, timeend, timestamp_data_dict, analyzed_fish_list[0].secmintuple[2])
		(tenminshortstartindex, tenminshortendindex) = find_indices(timestart, timeend, timestamp_data_dict, analyzed_fish_list[0].min10mintuple[2])
		for afish in analyzed_fish_list:
			if afish.genotype == 'wt':
				wt_bouts.append(afish.boutpermintuple[0][minshortstartindex:minshortendindex])
				dpix_wt_bouts.append(afish.boutpermintuple[1][minshortstartindex:minshortendindex])
				wt_dpixbouts_minus_distbouts.append(afish.boutpermintuple[2][minshortstartindex:minshortendindex])
				wt_times.append(afish.boutpermintuple[3][minshortstartindex:minshortendindex])
				dpix_wt_times.append(afish.boutpermintuple[4][minshortstartindex:minshortendindex])
				wt_dists.append(afish.boutpermintuple[5][minshortstartindex:minshortendindex])
				dpix_wt_cumdpix.append(afish.boutpermintuple[6][minshortstartindex:minshortendindex])
				wt_disps.append(afish.boutpermintuple[7][minshortstartindex:minshortendindex])
				wt_speeds.append(afish.boutpermintuple[8][minshortstartindex:minshortendindex])
				wt_vels.append(afish.boutpermintuple[9][minshortstartindex:minshortendindex])
				wt_dispoverdist.append(afish.boutpermintuple[10][minshortstartindex:minshortendindex])
				wt_averhofrac.append(afish.boutpermintuple[11][minshortstartindex:minshortendindex])
				wt_inter_averhofrac.append(afish.boutpermintuple[12][minshortstartindex:minshortendindex])
				wt_centerfrac.append(afish.boutpermintuple[13][minshortstartindex:minshortendindex])
				wt_inter_centerfrac.append(afish.boutpermintuple[14][minshortstartindex:minshortendindex])
				wt_interboutinterval.append(afish.boutpermintuple[15][minshortstartindex:minshortendindex])
				wt_dpix_interboutinterval.append(afish.boutpermintuple[16][minshortstartindex:minshortendindex])
				wt_longinterboutinterval.append(afish.boutpermintuple[17][minshortstartindex:minshortendindex])
				wt_dpix_longinterboutinterval.append(afish.boutpermintuple[18][minshortstartindex:minshortendindex])
				wt_cumdist_over_cumdpix.append(afish.boutpermintuple[19][minshortstartindex:minshortendindex])
				wt10_bouts.append(afish.boutper10mintuple[0][tenminshortstartindex:tenminshortendindex])
				dpix_wt10_bouts.append(afish.boutper10mintuple[1][tenminshortstartindex:tenminshortendindex])
				wt10_dpixbouts_minus_distbouts.append(afish.boutper10mintuple[2][tenminshortstartindex:tenminshortendindex])
				wt10_times.append(afish.boutper10mintuple[3][tenminshortstartindex:tenminshortendindex])
				dpix_wt10_times.append(afish.boutper10mintuple[4][tenminshortstartindex:tenminshortendindex])
				wt10_dists.append(afish.boutper10mintuple[5][tenminshortstartindex:tenminshortendindex])
				dpix_wt10_cumdpix.append(afish.boutper10mintuple[6][tenminshortstartindex:tenminshortendindex])
				wt10_disps.append(afish.boutper10mintuple[7][tenminshortstartindex:tenminshortendindex])
				wt10_speeds.append(afish.boutper10mintuple[8][tenminshortstartindex:tenminshortendindex])
				wt10_vels.append(afish.boutper10mintuple[9][tenminshortstartindex:tenminshortendindex])
				wt10_dispoverdist.append(afish.boutper10mintuple[10][tenminshortstartindex:tenminshortendindex])
				wt10_averhofrac.append(afish.boutper10mintuple[11][tenminshortstartindex:tenminshortendindex])
				wt10_inter_averhofrac.append(afish.boutper10mintuple[12][tenminshortstartindex:tenminshortendindex])
				wt10_centerfrac.append(afish.boutper10mintuple[13][tenminshortstartindex:tenminshortendindex])
				wt10_inter_centerfrac.append(afish.boutper10mintuple[14][tenminshortstartindex:tenminshortendindex])
				wt10_interboutinterval.append(afish.boutper10mintuple[15][tenminshortstartindex:tenminshortendindex])
				wt10_dpix_interboutinterval.append(afish.boutper10mintuple[16][tenminshortstartindex:tenminshortendindex])
				wt10_longinterboutinterval.append(afish.boutper10mintuple[17][tenminshortstartindex:tenminshortendindex])
				wt10_dpix_longinterboutinterval.append(afish.boutper10mintuple[18][tenminshortstartindex:tenminshortendindex])
				wt10_cumdist_over_cumdpix.append(afish.boutper10mintuple[19][tenminshortstartindex:tenminshortendindex])
			if afish.genotype == 'hom':
				mut_bouts.append(afish.boutpermintuple[0][minshortstartindex:minshortendindex])
				dpix_mut_bouts.append(afish.boutpermintuple[1][minshortstartindex:minshortendindex])
				mut_dpixbouts_minus_distbouts.append(afish.boutpermintuple[2][minshortstartindex:minshortendindex])
				mut_times.append(afish.boutpermintuple[3][minshortstartindex:minshortendindex])
				dpix_mut_times.append(afish.boutpermintuple[4][minshortstartindex:minshortendindex])
				mut_dists.append(afish.boutpermintuple[5][minshortstartindex:minshortendindex])
				dpix_mut_cumdpix.append(afish.boutpermintuple[6][minshortstartindex:minshortendindex])
				mut_disps.append(afish.boutpermintuple[7][minshortstartindex:minshortendindex])
				mut_speeds.append(afish.boutpermintuple[8][minshortstartindex:minshortendindex])
				mut_vels.append(afish.boutpermintuple[9][minshortstartindex:minshortendindex])
				mut_dispoverdist.append(afish.boutpermintuple[10][minshortstartindex:minshortendindex])
				mut_averhofrac.append(afish.boutpermintuple[11][minshortstartindex:minshortendindex])
				mut_inter_averhofrac.append(afish.boutpermintuple[12][minshortstartindex:minshortendindex])
				mut_centerfrac.append(afish.boutpermintuple[13][minshortstartindex:minshortendindex])
				mut_inter_centerfrac.append(afish.boutpermintuple[14][minshortstartindex:minshortendindex])
				mut_interboutinterval.append(afish.boutpermintuple[15][minshortstartindex:minshortendindex])
				mut_dpix_interboutinterval.append(afish.boutpermintuple[16][minshortstartindex:minshortendindex])
				mut_longinterboutinterval.append(afish.boutpermintuple[17][minshortstartindex:minshortendindex])
				mut_dpix_longinterboutinterval.append(afish.boutpermintuple[18][minshortstartindex:minshortendindex])
				mut_cumdist_over_cumdpix.append(afish.boutpermintuple[19][minshortstartindex:minshortendindex])
				mut10_bouts.append(afish.boutper10mintuple[0][tenminshortstartindex:tenminshortendindex])
				dpix_mut10_bouts.append(afish.boutper10mintuple[1][tenminshortstartindex:tenminshortendindex])
				mut10_dpixbouts_minus_distbouts.append(afish.boutper10mintuple[2][tenminshortstartindex:tenminshortendindex])
				mut10_times.append(afish.boutper10mintuple[3][tenminshortstartindex:tenminshortendindex])
				dpix_mut10_times.append(afish.boutper10mintuple[4][tenminshortstartindex:tenminshortendindex])
				mut10_dists.append(afish.boutper10mintuple[5][tenminshortstartindex:tenminshortendindex])
				dpix_mut10_cumdpix.append(afish.boutper10mintuple[6][tenminshortstartindex:tenminshortendindex])
				mut10_disps.append(afish.boutper10mintuple[7][tenminshortstartindex:tenminshortendindex])
				mut10_speeds.append(afish.boutper10mintuple[8][tenminshortstartindex:tenminshortendindex])
				mut10_vels.append(afish.boutper10mintuple[9][tenminshortstartindex:tenminshortendindex])
				mut10_dispoverdist.append(afish.boutper10mintuple[10][tenminshortstartindex:tenminshortendindex])
				mut10_averhofrac.append(afish.boutper10mintuple[11][tenminshortstartindex:tenminshortendindex])
				mut10_inter_averhofrac.append(afish.boutper10mintuple[12][tenminshortstartindex:tenminshortendindex])
				mut10_centerfrac.append(afish.boutper10mintuple[13][tenminshortstartindex:tenminshortendindex])
				mut10_inter_centerfrac.append(afish.boutper10mintuple[14][tenminshortstartindex:tenminshortendindex])
				mut10_interboutinterval.append(afish.boutper10mintuple[15][tenminshortstartindex:tenminshortendindex])
				mut10_dpix_interboutinterval.append(afish.boutper10mintuple[16][tenminshortstartindex:tenminshortendindex])
				mut10_longinterboutinterval.append(afish.boutper10mintuple[17][tenminshortstartindex:tenminshortendindex])
				mut10_dpix_longinterboutinterval.append(afish.boutper10mintuple[18][tenminshortstartindex:tenminshortendindex])
				mut10_cumdist_over_cumdpix.append(afish.boutper10mintuple[19][tenminshortstartindex:tenminshortendindex])
	#(numberofbouts, dpix_numberofbouts, dpixbouts_minus_distbouts, bouttimes, dpix_bouttimes, boutcumdist, dpix_boutcumdpix,  boutdisp, boutspeeds, boutvelocities, boutdispoverdist, averhofrac, inter_averhofrac, centerfrac, inter_centerfrac, interboutinterval, dpix_interboutinterval, longinterboutinveral, dpix_longinterboutinterval)
		savedata.activity_ribbongraph2(np.array(wt_bouts), np.array(mut_bouts), "ribbonbout_numberofbouts_min_" + graphtitle, "Time (Minute)", "Number of Bouts / Minute")
		hist_plot(wt_bouts, mut_bouts, "numberofbouts_min_" + graphtitle, "Number of Bouts / Minute Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(dpix_wt_bouts), np.array(dpix_mut_bouts), "ribbonbout_dpixnumberofbouts_min_" + graphtitle, "Time (Minute)", "Number of Bouts / Minute")
		hist_plot(dpix_wt_bouts, dpix_mut_bouts, "dpixnumberofbouts_min_" + graphtitle, "Number of Bouts / Minute Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_dpixbouts_minus_distbouts), np.array(mut_dpixbouts_minus_distbouts), "ribbonbout_dpixnumberofbouts_minus_distnumberofbouts_min_" + graphtitle, "Time (Minute)", "Number of Bouts / Minute - Number of Bouts / Minute")
		hist_plot(wt_dpixbouts_minus_distbouts, mut_dpixbouts_minus_distbouts, "dpixnumberofbouts_minus_distnumberofbouts_min_" + graphtitle, "Number of Bouts / Minute - Number of Bouts / Minute Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_times), np.array(mut_times), "ribbonbout_avebouttime_min_" + graphtitle, "Time (Minute)", "Average Bout Time (Millisecond)")
		hist_plot(wt_times, mut_times, "avebouttime_min_" + graphtitle, "Average Bout Time (Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(dpix_wt_times), np.array(dpix_mut_times), "ribbonbout_dpixavebouttime_min_" + graphtitle, "Time (Minute)", "Average Bout Time (Millisecond)")
		hist_plot(dpix_wt_times, dpix_mut_times, "dpixavebouttime_min_" + graphtitle, "Average Bout Time (Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_dists), np.array(mut_dists), "ribbonbout_aveboutdist_min_" + graphtitle, "Time (Minute)", "Average Bout Distance (Pixel)")
		hist_plot(wt_dists, mut_dists, "aveboutdist_min_" + graphtitle, "Average Bout Distance (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(dpix_wt_cumdpix), np.array(dpix_mut_cumdpix), "ribbonbout_aveboutcumdpix_min_" + graphtitle, "Time (Minute)", "Average Bout Cumulative DPIX (Pixel)")
		hist_plot(dpix_wt_cumdpix, dpix_mut_cumdpix, "aveboutcumdpix_min_" + graphtitle, "Average Bout Cumulative DPIX (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_cumdist_over_cumdpix), np.array(mut_cumdist_over_cumdpix), "ribbonbout_aveboutcumdistovercumdpix_min_" + graphtitle, "Time (Minute)", "Average Distance Bout Cumulative Distance Over Cumulative DPIX (Pixel / Pixel)")
		hist_plot(wt_cumdist_over_cumdpix, mut_cumdist_over_cumdpix, "aveboutcumdistovercumdpix_min_" + graphtitle, "Average Bout Cumulative DPIX (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_disps), np.array(mut_disps), "ribbonbout_aveboutdisp_min_" + graphtitle, "Time (Minute)", "Average Bout Displacement (Pixel)")
		hist_plot(wt_disps, mut_disps, "aveboutdisp_min_" + graphtitle, "Average Bout Displacement (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_speeds), np.array(mut_speeds), "ribbonbout_aveboutspeed_min_" + graphtitle, "Time (Minute)", "Average Bout Speed (Pixel / Millisecond)")
		hist_plot(wt_speeds, mut_speeds, "aveboutspeed_min_" + graphtitle, "Average Bout Speed (Pixel / Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_vels), np.array(mut_vels), "ribbonbout_aveboutvel_min_" + graphtitle, "Time (Minute)", "Average Bout Velocity (Pixel / Millisecond)")
		hist_plot(wt_vels, mut_vels, "aveboutvel_min_" + graphtitle, "Average Bout Velocity (Pixel / Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_dispoverdist), np.array(mut_dispoverdist), "ribbonbout_aveboutdispoverdist_min_" + graphtitle, "Time (Minute)", "Average Bout Displacement / Distance")
		hist_plot(wt_dispoverdist, mut_dispoverdist, "aveboutdispoverdist_min_" + graphtitle, "Average Bout Displacement / Distance Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_averhofrac), np.array(mut_averhofrac), "ribbonbout_averhofrac_min_" + graphtitle, "Time (Minute)", "Average Rho per Bout / Maximum Rho")
		hist_plot(wt_averhofrac, mut_averhofrac, "averhofrac_min_" + graphtitle, "Average Rho per Bout / Maximum Rho Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_inter_averhofrac), np.array(mut_inter_averhofrac), "ribbonbout_interboutaverhofrac_min_" + graphtitle, "Time (Minute)", "Average Rho per Interbout / Maximum Rho")
		hist_plot(wt_inter_averhofrac, mut_inter_averhofrac, "interaverhofrac_min_" + graphtitle, "Average Rho per Interbout / Maximum Rho Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_centerfrac), np.array(mut_centerfrac), "ribbonbout_centerfrac_min_" + graphtitle, "Time (Minute)", "Fraction of Bout Time in Well Center")
		hist_plot(wt_centerfrac, mut_centerfrac, "centerfrac_min_" + graphtitle, "Fraction of Bout Time in Well Center Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_inter_centerfrac), np.array(mut_inter_centerfrac), "ribbonbout_interboutcenterfrac_min_" + graphtitle, "Time (Minute)", "Fraction of Interbout Time in Well Center")
		hist_plot(wt_inter_centerfrac, mut_inter_centerfrac, "intercenterfrac_min_" + graphtitle, "Fraction of Interbout Time in Well Center Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_interboutinterval), np.array(mut_interboutinterval), "ribbonbout_aveinterboutinterval_min_" + graphtitle, "Time (Minute)", "Average Interbout Interval (Second)")
		hist_plot(wt_interboutinterval, mut_interboutinterval, "aveinterboutinterval_min_" + graphtitle, "Average Interbout Interval (Second) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_dpix_interboutinterval), np.array(mut_dpix_interboutinterval), "ribbonbout_avedpixinterboutinterval_min_" + graphtitle, "Time (Minute)", "Average Interbout Interval (Second)")
		hist_plot(wt_dpix_interboutinterval, mut_dpix_interboutinterval, "avedpixinterboutinterval_min_" + graphtitle, "Average Interbout Interval (Second) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt_longinterboutinterval), np.array(mut_longinterboutinterval), "ribbonbout_avelonginterboutinterval_min_" + graphtitle, "Time (Minute)", "Average Long (>= 1 Second) Interbout Interval (Second)")
		savedata.activity_ribbongraph2(np.array(wt10_bouts), np.array(mut10_bouts), "ribbonbout_numberofbouts_10min_" + graphtitle, "Time (10 Minute)", "Number of Bouts / 10 Minute")
		hist_plot(wt10_bouts, mut10_bouts, "numberofbouts_10min_" + graphtitle, "Number of Bouts / 10 Minute Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(dpix_wt10_bouts), np.array(dpix_mut10_bouts), "ribbonbout_dpixnumberofbouts_10min_" + graphtitle, "Time (10 Minute)", "Number of Bouts / 10 Minute")
		hist_plot(dpix_wt10_bouts, dpix_mut10_bouts, "dpixnumberofbouts_10min_" + graphtitle, "Number of Bouts / 10 Minute Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_dpixbouts_minus_distbouts), np.array(mut10_dpixbouts_minus_distbouts), "ribbonbout_dpixnumberofbouts_minus_distnumberofbouts_10min_" + graphtitle, "Time (10 Minute)", "Number of Bouts / 10 Minute - Number of Bouts / 10 Minute")
		hist_plot(wt10_dpixbouts_minus_distbouts, mut10_dpixbouts_minus_distbouts, "dpixnumberofbouts_minus_distnumberofbouts_10min_" + graphtitle, "Number of Bouts / 10 Minute - Number of Bouts / 10 Minute Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_times), np.array(mut10_times), "ribbonbout_avebouttime_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Time (Millisecond)")
		hist_plot(wt10_times, mut10_times, "avebouttime_10min_" + graphtitle, "Average Bout Time (Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(dpix_wt10_times), np.array(dpix_mut10_times), "ribbonbout_dpixavebouttime_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Time (Millisecond)")
		hist_plot(dpix_wt10_times, dpix_mut10_times, "dpixavebouttime_10min_" + graphtitle, "Average Bout Time (Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_dists), np.array(mut10_dists), "ribbonbout_aveboutdist_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Distance (Pixel)")
		hist_plot(wt10_dists, mut10_dists, "aveboutdist_10min_" + graphtitle, "Average Bout Distance (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(dpix_wt10_cumdpix), np.array(dpix_mut10_cumdpix), "ribbonbout_aveboutcumdpix_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Cumulative DPIX (Pixel)")
		hist_plot(dpix_wt10_cumdpix, dpix_mut10_cumdpix, "aveboutcumdpix_10min_" + graphtitle, "Average Bout Cumulative DPIX (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_cumdist_over_cumdpix), np.array(mut10_cumdist_over_cumdpix), "ribbonbout_aveboutcumdistovercumdpix_10min_" + graphtitle, "Time (10 Minute)", "Average Distance Bout Cumulative Distance Over Cumulative DPIX (Pixel / Pixel)")
		hist_plot(wt10_cumdist_over_cumdpix, mut10_cumdist_over_cumdpix, "aveboutcumdistovercumdpix_10min_" + graphtitle, "Average Bout Cumulative DPIX (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_disps), np.array(mut10_disps), "ribbonbout_aveboutdisp_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Displacement (Pixel)")
		hist_plot(wt10_disps, mut10_disps, "aveboutdisp_10min_" + graphtitle, "Average Bout Displacement (Pixel) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_speeds), np.array(mut10_speeds), "ribbonbout_aveboutspeed_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Speed (Pixel / Millisecond)")
		hist_plot(wt10_speeds, mut10_speeds, "aveboutspeed_10min_" + graphtitle, "Average Bout Speed (Pixel / Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_vels), np.array(mut10_vels), "ribbonbout_aveboutvel_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Velocity (Pixel / Millisecond)")
		hist_plot(wt10_vels, mut10_vels, "aveboutvel_10min_" + graphtitle, "Average Bout Velocity (Pixel / Millisecond) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_dispoverdist), np.array(mut10_dispoverdist), "ribbonbout_aveboutdispoverdist_10min_" + graphtitle, "Time (10 Minute)", "Average Bout Displacement / Distance")
		hist_plot(wt10_dispoverdist, mut10_dispoverdist, "aveboutdispoverdist_10min_" + graphtitle, "Average Bout Displacement / Distance Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_averhofrac), np.array(mut10_averhofrac), "ribbonbout_averhofrac_10min_" + graphtitle, "Time (10 Minute)", "Average Rho per Bout / Maximum Rho")
		hist_plot(wt10_averhofrac, mut10_averhofrac, "averhofrac_10min_" + graphtitle, "Average Rho per Bout / Maximum Rho Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_inter_averhofrac), np.array(mut10_inter_averhofrac), "ribbonbout_interboutaverhofrac_10min_" + graphtitle, "Time (10 Minute)", "Average Rho per Interbout / Maximum Rho")
		hist_plot(wt10_inter_averhofrac, mut10_inter_averhofrac, "interaverhofrac_10min_" + graphtitle, "Average Rho per Interbout / Maximum Rho Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_centerfrac), np.array(mut10_centerfrac), "ribbonbout_centerfrac_10min_" + graphtitle, "Time (10 Minute)", "Fraction of Bout Time in Well Center")
		hist_plot(wt10_centerfrac, mut10_centerfrac, "centerfrac_10min_" + graphtitle, "Fraction of Bout Time in Well Center Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_inter_centerfrac), np.array(mut10_inter_centerfrac), "ribbonbout_interboutcenterfrac_10min_" + graphtitle, "Time (10 Minute)", "Fraction of Interbout Time in Well Center")
		hist_plot(wt10_inter_centerfrac, mut10_inter_centerfrac, "intercenterfrac_10min_" + graphtitle, "Fraction of Interbout Time in Well Center Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_interboutinterval), np.array(mut10_interboutinterval), "ribbonbout_aveinterboutinterval_10min_" + graphtitle, "Time (10 Minute)", "Average Interbout Interval (Second)")
		hist_plot(wt10_interboutinterval, mut10_interboutinterval, "aveinterboutinterval_10min_" + graphtitle, "Average Interbout Interval (Second) Binned", "Frequencies")
		savedata.activity_ribbongraph2(np.array(wt10_dpix_interboutinterval), np.array(mut10_dpix_interboutinterval), "ribbonbout_avedpixinterboutinterval_10min_" + graphtitle, "Time (10 Minute)", "Average Interbout Interval (Second)")
		hist_plot(wt10_dpix_interboutinterval, mut10_dpix_interboutinterval, "avedpixinterboutinterval_10min_" + graphtitle, "Average Interbout Interval (Second) Binned", "Frequencies")

def response_graphs(analyzed_fish_list):
		#bout_data[ek] = (bout_freq_list, bout_disp_list, bout_lat_list, new_bout_time, new_bout_tdist, new_bout_vel, new_bout_speed, poly_areas, dpix_bout_freq_list, dpix_bout_lat_list, dpix_bout_cumdpix, dpix_bout_time, distbouts_dpix_over_dist, full_bout_data, dpix_full_bout_data, event_bout_data, dpix_event_bout_data)
	# All is put in correctly so far, up until polyAreas, and all the of the dpix ones are off, since there's no dpix data anymore
	eventsectionswt = []
	eventsectionsmut = []
	for afish in analyzed_fish_list:
		if afish.genotype == 'wt':
			eventsectionswt.append(afish.fishevents)
		if afish.genotype == 'hom':
			eventsectionsmut.append(afish.fishevents)
	#distance-based data
	disteventdictwt = {}
	distdispeventdictwt = {}
	distlateventdictwt = {}
	distTimeeventdictwt = {}
	distTdisteventdictwt = {}
	distVeleventdictwt = {}
	distSpeedeventdictwt = {}
	distPolyareadictwt = {}
	distPolyareadistdictwt = {}
	#dpix-based data
	eventdictwt = {}
	lateventdictwt = {}
	cumdpixeventdictwt = {} # This is cumulative dpix
	#dispeventdictwt = {} # This is cumulative dpix
	timeeventdictwt = {}
	distoverdpixeventdictwt = {}
	#array data, not single numbers
	fullboutdataeventdictwt = {}
	sloweventboutdataeventdictwt = {}
	dpixfullboutdataeventdictwt = {}
	slowdpixeventboutdataeventdictwt = {}
	peakspeeddictwt = {}
	peakdpixdictwt = {}

	#distance-based data
	disteventdictmut = {}
	distdispeventdictmut = {}
	distlateventdictmut = {}
	distTimeeventdictmut = {}
	distTdisteventdictmut = {}
	distVeleventdictmut = {}
	distSpeedeventdictmut = {}
	distPolyareadictmut = {}
	distPolyareadistdictmut = {}
	#dpix-based data
	eventdictmut = {}
	lateventdictmut = {}
	cumdpixeventdictmut = {} # This is cumulative dpix
	#dispeventdictmut = {} # This is cumulative dpix
	timeeventdictmut = {}
	distoverdpixeventdictmut = {}
	#array data, not single numbers
	fullboutdataeventdictmut = {}
	sloweventboutdataeventdictmut = {}
	dpixfullboutdataeventdictmut = {}
	slowdpixeventboutdataeventdictmut = {}
	peakspeeddictmut = {}
	peakdpixdictmut = {}

	for es0 in eventsectionswt:
		for es in es0:
			for ekeys in es.boutdatadist.keys(): # this is the type of event in the event section
			#for ekeys in es.boutdatadpix.keys(): # this is the type of event in the event section
				if (es.name + ekeys) not in eventdictwt.keys():
					disteventdictwt[es.name + ekeys] = []
					distdispeventdictwt[es.name + ekeys] = []
					distlateventdictwt[es.name + ekeys] = []
					distTimeeventdictwt[es.name + ekeys] = []
					distTdisteventdictwt[es.name + ekeys] = []
					distVeleventdictwt[es.name + ekeys] = []
					distSpeedeventdictwt[es.name + ekeys] = []
					distPolyareadictwt[es.name + ekeys] = []
					distPolyareadistdictwt[es.name + ekeys] = []
					peakdpixdictwt[es.name + ekeys] = []
					peakspeeddictwt[es.name + ekeys] = []
					#dpix-based data
					eventdictwt[es.name + ekeys] = []
					lateventdictwt[es.name + ekeys] = []
					cumdpixeventdictwt[es.name + ekeys] = []
					#dispeventdictwt = {} # This is cumulative dpix
					timeeventdictwt[es.name + ekeys] = []
					distoverdpixeventdictwt[es.name + ekeys] = []
					#array data, not single numbers
					fullboutdataeventdictwt[es.name + ekeys] = []
					sloweventboutdataeventdictwt[es.name + ekeys] = []
					dpixfullboutdataeventdictwt[es.name + ekeys] = []
					slowdpixeventboutdataeventdictwt[es.name + ekeys] = []

					disteventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][0])
					distdispeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][1])
					distlateventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][2])
					distTimeeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][3])
					distTdisteventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][4])
					distVeleventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][5])
					distSpeedeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][6])
					distPolyareadictwt[es.name + ekeys].append(es.boutdatadist[ekeys][7])
					distPolyareadistdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][17])
					peakdpixdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][18])
					peakspeeddictwt[es.name + ekeys].append(es.boutdatadist[ekeys][19])
					#dpix-based data
					eventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][8])
					lateventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][9])
					cumdpixeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][10])
					#dispeventdictwt = {} # This is cumulative dpix
					timeeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][11])
					distoverdpixeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][12])
					#array data, not single numbers
					fullboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][13])
					sloweventboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][15])
					dpixfullboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][14])
					slowdpixeventboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][16])
				else:
					disteventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][0])
					distdispeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][1])
					distlateventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][2])
					distTimeeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][3])
					distTdisteventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][4])
					distVeleventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][5])
					distSpeedeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][6])
					distPolyareadictwt[es.name + ekeys].append(es.boutdatadist[ekeys][7])
					distPolyareadistdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][17])
					#dpix-based data
					peakdpixdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][18])
					peakspeeddictwt[es.name + ekeys].append(es.boutdatadist[ekeys][19])
					eventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][8])
					lateventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][9])
					cumdpixeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][10])
					#dispeventdictwt = {} # This is cumulative dpix
					timeeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][11])
					distoverdpixeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][12])
					#array data, not single numbers
					fullboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][13])
					sloweventboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][15])
					dpixfullboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][14])
					slowdpixeventboutdataeventdictwt[es.name + ekeys].append(es.boutdatadist[ekeys][16])
	for es0 in eventsectionsmut:
		for es in es0:
			for ekeys in es.boutdatadist.keys(): # this is the type of event in the event section
				if (es.name + ekeys) not in eventdictmut.keys():
					disteventdictmut[es.name + ekeys] = []
					distdispeventdictmut[es.name + ekeys] = []
					distlateventdictmut[es.name + ekeys] = []
					distTimeeventdictmut[es.name + ekeys] = []
					distTdisteventdictmut[es.name + ekeys] = []
					distVeleventdictmut[es.name + ekeys] = []
					distSpeedeventdictmut[es.name + ekeys] = []
					distPolyareadictmut[es.name + ekeys] = []
					distPolyareadistdictmut[es.name + ekeys] = []
					peakdpixdictmut[es.name + ekeys] = []
					peakspeeddictmut[es.name + ekeys] = []
					#dpix-based data
					eventdictmut[es.name + ekeys] = []
					lateventdictmut[es.name + ekeys] = []
					cumdpixeventdictmut[es.name + ekeys] = []
					#dispeventdictmut = {} # This is cumulative dpix
					timeeventdictmut[es.name + ekeys] = []
					distoverdpixeventdictmut[es.name + ekeys] = []
					#array data, not single numbers
					fullboutdataeventdictmut[es.name + ekeys] = []
					sloweventboutdataeventdictmut[es.name + ekeys] = []
					dpixfullboutdataeventdictmut[es.name + ekeys] = []
					slowdpixeventboutdataeventdictmut[es.name + ekeys] = []

					disteventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][0])
					distdispeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][1])
					distlateventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][2])
					distTimeeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][3])
					distTdisteventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][4])
					distVeleventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][5])
					distSpeedeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][6])
					distPolyareadictmut[es.name + ekeys].append(es.boutdatadist[ekeys][7])
					distPolyareadistdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][17])
					peakdpixdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][18])
					peakspeeddictmut[es.name + ekeys].append(es.boutdatadist[ekeys][19])
					#dpix-based data
					eventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][8])
					lateventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][9])
					cumdpixeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][10])
					#dispeventdictmut = {} # This is cumulative dpix
					timeeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][11])
					distoverdpixeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][12])
					#array data, not single numbers
					fullboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][13])
					sloweventboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][15])
					dpixfullboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][14])
					slowdpixeventboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][16])
				else:
					disteventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][0])
					distdispeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][1])
					distlateventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][2])
					distTimeeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][3])
					distTdisteventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][4])
					distVeleventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][5])
					distSpeedeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][6])
					distPolyareadictmut[es.name + ekeys].append(es.boutdatadist[ekeys][7])
					distPolyareadistdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][17])
					peakdpixdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][18])
					peakspeeddictmut[es.name + ekeys].append(es.boutdatadist[ekeys][19])
					#dpix-based data
					eventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][8])
					lateventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][9])
					cumdpixeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][10])
					#dispeventdictmut = {} # This is cumulative dpix
					timeeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][11])
					distoverdpixeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][12])
					#array data, not single numbers
					fullboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][13])
					sloweventboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][15])
					dpixfullboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][14])
					slowdpixeventboutdataeventdictmut[es.name + ekeys].append(es.boutdatadist[ekeys][16])
	for k in eventdictwt.keys():
		savedata.activity_ribbongraph2(np.array(eventdictwt[k]), np.array(eventdictmut[k]), "ribbon_freqresponse_dpix_" + k, "Events", "Response Frequency")
		hist_plot(eventdictwt[k], eventdictmut[k], "histgraph_freqresponse_dpix_" + k, "Response Frequency Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(cumdpixeventdictwt[k]), listtoNanarray(cumdpixeventdictmut[k]), "ribbon_cumdpixresponse_dpix_" + k, "Time", "Response Cumulative DPIX")
		hist_plot(listtoNanarray(cumdpixeventdictwt[k]), listtoNanarray(cumdpixeventdictmut[k]), "histgraph_cumdpixresponse_dpix_" + k, "Cumulative DPIX Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(lateventdictwt[k]), listtoNanarray(lateventdictmut[k]), "ribbon_latencyresponse_dpix_" + k, "Events", "Response Latency (Millisecond)")
		hist_plot(listtoNanarray(lateventdictwt[k]), listtoNanarray(lateventdictmut[k]), "histgraph_latencyresponse_dpix_" + k, "Latency (Millisecond) Binned", "Frequencies")
		hist_plot_latency(listtoNanarray(lateventdictwt[k]), listtoNanarray(lateventdictmut[k]), "histgraph_latencyresponse21bins_dpix_" + k, "Latency (Millisecond) Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(timeeventdictwt[k]), listtoNanarray(timeeventdictmut[k]), "ribbon_timeresponse_dpix_" + k, "Events", "Response Time (Millisecond)")
		hist_plot(listtoNanarray(timeeventdictwt[k]), listtoNanarray(timeeventdictmut[k]), "histgraph_timeresponse_dpix_" + k, "Response Time (Millisecond) Binned", "Frequencies")

		savedata.activity_ribbongraph2(np.array(distdispeventdictwt[k]), np.array(distdispeventdictmut[k]), "ribbon_displacement_dist_" + k, "Time", "Response Displacement (Pixels)")
		hist_plot(distdispeventdictwt[k], distdispeventdictmut[k], "histgraph_displacement_dist_" + k, "Response Frequency Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(distTdisteventdictwt[k]), listtoNanarray(distTdisteventdictmut[k]), "ribbon_totaldistanceresponse_dist_" + k, "Events", "Response Total Distance (Pixels)")
		hist_plot(listtoNanarray(distTdisteventdictwt[k]), listtoNanarray(distTdisteventdictmut[k]), "histgraph_totaldistanceresponse_dist_" + k, "Response Total Distance (Pixels) Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(distVeleventdictwt[k]), listtoNanarray(distVeleventdictmut[k]), "ribbon_velocityresponse_dist_" + k, "Events", "Response Velocity (Pixels / mSec)")
		hist_plot(listtoNanarray(distVeleventdictwt[k]), listtoNanarray(distVeleventdictmut[k]), "histgraph_velocitydistanceresponse_dist_" + k, "Response Velocity (Pixels / mSec) Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(distSpeedeventdictwt[k]), listtoNanarray(distSpeedeventdictmut[k]), "ribbon_speedresponse_dist_" + k, "Events", "Response Speed (Pixels / mSec)")
		hist_plot(listtoNanarray(distSpeedeventdictwt[k]), listtoNanarray(distSpeedeventdictmut[k]), "histgraph_speeddistanceresponse_dist_" + k, "Response Speed (Pixels / mSec) Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(distPolyareadictwt[k]), listtoNanarray(distPolyareadictmut[k]), "ribbon_polygonarea_dist_" + k, "Events", "Movement Area (Pixels)")
		hist_plot(distPolyareadictwt[k], distPolyareadictmut[k], "histgraph_polygonarea_dist_" + k, "Movement Area (Pixel) Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(distPolyareadistdictwt[k]), listtoNanarray(distPolyareadistdictmut[k]), "ribbon_polygonareadivdist_dist_" + k, "Events", "Movement Area / Total Distance")
		hist_plot(distPolyareadistdictwt[k], distPolyareadistdictmut[k], "histgraph_polygonareadivdist_dist_" + k, "Movement Area / Total Distance Binned", "Frequencies")

		savedata.activity_ribbongraph2(listtoNanarray(peakdpixdictwt[k]), listtoNanarray(peakdpixdictmut[k]), "ribbon_peakdpix_" + k, "Events", "Dpix (Pixels)")
		hist_plot(peakdpixdictwt[k], peakdpixdictmut[k], "histgraph_peakdpix_" + k, "Peak Dpix", "Dpix (Pixels)")
		savedata.activity_ribbongraph2(listtoNanarray(peakspeeddictwt[k]), listtoNanarray(peakspeeddictmut[k]), "ribbon_peakspeed_" + k, "Events", "Pixels / msec")
		hist_plot(peakspeeddictwt[k], peakspeeddictmut[k], "histgraph_peakspeed_" + k, "Peak Speed", "Pixels / msec")

		savedata.activity_ribbongraph2(listtoNanarray(distoverdpixeventdictwt[k]), listtoNanarray(distoverdpixeventdictmut[k]), "ribbon_distoverdpix_dist_" + k, "Events", "Distance / Cumulative DPIX")
		hist_plot(listtoNanarray(distoverdpixeventdictwt[k]), listtoNanarray(distoverdpixeventdictmut[k]), "histgraph_distoverdpix_dist_" + k, "Distance / Cumulative DPIX Binned", "Frequencies")
		try:
			savedata.activity_ribbongraph2(fullboutdataeventdictwt[k], fullboutdataeventdictmut[k], "ribbon_fullboutdata_dist_" + k, "Time (Frames)", "Distance Traveled (Pixels)")
			savedata.activity_ribbongraph2(dpixfullboutdataeventdictwt[k], dpixfullboutdataeventdictmut[k], "ribbon_fullboutdata_dpix_" + k, "Time (Frames)", "DPIX Traveled (Pixels)")
		except:
			print "failed the fast bout data graphs"
		try:
			savedata.activity_ribbongraph2(sloweventboutdataeventdictwt[k], sloweventboutdataeventdictmut[k], "ribbon_slowfullboutdata_dist_" + k, "Time (Frames)", "Distance Traveled (Pixels)")

			savedata.activity_ribbongraph2(slowdpixeventboutdataeventdictwt[k], slowdpixeventboutdataeventdictmut[k], "ribbon_slowfullboutdata_dpix_" + k, "Time (Frames)", "DPIX Traveled (Pixels)")
		except:
			print "failed the slow bout data graphs"

def polar_plot(analyzed_fish_list, timelist, timestamp_data_dict):
	for times in timelist:
		timestart = times[0]
		timeend = times[1]
		graphtitle = times[2]
		indexstart = timestamp_data_dict[timestart] # The index value for the first occurrence of the start time, so this is the inclusive value
		indexend = timestamp_data_dict[timeend] # The index value for the first occurrence of the start time, so this is the inclusive value
		wts = []
		muts = []
		wts_all = []
		muts_all = []
		# These plots have a decided number of bins because of the numbers of pixels
		# Not calculating statistics on these plots, just have because they can be interesting
		for afish in analyzed_fish_list:
			if afish.genotype == 'wt':
				wts.append(np.histogram(afish.rho_array[indexstart:indexend],bins=10,range=(0,44))[0])
				wts_all.append(afish.rho_array[indexstart:indexend])
			if afish.genotype == 'hom':
				muts.append(np.histogram(afish.rho_array[indexstart:indexend],bins=10,range=(0,44))[0])
				muts_all.append(afish.rho_array[indexstart:indexend])
		savedata.activity_ribbongraph2(np.array(wts), np.array(muts), "histgraph_polar_plot_" + graphtitle, "Rho - 10 Bins", "Number of Frames")
