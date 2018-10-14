#!/usr/bin/python

#requires that you are in a directory you made called "images"

import os,sys,glob,shutil
import pandas as pd
import numpy as np
import collections

#Lowaverage (reg if not >3, <0.05) Location in well day2night2: 0.569

#Repeated genes, 73
#akt3b,ambra1,anp32e,apopt1,arhgap1,astn1,vrk2,atxn7,bcl11b,tmtc1,c10orf32,c2orf69,ca8,cacna1c,cacna1i,cacnb2,chrna5,chrm4,chst12,clcn3,cnksr2,cnnm2,csmd1,csmd3,egr1,elfn1,ep300,fam5b,fes,foxg1,fpgt,ftcdnl1,fxr1,gigyf2,glt8d1,gpm6a,gramd1b,gria1,grin2a,grm3,hcn1,ireb2,lrrn3,klc1,kmt2e,lrriq3,luzp2,mad1l1,man2a2,mbd5,mir137,mmp16,nfkb1,nrgn,ntm,otud7b,plcl1,ptprf,rgs6,satb1,satb2,sbno1,shisa9,shmt2,slc32a1,snap91,srpk2,syngap1,tcf4,tle1,tle3,tsnare1,znf536
# ones that originally had phenotypes
#Repeated genes 46 without noise (reppos2)
reppos = ['akt3b','ambra1','arhgap1','astn1','vrk2','atxn7','bcl11b','c2orf69',"cacna1c","cacnb2","chrm4","chst12","clcn3","cnnm2","csmd1","csmd3","egr1","elfn1","ep300","fam5b","foxg1","fpgt","gigyf2","gpm6a","gramd1b","gria1","grin2a","hcn1","ireb2","lrrn3","kmt2e","luzp2","man2a2","mir137","mmp16","ntm","otud7b","ptprf","rgs6","sbno1","shisa9","shmt2","snap91","syngap1","tcf4","tle3","tsnare1","znf536"]
reppos2 = ['akt3b','ambra1','arhgap1','astn1','atxn7','bcl11b','c2orf69',"cacna1c","cacnb2","chrm4","chst12","clcn3","cnnm2","csmd1","csmd3","egr1","elfn1","ep300","fam5b","foxg1","fpgt","gigyf2","gpm6a","gramd1b","gria1","grin2a","hcn1","ireb2","lrrn3","kmt2e","luzp2","man2a2","mir137","mmp16","ntm","ptprf","rgs6","satb1","sbno1","shisa9","snap91","syngap1","tle3","tsnare1","vrk2","znf536"]

allkeys = [
'Frequency of movement day1night',
'Frequency of movement day1morntrans',
'Frequency of movement day1mornstim',
'Frequency of movement day1day',
'Frequency of movement day1taps',
'Frequency of movement day1evening',
'Frequency of movement day2nighttrans',
'Frequency of movement day2night1',
'Frequency of movement day2nightstim',
'Frequency of movement day2night2',
'Frequency of movement day2morntrans',
'Frequency of movement day2morning',
'Frequency of movement day2darkflashes',
'Frequency of movement day2heatshock',
'Frequency of movement combo',
'Features of movement day1night',
'Features of movement day1morntrans',
'Features of movement day1mornstim',
'Features of movement day1day',
'Features of movement day1taps',
'Features of movement day1evening',
'Features of movement day2nighttrans',
'Features of movement day2night1',
'Features of movement day2nightstim',
'Features of movement day2night2',
'Features of movement day2morntrans',
'Features of movement day2morning',
'Features of movement day2darkflashes',
'Features of movement day2heatshock',
'Features of movement combo',
'Location in well day1night',
'Location in well day1morntrans',
'Location in well day1mornstim',
'Location in well day1day',
'Location in well day1taps',
'Location in well day1evening',
'Location in well day2nighttrans',
'Location in well day2night1',
'Location in well day2nightstim',
'Location in well day2night2',
'Location in well day2morntrans',
'Location in well day2morning',
'Location in well day2darkflashes',
'Location in well day2heatshock',
'Location in well combo',
'Day early prepulse tap',
'Day all prepulse tap',
'Night early prepulse tap',
'Night all prepulse tap',
'Day early weak tap',
'Day all weak tap',
'Night early weak tap',
'Night all weak tap',
'Day early strong tap',
'Day all strong tap',
'Night early strong tap',
'Night all strong tap',
'Day tap habituation 1',
'Day tap habituation 2',
'Day tap habituation 3',
'Night tap habituation',
'Day light flash',
'Night light flash',
'Dark flash block 1 start',
'Dark flash block 1 end',
'Dark flash block 2 start',
'Dark flash block 2 end',
'Dark flash block 3 start',
'Dark flash block 3 end',
'Dark flash block 4 start',
'Dark flash block 4 end']

def recode_empty_cells(dataframe, list_of_columns):
	for column in list_of_columns:
		dataframe[column] = dataframe[column].replace(r'\s+', np.nan, regex=True)
		dataframe[column] = dataframe[column].fillna(1)
	return dataframe

keylist = {0:"Frequency of movement", 1:"Features of movement", 2:"Location in well", 3:"PPI tap", 4:"Weak tap", 5:"Strong tap", 6:"Tap habituation", 7:"Light flash", 8:"Darkflash"}
keydict = {"Frequency of movement":[],"Features of movement":[],"Location in well":[],"PPI tap":[],"Weak tap":[],"Strong tap":[],"Tap habituation":[],"Light flash":[],"Darkflash":[]}

#completedict = {}
def generateDF():
	fulllist = []
	for i in range(0,9):
		completelist = []
		colts = []
		#fw = open("lowavedata.csv", 'w')
		totalgenes = []
		for file in glob.glob("finalsorte*"):
			completeddict = {}
			f = open(file, 'r')
			lines = f.readlines()
			#gene = file.split("linearmodel_")[1]
			#finalsorted_linearmodel_akt3bhetfxhetmJune12_wt_vs_akt3bhetfxhetmJune12_hom_26207700_4294967294.out_man2a2_and_akt3b_box3_set8
			first = file.split('.o')[0]
			second = file.split('.o')[1]
			gene1 = second.split('_')[1]
			if "_and_" in second:
		#		print "AND"
				gene2 = second.split('_and_')[1].split('_')[0]
				if gene1 in first:
					gene = gene1
				elif gene2 in first:
					gene = gene2
			else:
				gene = gene1
			run = file.split('.')[1]
			gene = gene + "+" + run
		#	print file, gene, run
			totalgenes.append(gene)
			hasdata = False
			for line in lines:
				if line.startswith("Lowaverage"):
					hasdata = True
				#	print line
				else:
					continue
				val = line.split(":")[1].strip()
				title = line.split(":")[0].split(")")[1].strip()
				completeddict[title] = val
		# Make ordered set of tuples and then past to OrderedDict
			#print completeddict.keys()
			#print completeddict['Frequency of movement day1night']
			for key in allkeys:
				if key not in completeddict.keys():
					#print "missing value: ", key, file
					completeddict[key] = '2.0'
			tuplelist = [
			[('Frequency of movement Night 1',completeddict['Frequency of movement day1night']),
			('Frequency of movement Morning transition 1',completeddict['Frequency of movement day1morntrans']),
			('Frequency of movement Morning stimulation',completeddict['Frequency of movement day1mornstim']),
			('Frequency of movement Day baseline',completeddict['Frequency of movement day1day']),
			('Frequency of movement Taps',completeddict['Frequency of movement day1taps']),
			('Frequency of movement Evening',completeddict['Frequency of movement day1evening']),
			('Frequency of movement Night transition',completeddict['Frequency of movement day2nighttrans']),
			('Frequency of movement Night 2',completeddict['Frequency of movement day2night1']),
			('Frequency of movement Night stimulation',completeddict['Frequency of movement day2nightstim']),
			('Frequency of movement Night 2b',completeddict['Frequency of movement day2night2']),
			('Frequency of movement Morning transition 2',completeddict['Frequency of movement day2morntrans']),
			('Frequency of movement Morning 2',completeddict['Frequency of movement day2morning']),
			('Frequency of movement Dark flashes',completeddict['Frequency of movement day2darkflashes']),
			('Frequency of movement Heatshock',completeddict['Frequency of movement day2heatshock']),
			('Frequency of movement All',completeddict['Frequency of movement combo'])],
			[('Features of movement Night 1',completeddict['Features of movement day1night']),
			('Features of movement Morning transition 1',completeddict['Features of movement day1morntrans']),
			('Features of movement Morning stimulation',completeddict['Features of movement day1mornstim']),
			('Features of movement Day baseline',completeddict['Features of movement day1day']),
			('Features of movement Taps',completeddict['Features of movement day1taps']),
			('Features of movement Evening',completeddict['Features of movement day1evening']),
			('Features of movement Night transition',completeddict['Features of movement day2nighttrans']),
			('Features of movement Night 2',completeddict['Features of movement day2night1']),
			('Features of movement Night stimulation',completeddict['Features of movement day2nightstim']),
			('Features of movement Night 2b',completeddict['Features of movement day2night2']),
			('Features of movement Morning transition 2',completeddict['Features of movement day2morntrans']),
			('Features of movement Morning 2',completeddict['Features of movement day2morning']),
			('Features of movement Dark flashes',completeddict['Features of movement day2darkflashes']),
			('Features of movement Heatshock',completeddict['Features of movement day2heatshock']),
			('Features of movement All',completeddict['Features of movement combo'])],
			[('Location in well Night 1',completeddict['Location in well day1night']),
			('Location in well Morning transition 1',completeddict['Location in well day1morntrans']),
			('Location in well Morning stimulation',completeddict['Location in well day1mornstim']),
			('Location in well Day baseline',completeddict['Location in well day1day']),
			('Location in well Taps',completeddict['Location in well day1taps']),
			('Location in well Evening',completeddict['Location in well day1evening']),
			('Location in well Night transition',completeddict['Location in well day2nighttrans']),
			('Location in well Night 2',completeddict['Location in well day2night1']),
			('Location in well Night stimulation',completeddict['Location in well day2nightstim']),
			('Location in well Night 2b',completeddict['Location in well day2night2']),
			('Location in well Morning transition 2',completeddict['Location in well day2morntrans']),
			('Location in well Morning 2',completeddict['Location in well day2morning']),
			('Location in well Dark flashes',completeddict['Location in well day2darkflashes']),
			('Location in well Heatshock',completeddict['Location in well day2heatshock']),
			('Location in well All',completeddict['Location in well combo'])],
			[('Day early prepulse tap',completeddict['Day early prepulse tap']),
			('Day all prepulse tap',completeddict['Day all prepulse tap']),
			('Night early prepulse tap',completeddict['Night early prepulse tap']),
			('Night all prepulse tap',completeddict['Night all prepulse tap'])],
			[('Day early weak tap',completeddict['Day early weak tap']),
			('Day all weak tap',completeddict['Day all weak tap']),
			('Night early weak tap',completeddict['Night early weak tap']),
			('Night all weak tap',completeddict['Night all weak tap'])],
			[('Day early strong tap',completeddict['Day early strong tap']),
			('Day all strong tap',completeddict['Day all strong tap']),
			('Night early strong tap',completeddict['Night early strong tap']),
			('Night all strong tap',completeddict['Night all strong tap'])],
			[('Day tap habituation 1',completeddict['Day tap habituation 1']),
			('Day tap habituation 2',completeddict['Day tap habituation 2']),
			('Day tap habituation 3',completeddict['Day tap habituation 3']),
			('Night tap habituation',completeddict['Night tap habituation'])],
			#('Day light flash and weak tap',completeddict['Day light flash and weak tap']),
			#('Night light flash and weak tap',completeddict['Night light flash and weak tap']),
			[('Day light flash',completeddict['Day light flash']),
			('Night light flash',completeddict['Night light flash'])],
			[('Dark flash block 1 start',completeddict['Dark flash block 1 start']),
			('Dark flash block 1 end',completeddict['Dark flash block 1 end']),
			('Dark flash block 2 start',completeddict['Dark flash block 2 start']),
			('Dark flash block 2 end',completeddict['Dark flash block 2 end']),
			('Dark flash block 3 start',completeddict['Dark flash block 3 start']),
			('Dark flash block 3 end',completeddict['Dark flash block 3 end']),
			('Dark flash block 4 start',completeddict['Dark flash block 4 start']),
			('Dark flash block 4 end',completeddict['Dark flash block 4 end'])]]
			#('Dark flash all blocks',completeddict['Dark flash all blocks'])]]
		#'Location in well day2night2', 'Location in well day2night1', 'Day all strong tap', 'Features of movement day1night', 'Frequency of movement day2heatshock', 'Day tap habituation 2', 'Day tap habituation 3', 'Dark flash block 3 start', 'Day tap habituation 1', 'Frequency of movement day2morning', 'Location in well day1taps', 'Dark flash block 2 start', 'Night early prepulse tap', 'Day all weak tap', 'Dark flash block 1 end', 'Features of movement combo', 'Frequency of movement day2night2', 'Features of movement day1taps', 'Frequency of movement day1mornstim', 'Frequency of movement day2night1', 'Frequency of movement day1morntrans', 'Night early strong tap', 'Dark flash all blocks', 'Night light flash', 'Night early weak tap', 'Frequency of movement day2darkflashes', 'Dark flash block 4 end', 'Location in well day1day', 'Location in well day2heatshock', 'Dark flash block 4 start', 'Day early prepulse tap', 'Location in well day1night', 'Frequency of movement day1night', 'Features of movement day2heatshock', 'Location in well day2morning', 'Features of movement day2morntrans', 'Location in well day2darkflashes', 'Night light flash and weak tap', 'Location in well day1morntrans', 'Night all weak tap', 'Features of movement day2night2', 'Location in well day1mornstim', 'Location in well day2nightstim', 'Frequency of movement day2nightstim', 'Day light flash', 'Night tap habituation', 'Features of movement day2morning', 'Frequency of movement day2morntrans', 'Location in well combo', 'Frequency of movement day1evening', 'Dark flash block 3 end', 'Day early strong tap', 'Frequency of movement day1taps', 'Day light flash and weak tap', 'Dark flash block 1 start', 'Frequency of movement day2nighttrans', 'Frequency of movement day1day', 'Location in well day1evening', 'Features of movement day1morntrans', 'Features of movement day2nightstim', 'Night all strong tap', 'Day early weak tap', 'Day all prepulse tap', 'Dark flash block 2 end', 'Features of movement day1day', 'Features of movement day1evening', 'Features of movement day2night1', 'Night all prepulse tap', 'Location in well day2nighttrans', 'Features of movement day1mornstim', 'Location in well day2morntrans', 'Features of movement day2darkflashes', 'Features of movement day2nighttrans', 'Frequency of movement combo'
			#print completedict.keys()
#	#		if title in completedict.keys():
#	#			completedict[title].append(val)
#	#		else:
#	#			completedict[title] = []
#	#			completedict[title].append(val)
			tuplelist[i].reverse()
			ordereddict = collections.OrderedDict(tuplelist[i])
			#print "TEST", completelist
			#print ordereddict
			if hasdata:
				#if len(colts) == 0:
				#	colts.append(gene)
				#	completelist.append(ordereddict)
				notinlist = True
				for l in range(0,len(colts)):
					#print l, colts[l], gene
					if colts[l] == gene:
						notinlist = False
						for k,v in completelist[l].iteritems():
							for k2,v2 in ordereddict.iteritems():
								if k == k2 and abs(float(v2)) < abs(float(v)):
									#if (abs(float(v2))) < 0.051:
									#	print "changing value", gene, k, v, v2
									completelist[l][k] = v2
				#	else:
				#		notinlist = False
						#print gene
				if notinlist:
					colts.append(gene)
					completelist.append(ordereddict)
				#completelist.append(completedict)
		#print completelist
		notrepeats = []
		for x in range(0, len(colts)):
			#print "TEST", colts[x]
			repeated = False
			for x2 in range(0, len(colts)):
				if colts[x] != colts[x2]:
					if colts[x].split("+")[0] == colts[x2].split("+")[0]:
						#print colts[x], colts[x2]
						repeated = True
					#	for k3,v3 in completelist[x].iteritems():
					#		for k4,v4 in completelist[x2].iteritems():
					#			if k3 == k4:
					#			#if k3 == k4 and abs(float(v4)) < abs(float(v3)):
					#				if (abs(float(v4))) < 0.051:
					#					completelist[x][k3] = float(v4) + 10
			if repeated == False:
				#print "Not repeated", colts[x]
				notrepeats.append(colts[x].split("+")[0])
		#print "t1", completelist[0]
		#print "t2", completelist[1]
		#print "t3", completelist[3]
		print "genes we did not repeat: ", len(notrepeats), notrepeats
		completelistnew = [v5 for i5, v5 in enumerate(completelist) if i5 not in notrepeats]
		coltsnew = [v6 for i6, v6 in enumerate(colts) if i6 not in notrepeats]
		#print completelistnew
		#print coltsnew
		uniques = []
		for c in range(0,len(coltsnew)):
			uniques.append(coltsnew[c].split("+")[0])
		uniques = set(uniques)
		uniquesl = list(uniques)
		ids = {}
		for u in range(0, len(uniquesl)):
			innerids = []
			for z in range(0, len(coltsnew)):
				if coltsnew[z].split("+")[0] == uniquesl[u]:
					innerids.append(z)
			ids[uniquesl[u]] = innerids
		#print ids
		keys = []
		for k7,v7 in completelistnew[0].iteritems():
			keys.append(k7)
		for k9,v9 in ids.iteritems():
			#for id in v9:
			#if len(v9) == 2:
			for x in keys:
				#print x, k9, v9
				morethantwocounter = 0
				morethantwolist = []
				for id in v9:
					# iterature only True if more than once
					# if hits 2 have list of all values, sort for lowest
					#if abs(float(completelistnew[v9[0]][x])) < 0.051 and abs(float(completelistnew[v9[1]][x])) < 0.051:
				#	print id, abs(float(completelistnew[id][x]))
					if abs(float(completelistnew[id][x])) < 0.051:
				#		print k9, morethantwolist
						morethantwocounter = morethantwocounter + 1
						morethantwolist.append(float(completelistnew[id][x]))
				# IF COUNTER = 1?? USE THIS TO CHECK FOR REPEATS
				if morethantwocounter > 1:
					#print k9, morethantwolist
					morethantwolist = sorted(morethantwolist, key=abs)
					#print k9, morethantwolist
					#negtest = morethantwolist[0] < 0 # Will be true if it is
					if i == 0 or i == 2:
						pos = []
						neg = []
						for n2 in range(0,len(morethantwolist)):
							if morethantwolist[n2] < 0:
								neg.append(morethantwolist[n2])
							else:
								pos.append(morethantwolist[n2])
						if len(neg) > 1 or len(pos) > 1:
							completelistnew[v9[0]][x] = morethantwolist[0]
						else:
							completelistnew[v9[0]][x] = 2.0
				# IF COUNTER = 1?? USE THIS TO CHECK FOR REPEATS
					else:
						completelistnew[v9[0]][x] = morethantwolist[0]
				else:
					completelistnew[v9[0]][x] = 2.0
			# This is for finding bad spots
			#$	if morethantwocounter == 1:
			#$		completelistnew[v9[1]][x] = 0
			#$	else:
			#$		completelistnew[v9[1]][x] = 2.0
		#print coltsnew
		for t in range(0,len(coltsnew)):
			coltsnew[t] = coltsnew[t].split("+")[0]
		#print coltsnew
		secondsets = []
		for s in range(0, len(coltsnew)):
			for s2 in range(s+1, len(coltsnew)):
				if coltsnew[s] == coltsnew[s2]:
					secondsets.append(s2)
		secondsetnew = set(secondsets)

	# NEED TO GET SECOND ONE OUT TO SEE NON-REPEAT
	#	secondsetsb = []
	#	for s in range(0, len(coltsnew)):
	#		for s2 in range(s, len(coltsnew)):
	#			if coltsnew[s] == coltsnew[s2]:
	#				secondsetsb.append(s2)
	#				secondsetsb.append(coltsnew[s2])
	#				break
	#	print secondsetsb

	#	NEED TO GET SECOND ONE OUT TO SEE NON-REPEAT
	#	secondsetsb = []
	#	for s in range(0, len(coltssecond)):
	#		for s2 in range(s, len(coltsnewb)):
	#			if coltsnewb[s] == coltsnewb[s2]:
	#				secondsetsb.append(s2)
	#				secondsetsb.append(coltsnew[s2])
	#	print secondsetsb

		coltsnewb = [v4 for i4, v4 in enumerate(coltsnew) if i4 not in secondsetnew]
		completelistnewb = [v3 for i3, v3 in enumerate(completelistnew) if i3 not in secondsetnew]
		totalgenes = set(totalgenes)
		#print "TOTALNUMBER:", len(totalgenes), sorted(totalgenes)
		for l9 in completelistnewb:
			fulldict = {}
			lowest = 2.0
			minus = []
			plus = []
			for k9,v9 in l9.iteritems():
				if abs(float(v9)) < lowest:
					lowest = float(v9)
				if abs(float(v9)) < 0.05:
					if float(v9) < 0:
						minus.append(float(v9))
					else:
						plus.append(float(v9))
			#fulldict[keylist[i]] = lowest
		#	print plus, minus, lowest, len(minus), len(plus)
			if len(plus) > len(minus) and lowest < 0:
				keydict[keylist[i]].append(lowest*-1)
		#		print "logic1"
			elif len(minus) > len(plus) and lowest > 0:
				keydict[keylist[i]].append(lowest*-1)
		#		print "logic2"
			else:
				keydict[keylist[i]].append(lowest)
		#		print "logic3"
			#fulllist.append(fulldict)
		D = pd.DataFrame(completelistnewb, index = coltsnewb)
		#D = pd.DataFrame(completelist, index = colts, columns=completelist[0].keys())
		D2 = D.T
		#SELECTING JUST THE ONES THAT HAD PHENOTYPES
		#D2.fillna(value=1)
		#D2.replace('',1.0)
		#D2[column] = D2[column].replace(r'\s+', np.nan, regex=True)
		#D2.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
		#convert_fill(D2)
		recode_empty_cells(D2, coltsnewb)
		#SELECTING JUST THE ONES THAT HAD PHENOTYPES
		D2.to_csv('AUGMAY18subsetslowavedataALL_' + str(i) + 'fixed.csv')
		D0 = D2[reppos2]
		D0.to_csv('AUGMAY18subsetslowavedatajustgoodonesdir_' + str(i) + 'fixed.csv')
		#return D2
	print keydict
	D4 = pd.DataFrame(keydict, index = coltsnewb)
	D5 = D4.T
	recode_empty_cells(D5, coltsnewb)
	D6 = D5[reppos2]
	D6 = D6.sort()
	D6.to_csv('AUGMAY18testingfinalfullgoodonesoct30nonoise.csv')
generateDF()
#print D2
#for c in range(0,len(colts)):
#	fw.write(colts[c])
#	if c < (len(colts)-1):
#		fw.write(',')
#fw.write(colts[len(colts)-1])
#fw.write('\n')
#for k in completedict.keys():
#	fw.write(k)
#	fw.write(',')
#	for v in range(0, len(completedict[k])-1):
#		fw.write(completedict[k][v])
#		if v < (len(completedict[k])-1):
#			fw.write(',')
#	fw.write('\n')
#	fw.write(completedict[len(completedict[k])-1])
