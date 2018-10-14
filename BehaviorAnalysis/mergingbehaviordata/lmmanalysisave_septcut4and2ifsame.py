#!/usr/bin/python
import os,sys,glob,re
import numpy as np
import scipy
from scipy import stats
import datetime
import time
from datetime import timedelta
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from matplotlib import colors as c
#from matplotlib  import cm
from scipy.stats.kde import gaussian_kde
from numpy import linspace
from scipy.stats import kruskal
#from scipy.stats import nanmean
#from scipy.stats import nanmedian
import pandas as pd
import statsmodels.api as sm
from scipy.stats import mstats

#freqlist = ["numberofbouts_min", "numberofbouts_10min", "dpixnumberofbouts_min", "dpixnumberofbouts_10min", "aveinterboutinterval_min", "aveinterboutinterval_10min", "avedpixinterboutinterval_min", "avedpixinterboutinterval_10min", "dpixsecpermin", "dpixminper10min", "distsecpermin", "distminper10min"]
#loclist = ["interboutcenterfrac", "interboutaverhofrac", "centerfrac", "averhofrac"]
#featlist = ["dpixavebouttime_min", "dpixavebouttime_10min", "aveboutvel_min", "aveboutvel_10min", "avebouttime_min", "avebouttime_10min", "aveboutspeed_min", "aveboutspeed_10min", "aveboutdist_min", "aveboutdist_10min", "aveboutdisp_min", "aveboutdisp_10min", "aveboutcumdpix_min", "aveboutcumdpix_10min"]

nonstimcombos = {"Frequency of movement":  ["numberofbouts_min", "numberofbouts_10min", "dpixnumberofbouts_min", "dpixnumberofbouts_10min", "aveinterboutinterval_min", "aveinterboutinterval_10min", "avedpixinterboutinterval_min", "avedpixinterboutinterval_10min", "dpixsecper_min", "dpixminper_10min", "distsecper_min", "distminper_10min"], "Location in well": ["interboutcenterfrac_min", "interboutaverhofrac_min", "centerfrac_min", "averhofrac_min","interboutcenterfrac_10min", "interboutaverhofrac_10min", "centerfrac_10min", "averhofrac_10min"], "Features of movement": ["dpixavebouttime_min", "dpixavebouttime_10min", "aveboutvel_min", "aveboutvel_10min", "avebouttime_min", "avebouttime_10min", "aveboutspeed_min", "aveboutspeed_10min", "aveboutdist_min", "aveboutdist_10min", "aveboutdisp_min", "aveboutdisp_10min", "aveboutcumdpix_min", "aveboutcumdpix_10min"]}

typecombos = [["Night tap habituation", "Day tap habituation 1", "Day tap habituation 2", "Day tap habituation 3"], ["Day light flash", "Night light flash"],["Night early prepulse tap", "Day early prepulse tap"], ["Night all prepulse tap", "Day all prepulse tap"], ["Day all strong tap", "Night all strong tap"], ["Day early strong tap","Night early strong tap"],["Night early weak tap", "Day early weak tap"], ["Day all weak tap", "Night all weak tap"], ["Dark flash block 3 start","Dark flash block 3 end","Dark flash block 4 start","Dark flash block 4 end","Dark flash block 1 start","Dark flash block 1 end","Dark flash block 2 start","Dark flash block 2 end"]]

stimcombos = {
	#"Day light flash and weak tap": ["106106"],
	#"Night light flash and weak tap": ["night106106"],
	"Night tap habituation": ["nighttaphab102", "nighttaphab1"],
	"Day tap habituation 1": ["adaytaphab102", "adaytaphab1"],
	"Day tap habituation 3": ["cdaytaphab102", "cdaytaphab1"],
	"Day tap habituation 2": ["bdaytaphab102", "bdaytaphab1"],
	"Day light flash": ["lightflash104"],
	#"Day light flash": ["lightflash104", "lightflash0"],
	"Night light flash": ["nightlightflash104"],
	#"Night light flash": ["nightlightflash104", "nightlightflash0"],
	"Night early prepulse tap": ["shortnightprepulseinhibition100b"],
	#"Night early prepulse tap": ["shortnightprepulseinhibition100b", "shortnightprepulseinhibition100c"],
	"Night all prepulse tap": ["nightprepulseinhibition100b"],
	#"Night all prepulse tap": ["nightprepulseinhibition100b", "nightprepulseinhibition100c"],
	"Day early prepulse tap": ["shortdayprepulseinhibition100b"],
	#"Day early prepulse tap": ["shortdayprepulseinhibition100b", "shortdayprepulseinhibition100c"],
	"Day all prepulse tap": ["dayprepulseinhibition100b"],
	#"Day all prepulse tap": ["dayprepulseinhibition100b", "dayprepulseinhibition100c"],
	"Day all weak tap": ["dayprepulseinhibition100a", "dayprepulseinhibition101"],
	"Day early weak tap": ["shortdayprepulseinhibition100a", "shortdayprepulseinhibition101"],
	"Night all weak tap": ["nightprepulseinhibition100a", "nightprepulseinhibition101"],
	"Night early weak tap": ["shortnightprepulseinhibition100a", "shortnightprepulseinhibition101"],
	"Day early strong tap": ["adaytappre102", "shortdayprepulseinhibition102"],
	#"Day early strong tap": ["adaytappre102", "adaytappre1", "shortdayprepulseinhibition102"],
	"Day all strong tap": ["dayprepulseinhibition102", "adaytappostbdaytappre102","bdaytappostcdaytappre102", "cdaytappost102"],
	#"Day all strong tap": ["dayprepulseinhibition102", "adaytappostbdaytappre102","bdaytappostcdaytappre102", "bdaytappostcdaytappre1", "cdaytappost1", "cdaytappost102","adaytappostbdaytappre1"],
	"Night early strong tap": ["nighttappre102"],
	#"Night early strong tap": ["nighttappre1", "nighttappre102"],
	"Night all strong tap": ["nightprepulseinhibition102","nighttappost102"],
	#"Night all strong tap": ["nightprepulseinhibition102","nighttappost102", "nighttappost1"],
	#"Dark flash all blocks": ["darkflash103", "darkflash0"],
	"Dark flash block 3 start": ["cdarkflash103"],
	"Dark flash block 3 end": ["c2darkflash103"],
	"Dark flash block 1 start": ["adarkflash103"],
	"Dark flash block 1 end": ["a2darkflash103"],
	"Dark flash block 2 start": ["bdarkflash103"],
	"Dark flash block 2 end": ["b2darkflash103"],
	"Dark flash block 4 start": ["ddarkflash103"],
	"Dark flash block 4 end": ["d2darkflash103"]}
#	"Dark flash block 3 start": ["cdarkflash103", "cdarkflash0"],
#	"Dark flash block 3 end": ["c2darkflash103", "c2darkflash0"],
#	"Dark flash block 1 start": ["adarkflash103", "adarkflash0"],
#	"Dark flash block 1 end": ["a2darkflash103", "a2darkflash0"],
#	"Dark flash block 2 start": ["bdarkflash103", "bdarkflash0"],
#	"Dark flash block 2 end": ["b2darkflash103", "b2darkflash0"],
#	"Dark flash block 4 start": ["ddarkflash103", "ddarkflash0"],
#	"Dark flash block 4 end": ["d2darkflash103", "d2darkflash0"]}

#direction = {
#	"aveboutspeed": 1
#	"aveboutspeed": 1
# ones that are opposite of expected
# fullboutdatamaxloc (max peak location (larger is less strong of response))
# latency (longer is less good), similar to max peak
# aveinterboutinterval
# rho or centerfrac, not sure which orientation would want
# make wall-hugging positive
# lower centerfrac means more positive, which is how it is right now I think, yes, so if I default everything to switching signs, then averhofrac is the odd one out and should be skipped
# for most, larger should mean - and should mean mutant is stronger response or more movement
# need to make most into opposite
# standard
# cumdpix, displacement, distance, speed, velocity, secpermin, numberofbouts, frequency of response, polygonarea
# unsure - fullboutdata as done with linear model, and also the dark flash ones done with linear model
#}
direction_swaps = ["rhofrac", "latency", "interboutinterval", "fullboutdatamaxloc"]

for file in glob.glob("*linearmodel*"): # THIS IS WHAT THE PRINT OUTPUT MUST POINT TO, CAN HAVE SOMETHING AT END, BUT MUST START THIS WAY
	if "finalsorted" in file:
		continue
	dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
	ffile = open('finalsortedupdatedCP4or2_' + file + "_" + dir, 'w')
	ofile = open(file, 'r')
	lines = ofile.readlines()
	pdict = {}
	for line in lines:
		# anova data
		if line.startswith("anova:"):
			pval = line.split(":")[3].strip().split()[3].strip()
			#anova:  ribgraph_mean_ribbon_latencyresponse_dpix_nighttappost102.png : Mean of array wt, mut, H-stat, P-value:  25.8557471264 21.4177419355 2.63243902441 0.104700765405
			meanwtminmut = float(line.split(":")[3].strip().split()[0]) - float(line.split(":")[3].strip().split()[1])
			name = line.split(":")[1].strip()
			pdict[name] = [pval, meanwtminmut]
#			ffile.write(str(pval))
#			ffile.write(', ')
#			ffile.write(str(meanwtminmut))
#			ffile.write(', ')
#			ffile.write(name.strip())
#			ffile.write('\n')
		# linear mixed model data - this formatting could change if I change the linear model I'm using
		else:
			list = []
			for line in range(0, len(lines)):
		#print lines[line]
				if lines[line].startswith("mutornot[T.wt] "):
			#print lines[line]
					if len(lines[line].split()) > 3:
						pvalue = lines[line].split()[4]
						coef = lines[line].split()[1]
						if float(pvalue) == 0:
							pvalue = 0.001
						list.append((float(pvalue), float(coef), lines[line-13].strip()))
						#list.append((float(pvalue), lines[line-13].strip(), lines[line].split()[1:6]))
		#		list2 = sorted(list, key=lambda x: x[0])
			for fline in list:
				#pdict[str(fline[2])] = (str(fline[0])[:8], str(fline[1])[:8])
				pdict[str(fline[2])] = [str(fline[0])[:8], str(fline[1])[:8]]
				#ffile.write(str(fline[0])[:8])
				#ffile.write(', ')
				#ffile.write(str(fline[1])[:8])
				#ffile.write(', ')
				#ffile.write(str(fline[2]))
				#ffile.write('\n')
	splitdict = {}
	for k in pdict:
		# k = ribgraph_mean_ribbonbout_dpixavebouttime_min_day1taps.png
		# section = day1taps
		# or section = adaytappostbdaytappre102
		if k.startswith("ratio"):
			continue
		section = k.split('.')[0].split('_')[-1]
		for k2 in nonstimcombos.keys():
			# k2 = "Frequency of movement"
			for v2 in nonstimcombos[k2]:
				# v2 = numberofbouts_min
				if v2 in k:
					test = False
					for k3 in splitdict.keys():
						if (k2 + " " + section) == k3:
							test = True
					if test == False:
						splitdict[k2 + " " + section] = []
						splitdict[k2 + " " + section].append([k,pdict[k]])
					else:
						splitdict[k2 + " " + section].append([k,pdict[k]])
					break
		for sk2 in stimcombos.keys():
			# sk2 = "Night light flash"
			for sv2 in stimcombos[sk2]:
				# sv2 = nightlightflash104
				if sv2 == k.split('.')[0].split('_')[-1]:
					# combining everything for these stimuli responses
					test = False
					for sk3 in splitdict.keys():
						if sk2 == sk3:
							test = True
					if test == False:
						splitdict[sk2] = []
						splitdict[sk2].append([k,pdict[k]])
					else:
						splitdict[sk2].append([k,pdict[k]])
					break
	for skey in splitdict.keys():
		lowest = 10
		listints = []
		cutpoint = 0.05
		cutpointnumber = 3
		if skey in stimcombos.keys():
			cutpointnumber = 4
		else:
			cutpointnumber = 3
		cutlist = []
		for t in typecombos:
			for tt in t:
				if skey == tt:
					#cutpointnumber = 4
					#print "TEST", skey, t
					import copy
					shortt = copy.copy(t)
					shortt.remove(tt)
					#print shortt
					for svey0 in splitdict[skey]:
						if abs(float(svey0[1][0]))  < cutpoint:
							if "bigmovesribgraph_mean_ribbon_freqresponse_dpix_" in svey0[0] and "100b.png" in svey0[0]:
								cutpointnumber = 0
							#print "testing1 ", skey, svey0
							for ttt in shortt:
								for tsvey in splitdict[ttt]:
									#print "testing3", ttt, tsvey
									if '_'.join(svey0[0].split('.')[0].split('_')[:-1]) == '_'.join(tsvey[0].split('.')[0].split('_')[:-1]):
										#print "testing4", ttt, tsvey, '_'.join(svey0[0].split('.')[0].split('_')[:-1]), '_'.join(tsvey[0].split('.')[0].split('_')[:-1])
										if abs(float(tsvey[1][0])) < cutpoint:
											#print "testing5", tsvey
											cutpointnumber = 2
											break
		for svey in splitdict[skey]:
			switch = False
			for x in direction_swaps:
				if x in svey[0]:
					switch = True
			if switch == False:
				if float(svey[1][1]) > 0:
					# change the sign of the original data
					# if wt is moving more than mutant (>0), want signs swapped so mutant is over wt (ie, mutant moving less than wt has - number)
					svey[1][0] = float(svey[1][0]) * -1
				# else, data is fine as is
			else: # switch == True
				# in the cases where a switch is needed for the sign (such as interboutinterval because it's opposite when considering frequency)
				if float(svey[1][1]) < 0: # if wt has greater interboutinterval and then the number is positive (ie, mutant moves more), don't swap, do swap if <
					# change the sign of the original data
					svey[1][0] = float(svey[1][0]) * -1
		#lowest = 10
		#listints = []
		#cutpoint = 0.05
		#cutpointnumber = 3
		#cutlist = []
		for svey in splitdict[skey]:
			#print skey, svey
			listints.append(float(svey[1][0]))
			if abs(float(svey[1][0])) < abs(lowest):
				lowest = float(svey[1][0])
			if abs(float(svey[1][0])) < cutpoint:
				cutlist.append(float(svey[1][0]))
		ave = np.mean(np.absolute(np.asarray(listints)))
		if lowest < 0:
			ave = ave * -1
		if len(cutlist) > cutpointnumber:
			cutave = np.mean(np.absolute(np.asarray(cutlist)))
			if lowest < 0:
				cutave = cutave * -1
		else:
			cutave = ave
		ffile.write("Lowest ")
		ffile.write(skey)
		ffile.write(": ")
		ffile.write(str(lowest))
		ffile.write('\n')
		ffile.write("Average ")
		ffile.write(skey)
		ffile.write(": ")
		ffile.write(str(ave))
		ffile.write('\n')
		ffile.write("Lowaverage (reg if not >")#3, <0.05) ")
		ffile.write(str(cutpointnumber))
		ffile.write(", <0.05) ")
		ffile.write(skey)
		ffile.write(": ")
		ffile.write(str(cutave))
		ffile.write('\n')
		for svey in splitdict[skey]:
			ffile.write(str(svey[0]))
			ffile.write(', ')
			ffile.write(str(svey[1][0]))
			ffile.write(', ')
			ffile.write(str(svey[1][1]))
			ffile.write('\n')
	#print splitdict
	#ffile.write(k)
	#ffile.write(', ')
	#ffile.write(str(pdict[k][0]))
	#ffile.write(', ')
	#ffile.write(str(pdict[k][1]))
	#ffile.write('\n')
