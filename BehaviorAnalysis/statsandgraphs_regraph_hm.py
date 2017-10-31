#!/usr/bin/python
import os,sys,glob,re
import numpy as np
import scipy
from scipy import stats
import datetime
import time
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors as c
from matplotlib  import cm
from scipy.stats.kde import gaussian_kde
from numpy import linspace
from scipy.stats import kruskal
#from scipy.stats import nanmean
#from scipy.stats import nanmedian
import pandas as pd
import statsmodels.api as sm
from scipy.stats import mstats
from matplotlib.ticker import FormatStrFormatter

# MAKE LIST OF ALL THINGS BEING COMBINE - TRY AVERAGE AND ALSO LOWEST P-VALUE
# LOWEST WOULD WORK IF STATS ARE MORE RELIABLE. I THINK I PROBABLY WILL USE THIS.

# don't forget!!!!! You will need to switch order for some and subtract wt from mut or swap signs on the means or the coefficient!

#min_split_dict = {"10min_day1evening":[("10min_day1evening",None,None)], "min_day1evening":[("min_day1evening",None,None)], "10min_day1taps":[("10min_day1taps",None,None)], "min_day1taps":[("min_day1taps",None,None)], "10min_day2darkflashes":[("10min_day2darkflashes",None,None)], "min_day2darkflashes":[("min_day2darkflashes",None,None)], "10min_day2heatshock":[("10min_day2heatshock",None,None)], "min_day2heatshock":[("min_day2heatshock",None,None)], "10min_day2nightstim":[("10min_day2nightstim",None,None)], "min_day2nightstim":[("min_day2nightstim",None,None)], "min_day1day":[("min_day1day",14,None)], "min_day2morning":[("min_day2night2",0,119), ("min_day2morntrans",119,129), ("min_day2morning",129,None)], "min_day1mornstim":[("min_day1mornstim",0,120)], "min_day1night":[("min_day1night",0,-9), ("min_day1morntrans",-9,None)], "10min_day1day":[("10min_day1day",1,None)], "10min_day2morning":[("10min_day2night2",0,10), ("10min_day2morning",11,None)], "10min_day1mornstim":[("10min_day1mornstim",0,12)], "10min_day1night":[("10min_day1night",0,-1)]} # Can't do the "TRANS" times for 10min because they would be one datapoint
skip_list = ["dpixnumberofbouts_minus_distnumberofbouts", "avelonginterboutinterval", "aveboutdispoverdist", "aveboutcumdistovercumdpix", "distoverdpix", "polygonareadivdist", "daytap1", "nighttap1"]

doubledict = {"nightprepulseinhibition100b":"nightprepulseinhibition102", "dayprepulseinhibition100b":"dayprepulseinhibition102", "shortnightprepulseinhibition100b":"shortnightprepulseinhibition102", "shortdayprepulseinhibition100b":"shortdayprepulseinhibition102", "nightprepulseinhibition100c":"nightprepulseinhibition102", "dayprepulseinhibition100c":"dayprepulseinhibition102", "shortnightprepulseinhibition100c":"shortnightprepulseinhibition102", "shortdayprepulseinhibition100c":"shortdayprepulseinhibition102", "a2darkflash103":"adarkflash103", "b2darkflash103":"bdarkflash103", "c2darkflash103":"cdarkflash103", "d2darkflash103":"ddarkflash103", "d0darkflash103":"a0darkflash103", "adaytaphab102":"adaytappre102", "bdaytaphab102":"adaytappostbdaytappre102", "cdaytaphab102":"bdaytappostcdaytappre102", "nighttaphab102":"nighttappre102"}


labels = {
"latencyresponse_dpix": ("Events", "Response latency (ms)"),
"freqresponse_dpix": ("Events", "Response frequency"),
"polygonarea_dist": ("Events", "Response area (pixels)"),
"timeresponse_dpix": ("Events", "Response time (ms)"),
"totaldistanceresponse_dist": ("Events", "Response cumulative distance (pixels)"),
"fullboutdatamax_dpix": ("Events", "Maximum dpix (pixels)"),
"fullboutdatamax_dist": ("Events", "Maximum distance (pixels)"),
"fullboutdatamaxloc_dpix": ("Events", "Time of maximum dpix (ms)"),
"fullboutdatamaxloc_dist": ("Events", "Time of maximum distance (ms)"),
"fullboutdata_dpix": ("Time (ms)", "Dpix (pixels)"),
"fullboutdata_dist": ("Time (ms)", "Distance (pixels)"),
"velocityresponse_dist": ("Events", "Response velocity (pixels / ms)"),
"speedresponse_dist": ("Events", "Response speed (pixels / ms)"),
"cumdpixresponse_dpix": ("Events", "Response cumulative dpix (pixels)"),
"displacement_dist": ("Events", "Response displacement (pixels)"),
"boutcenterfrac_10min": ("Time (min)", "Fraction of interbout time in well center / 10 min"),
"boutcenterfrac_min": ("Time (min)", "Fraction of interbout time in well center / min"),
"boutaverhofrac_10min": ("Time (min)", "Average interbout rho / maximum rho / 10 min"),
"boutaverhofrac_min": ("Time (min)", "Average interbout rho / maximum rho / min"),
"_centerfrac_10min": ("Time (min)", "Fraction of bout time in well center / 10 min"),
"_centerfrac_min": ("Time (min)", "Fraction of bout time in well center / min"),
"_averhofrac_10min": ("Time (min)", "Average bout rho / maximum rho / 10 min"),
"_averhofrac_min": ("Time (min)", "Average bout rho / maximum rho / min"),
"aveboutdisp_min": ("Time (min)", "Average bout displacement (pixels)"),
"aveboutdisp_10min": ("Time (min)", "Average bout displacement (pixels)"),
"aveboutdist_min": ("Time (min)", "Average bout distance (pixels)"),
"aveboutdist_10min": ("Time (min)", "Average bout distance (pixels)"),
"distsecper_min": ("Time (min)", "Active (dist) second / min"),
"dpixsecper_min": ("Time (min)", "Active (dpix) second / min"),
"distminper_10min": ("Time (min)", "Active (dist) min / 10 min"),
"dpixminper_10min": ("Time (min)", "Active (dpix) min / 10 min"),
"aveboutvel_min": ("Time (min)", "Average bout velocity (pixels / ms) / min"),
"aveboutspeed_min": ("Time (min)", "Average bout speed (pixels / ms) / min"),
"aveboutvel_10min": ("Time (min)", "Average bout velocity (pixels / ms) / 10 min"),
"aveboutspeed_10min": ("Time (min)", "Average bout speed (pixels / ms) / 10 min"),
"aveboutcumdpix_10min": ("Time (min)", "Average bout cumulative dpix (pixels) / 10 min"),
"aveboutcumdpix_min": ("Time (min)", "Average bout cumulative dpix (pixels) / min"),
"aveinterboutinterval_min": ("Time (min)", "Average interbout (dist) interval (sec) / min"),
"aveinterboutinterval_10min": ("Time (min)", "Average interbout (dist) interval (sec) / 10 min"),
"dpixinterboutinterval_min": ("Time (min)", "Average interbout (dpix) interval (sec) / min"),
"dpixinterboutinterval_10min": ("Time (min)", "Average interbout (dpix) interval (sec) / 10 min"),
"_avebouttime_min": ("Time (min)", "Average bout (dist) time (ms) / min"),
"_avebouttime_10min": ("Time (min)", "Average bout (dist) time (ms) / 10 min"),
"dpixavebouttime_min": ("Time (min)", "Average bout (dpix) time (ms)  / min"),
"dpixavebouttime_10min": ("Time (min)", "Average bout (dpix) time (ms) / 10 min"),
"_numberofbouts_min": ("Time (min)", "Number of bouts (dist) / min"),
"_numberofbouts_10min": ("Time (min)", "Number of bouts (dist) / 10 min"),
"dpixnumberofbouts_min": ("Time (min)", "Number of bouts (dpix) / min"),
"dpixnumberofbouts_10min": ("Time (min)", "Number of bouts (dpix) / 10 min"),
} # no longer need the min and 10 min because I'm switching them all to min, but not changing now

def hm_plot(intensity, type):
	heatgraphname = "heatgraphnew" + type +".png"
#	f = open(heatgraphname + "_data", 'w')
#	for x in range(0, len(intensity)):
#		f.write(' '.join(str(z) for z in intensity[x]))
#		f.write('\n')
#	f.close()
	x = range(0,len(intensity[0])+1)
	y = range(0,len(intensity)+1)
	x,y = np.meshgrid(x,y)
	intensity = np.array(intensity)
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	im = ax1.pcolormesh(x,y,intensity,cmap='hot',vmin=0,vmax=np.nanmax(intensity))
	plt.colorbar(im)
	plt.savefig(heatgraphname, transparent=True)
	plt.close()

def plate_hm(genotypefile):
	for file in glob.glob(genotypefile):
		f = open(file, 'r')
		lines = f.readlines()
		f.close()
		genotype_list = {}
		genotype_dict = {"controlgroup": "wt", "testgroup": "hom"}
		for line in lines:
			dictkey = genotype_dict[line.split(':')[0]]
			fishidslist = line.split(':')[1].strip().split(',')
			fishidslist2 = [int(i) for i in fishidslist]
			fishidslist2.sort()
			inputids = []
			for id in fishidslist2:
				inputids.append(id)
			genotype_list[dictkey] = inputids

def find_labels(ribgraphname):
	xlabel = ""
	ylabel = ""
	for l in labels.keys():
		if l in ribgraphname:
			xlabel = labels[l][0]
			ylabel = labels[l][1]
	return xlabel, ylabel

def box_plot(array1, array2, type, ylabel):
	data = []
	nparray1 = np.asarray(array1)
	nparray2 = np.asarray(array2)
	data.append(nparray1)
	data.append(nparray2)
	boxgraphname = "boxgraph_pd_" + "_" + type + ".png"
	dictdata = {}
	for l in range(0, len(data)):
		if data[l].ndim > 1:
			mu1 = np.nanmean(data[l], axis=1)
		else:
			mu1 = data[l]
		dictdata[str(l)] = mu1
	df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dictdata.iteritems() ]))
	df.to_csv(boxgraphname + "_data", sep='\t')
	plt.clf()
	plt.cla()
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	ax1.set_ylabel(ylabel)
	ax1.set_xlabel("Control, Test")
	xticks = ["control", "test"]
	ax1.set_xticklabels(xticks)
	plot = df.boxplot(ax=ax1)
	plt.savefig(boxgraphname, transparent=True)
	plt.close()

def ribbon_plot(array1, array2, type, xlabel, ylabel, t = None):
	ribgraphname = type + ".png"
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	array1 = np.atleast_2d(array1)
	array2 = np.atleast_2d(array2)
	if t == None:
		t = np.arange(np.shape(array1)[1])
		if "fullboutdata_" in ribgraphname:
			t = t * 3.5
		if "_10min_" in ribgraphname:
			t = t * 10
			# more than 3 hours
		if "combo" in ribgraphname:
		# trying to change axis ticks to ms
			t = t.astype(float)
			t = t / 60.0
			xlabel = "Time (hour)"
			ax1.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
		#print "t: ", t
	if "histgraph" in ribgraphname:
#		xlabel = "Bins"
		xlabel = ylabel + " (binned)"
		ylabel = "Probability"
	mu1 = np.nanmean(array1, axis=0)
	sigma1 = stats.sem(array1, axis=0, nan_policy='omit')
	mu2 = np.nanmean(array2, axis=0)
	sigma2 = stats.sem(array2, axis=0, nan_policy='omit')
	# trying to change axis ticks to ms
#	if "fullboutdata_" in ribgraphname:
#		scale = 3.5
#		ticks = ticker.FuncFormatter(lambda t, pos: '{0:g}'.format(x*scale))
#		ax1.xaxis.set_major_formatter(ticks)
	ax1.plot(t, mu1, lw=1, label = "mean wt", color = 'black')
	ax1.plot(t, mu2, lw=1, label = "mean mut", color = 'red')
	ax1.fill_between(t, mu1+sigma1, mu1-sigma1, facecolor='black', alpha=0.3)
	ax1.fill_between(t, mu2+sigma2, mu2-sigma2, facecolor='red', alpha=0.3)
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(ylabel)
	ax1.grid()
	fig.savefig(ribgraphname, transparent=True)
	plt.close()

def linear_model_array(ribgraphname, array1, array2):
	fw = open(ribgraphname + "_newdata.csv", 'w')
	fw.write("time,movement,id,mutornot\n")
	# Used to have this check in the justlmm.py, but I don't think I need it now that I'm preprocessing
	#if datawt.shape[0] > 5 and datamut.shape[0] > 5:
	for n in range(0, array1.shape[0]):
		t = 0
		for d in array1[n,:]:
			fw.write(str(t))
			fw.write(",")
			fw.write(str(d))
			fw.write(",")
			fw.write(str(n))
			fw.write(",wt")
			fw.write("\n")
			t = t+1
	for n2 in range(0, array2.shape[0]):
		t2 = 0
		for d2 in array2[n2,:]:
			fw.write(str(t2))
			fw.write(",")
			fw.write(str(d2))
			# just adding 100 to the id number, so that it's different from wt ids, since real ids are gone by now
			fw.write(",")
			fw.write(str(int(n2) + 100))
			fw.write(",mut")
			fw.write("\n")
			t2 = t2+1
	fw.close()
	data = pd.read_csv(ribgraphname + "_newdata.csv")
	data = data[data.movement.notnull()]
	model = sm.MixedLM.from_formula("movement ~ mutornot + time + mutornot * time", data, groups=data["id"])
	result = model.fit()
	print ribgraphname
	print result.summary()

def linear_model_re(ribgraphname, array1, array2):
	data = pd.read_csv(ribgraphname + "_newdata.csv")
	data = data[data.movement.notnull()]
	model = sm.MixedLM.from_formula(formula = "movement ~ mutornot", re_formula="time", data=data, groups=data["id"])
	result = model.fit()
	print ribgraphname
	print result.summary()

def calculate_peak(fullarray):
	# THIS IS TO GET THE PEAK VALUE FOR THE FULLBOUTDATA PLOTS
	maxlist = []
	maxlistloc = []
	for n in range (0, np.shape(fullarray)[0]):
		maxtest = np.nanmax(fullarray[n,:])
		maxlist.append(maxtest)
		maxloc = np.where(fullarray[n,:]==maxtest)[0]
		maxloc = maxloc * 3.5
		if np.shape(maxloc)[0] > 0:
			maxlistloc.append(maxloc[0])
	maxarray = np.asarray(maxlist)
	maxarrayloc = np.asarray(maxlistloc)
	return maxarray, maxarrayloc

def anova(dataname, nparray1, nparray2):
	if nparray1.ndim > 1:
		H, pval = mstats.kruskalwallis(np.nanmean(nparray1, axis=1), np.nanmean(nparray2, axis=1))
		print "anova: ", dataname, ': Mean of array wt, mut, H-stat, P-value: ', str(np.nanmean(np.nanmean(nparray1,axis=1))), str(np.nanmean(np.nanmean(nparray2,axis=1))), str(H), str(pval)
	else:
		H, pval = mstats.kruskalwallis(nparray1, nparray2)
		print "anova: ", dataname, ': Mean of array wt, mut, H-stat, P-Value: ', str(np.nanmean(np.nanmean(nparray1))), str(np.nanmean(np.nanmean(nparray2))), str(H), str(pval)

def read_process_data(ribgraphname, newarray_dict, anov_dict):
	skip = False
	for skip in skip_list:
		if skip in ribgraphname:
			return
	arraywt = np.loadtxt(ribgraphname + "_a1_data", delimiter = ',')
	arraymut = np.loadtxt(ribgraphname + "_a2_data", delimiter=',')
	if "histgraph" not in ribgraphname:
		if "_min_" in ribgraphname or "_10min_" in ribgraphname:
			if "combo" not in ribgraphname:
				newarray_dict[ribgraphname] = (arraywt, arraymut)
			anov_dict[ribgraphname] = (arraywt, arraymut)
		elif "fullboutdata" in ribgraphname:
			fullmaxpeakswt,fullmaxpeakslocwt = calculate_peak(arraywt)
			fullmaxpeaksmut,fullmaxpeakslocmut = calculate_peak(arraymut)
			#newarray_dict[ribgraphname] = (arraywt, arraymut)
			ribbon_plot(arraywt, arraymut, ribgraphname.split('.')[0], find_labels(ribgraphname)[0], find_labels(ribgraphname)[1])
			mlname = ribgraphname.replace("fullboutdata", "fullboutdatamaxloc")
			mname = ribgraphname.replace("fullboutdata", "fullboutdatamax")
			if "_darkflash" not in ribgraphname:
				anov_dict[mname] = (fullmaxpeakswt, fullmaxpeaksmut)
				anov_dict[mlname] = (fullmaxpeakslocwt, fullmaxpeakslocmut)
		else:
			#print "ones that are left: ", ribgraphname # this should be everything else
			# avoiding all the ones where there is no data in the file (like velocity on slow dark flashes)
			if np.shape(arraywt)[0] > 0:
				if "_darkflash" in ribgraphname:
					newarray_dict[ribgraphname] = (arraywt, arraymut)
				else:
					anov_dict[ribgraphname] = (arraywt, arraymut)
	else:
		# for the histgraphs, probably don't need any statistics, but want to make the plots
		bincenters = np.loadtxt(ribgraphname + "_bincenters", delimiter = ',')
		if arraywt.ndim <2 or arraymut.ndim < 2:
			return
		ribbon_plot(arraywt, arraymut, ribgraphname.split('.')[0], find_labels(ribgraphname)[0], find_labels(ribgraphname)[1], bincenters)
		# no longer adding it, just making the graph right away here, since I don't need stats on it
		#anov_dict[ribgraphname] = (arraywt, arraymut)

def ratiographs(anov_dict):
	# This would fail if you were renaming the ratios something that was in doubledict . . .
	for k in anov_dict.keys():
		ksplit = k.split(".")[0].split("_")[-1]
		#ribgraph_mean_ribbon_fullboutdatamaxloc_dist_nighttappre102.png
		if "fullboutdata" not in k and "histgraph" not in k:
			if ksplit in doubledict.keys():
				# ksplit is the key, type is the value
				# "nightprepulseinhibition100b":"nightprepulseinhibition102"
				# want to divide the key by the value
				type = doubledict[ksplit]
				#newrname is value
				newrname = k.replace(ksplit,type)
				#print ksplit, k, newrname, anov_dict[k][0], anov_dict[newrname][0]
				#divwt = np.divide(np.nanmean(anov_dict[newrname][0], axis=1),np.nanmean(anov_dict[k][0],axis=1))
				divwt = np.divide(np.nanmean(anov_dict[k][0], axis=1),np.nanmean(anov_dict[newrname][0],axis=1))
				#divmut = np.divide(np.nanmean(anov_dict[newrname][1], axis=1),np.nanmean(anov_dict[k][1],axis=1))
				divmut = np.divide(np.nanmean(anov_dict[k][1], axis=1),np.nanmean(anov_dict[newrname][1],axis=1))
				#newname = "ratio" + type + "_over_" + k.split(".")[0] + ".png"
				newname = "ratio" + "_".join(k.split(".")[0].split("_")[:-1])  + "_" + ksplit + "_over_" + type + ".png"
				anov_dict[newname] = (divwt,divmut)

def all():
	#for file in glob.glob("ribgraph_mean_ribbonbout_numberofbouts_*_day2night*.png"):
	timenewarray_dict = {} # Data I'm using with linear model, needed preprocessing, will use the coefficient (first value in the list) to figure out if + or -
	anovnewarray_dict = {} # Data I'm just doing the anova on
	for file in glob.glob("rib*_a1_data"):
		file = file.split("_a1_data")[0]
		try:
			read_process_data(file, timenewarray_dict, anovnewarray_dict)
		except:
			continue
	# setup the ratio sets
	ratiographs(anovnewarray_dict)
	print "Anova section: "
	for k2 in anovnewarray_dict.keys():
		if "histgraph" not in k2:
		#	try:
			#	anova(k2, anovnewarray_dict[k2][0], anovnewarray_dict[k2][1])
		#	except:
		#		print "anova failed: ", k2
#			box_plot(anovnewarray_dict[k2][0], anovnewarray_dict[k2][1], k2.split('.')[0], find_labels(k2)[1])
			if "fullboutdatamax" not in k2 or "ratio" not in k2:
				if anovnewarray_dict[k2][0].ndim <2 or anovnewarray_dict[k2][1].ndim < 2:
					print k2.split('.')[0], " only has one dimension ", anovnewarray_dict[k2][0].ndim, anovnewarray_dict[k2][1].ndim
					continue
#				ribbon_plot(anovnewarray_dict[k2][0], anovnewarray_dict[k2][1], k2.split('.')[0], find_labels(k2)[0], find_labels(k2)[1])
				hm_plot(anovnewarray_dict[k2][0], "_wt_" + k2.split('.')[0])
				hm_plot(anovnewarray_dict[k2][1], "_mut_" + k2.split('.')[0])
		else:
			if anovnewarray_dict[k2][0].ndim <2 or anovnewarray_dict[k2][1].ndim < 2:
					print k2.split('.')[0], " only has one dimension ", anovnewarray_dict[k2][0].ndim, anovnewarray_dict[k2][1].ndim
					continue
#			ribbon_plot(anovnewarray_dict[k2][0], anovnewarray_dict[k2][1], k2.split('.')[0], find_labels(k2)[0], find_labels(k2)[1])
			hm_plot(anovnewarray_dict[k2][0], "_wt_" + k2.split('.')[0])
			hm_plot(anovnewarray_dict[k2][1], "_mut_" + k2.split('.')[0])
	print "Linear multiply model section: "
	for k in timenewarray_dict.keys():
		try:
			#linear_model_array(k, timenewarray_dict[k][0], timenewarray_dict[k][1])
#			ribbon_plot(timenewarray_dict[k][0], timenewarray_dict[k][1], k.split('.')[0], find_labels(k)[0], find_labels(k)[1])
			hm_plot(timenewarray_dict[k2][0], "_wt_" + k2.split('.')[0])
			hm_plot(timenewarray_dict[k2][1], "_mut_" + k2.split('.')[0])
		except:
			print "linear model failed: ", k
#	print "Linear retime model section: "
# The time as a random effect model doesn't do well with heatshock data or stimuli (things with single peak)
#	for k in timenewarray_dict.keys():
#		try:
#			linear_model_re(k, timenewarray_dict[k][0], timenewarray_dict[k][1])
#		except:
#			print "linear model failed: ", k
all()
