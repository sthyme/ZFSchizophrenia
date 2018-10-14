#!/usr/bin/python

#requires that you are in a directory you made called "images"

import os,sys,glob,shutil
import pandas as pd
import numpy as np
import collections

#Lowaverage (reg if not >3, <0.05) Location in well day2night2: 0.569
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

#completedict = {}
def generateDF():
	for i in range(0,1):
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
				gene2 = second.split('_and_')[1].split('_')[0]
				if gene1 in first:
					gene = gene1
				elif gene2 in first:
					gene = gene2
			else:
				gene = gene1
			print file, gene
			totalgenes.append(gene)
			hasdata = False
			for line in lines:
				if line.startswith("Lowaverage"):
					hasdata = True
				else:
					continue
				val = line.split(":")[1].strip()
				title = line.split(":")[0].split(")")[1].strip()
				completeddict[title] = val
			# the mapping is fine at this point
			#print completeddict
		# Make ordered set of tuples and then past to OrderedDict
			#print completeddict.keys()
			#print completeddict['Frequency of movement day1night']
			for key in allkeys:
				if key not in completeddict.keys():
			#		print "missing value: ", key, file
					completeddict[key] = '2.0'
			#print completeddict
			#try:
			tuplelist = [
			('Frequency of movement Night 1',completeddict['Frequency of movement day1night']),
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
			('Frequency of movement All',completeddict['Frequency of movement combo']),
			('Features of movement Night 1',completeddict['Features of movement day1night']),
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
			('Features of movement All',completeddict['Features of movement combo']),
			('Location in well Night 1',completeddict['Location in well day1night']),
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
			('Location in well All',completeddict['Location in well combo']),
			('Day early prepulse tap',completeddict['Day early prepulse tap']),
			('Day all prepulse tap',completeddict['Day all prepulse tap']),
			('Night early prepulse tap',completeddict['Night early prepulse tap']),
			('Night all prepulse tap',completeddict['Night all prepulse tap']),
			('Day early weak tap',completeddict['Day early weak tap']),
			('Day all weak tap',completeddict['Day all weak tap']),
			('Night early weak tap',completeddict['Night early weak tap']),
			('Night all weak tap',completeddict['Night all weak tap']),
			('Day early strong tap',completeddict['Day early strong tap']),
			('Day all strong tap',completeddict['Day all strong tap']),
			('Night early strong tap',completeddict['Night early strong tap']),
			('Night all strong tap',completeddict['Night all strong tap']),
			('Day tap habituation 1',completeddict['Day tap habituation 1']),
			('Day tap habituation 2',completeddict['Day tap habituation 2']),
			('Day tap habituation 3',completeddict['Day tap habituation 3']),
			('Night tap habituation',completeddict['Night tap habituation']),
			#('Day light flash and weak tap',completeddict['Day light flash and weak tap']),
			#('Night light flash and weak tap',completeddict['Night light flash and weak tap']),
			('Day light flash',completeddict['Day light flash']),
			('Night light flash',completeddict['Night light flash']),
			('Dark flash block 1 start',completeddict['Dark flash block 1 start']),
			('Dark flash block 1 end',completeddict['Dark flash block 1 end']),
			('Dark flash block 2 start',completeddict['Dark flash block 2 start']),
			('Dark flash block 2 end',completeddict['Dark flash block 2 end']),
			('Dark flash block 3 start',completeddict['Dark flash block 3 start']),
			('Dark flash block 3 end',completeddict['Dark flash block 3 end']),
			('Dark flash block 4 start',completeddict['Dark flash block 4 start']),
			('Dark flash block 4 end',completeddict['Dark flash block 4 end'])]
			#('Dark flash all blocks',completeddict['Dark flash all blocks'])]]
			#except:
			#	print "missing some data"
		#'Location in well day2night2', 'Location in well day2night1', 'Day all strong tap', 'Features of movement day1night', 'Frequency of movement day2heatshock', 'Day tap habituation 2', 'Day tap habituation 3', 'Dark flash block 3 start', 'Day tap habituation 1', 'Frequency of movement day2morning', 'Location in well day1taps', 'Dark flash block 2 start', 'Night early prepulse tap', 'Day all weak tap', 'Dark flash block 1 end', 'Features of movement combo', 'Frequency of movement day2night2', 'Features of movement day1taps', 'Frequency of movement day1mornstim', 'Frequency of movement day2night1', 'Frequency of movement day1morntrans', 'Night early strong tap', 'Dark flash all blocks', 'Night light flash', 'Night early weak tap', 'Frequency of movement day2darkflashes', 'Dark flash block 4 end', 'Location in well day1day', 'Location in well day2heatshock', 'Dark flash block 4 start', 'Day early prepulse tap', 'Location in well day1night', 'Frequency of movement day1night', 'Features of movement day2heatshock', 'Location in well day2morning', 'Features of movement day2morntrans', 'Location in well day2darkflashes', 'Night light flash and weak tap', 'Location in well day1morntrans', 'Night all weak tap', 'Features of movement day2night2', 'Location in well day1mornstim', 'Location in well day2nightstim', 'Frequency of movement day2nightstim', 'Day light flash', 'Night tap habituation', 'Features of movement day2morning', 'Frequency of movement day2morntrans', 'Location in well combo', 'Frequency of movement day1evening', 'Dark flash block 3 end', 'Day early strong tap', 'Frequency of movement day1taps', 'Day light flash and weak tap', 'Dark flash block 1 start', 'Frequency of movement day2nighttrans', 'Frequency of movement day1day', 'Location in well day1evening', 'Features of movement day1morntrans', 'Features of movement day2nightstim', 'Night all strong tap', 'Day early weak tap', 'Day all prepulse tap', 'Dark flash block 2 end', 'Features of movement day1day', 'Features of movement day1evening', 'Features of movement day2night1', 'Night all prepulse tap', 'Location in well day2nighttrans', 'Features of movement day1mornstim', 'Location in well day2morntrans', 'Features of movement day2darkflashes', 'Features of movement day2nighttrans', 'Frequency of movement combo'
			#print completedict.keys()
#	#		if title in completedict.keys():
#	#			completedict[title].append(val)
#	#		else:
#	#			completedict[title] = []
#	#			completedict[title].append(val)
			tuplelist.reverse()
			ordereddict = collections.OrderedDict(tuplelist)
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
									# don't need to see this for debugging
									#if (abs(float(v2))) < 0.051:
										#print "changing value", gene, k, v, v2
									completelist[l][k] = v2
				#	else:
				#		notinlist = False
						#print gene
				if notinlist:
					colts.append(gene)
					completelist.append(ordereddict)
				#completelist.append(completedict)

		#ASSAY COUNTING SECTION
		for i2 in range(0,len(colts)):
			num = 0
			for j in completelist[i2].values():
			#	print j
				if abs(float(j)) < 0.05:
					num = num+1
			print colts[i2],num
		totalgenes = set(totalgenes)
		#

		print "TOTALNUMBER:", len(totalgenes), sorted(totalgenes)
		D = pd.DataFrame(completelist, index = colts)
		D = D.sort()
		#D = pd.DataFrame(completelist, index = colts, columns=completelist[0].keys())
		D2 = D.T
		#D2.fillna(value=1)
		#D2.replace('',1.0)
		#D2[column] = D2[column].replace(r'\s+', np.nan, regex=True)
		#D2.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
		#convert_fill(D2)
		recode_empty_cells(D2, colts)
		D2.to_csv('TESTnotrealMAY2018fullheatmapsetfinal_' + str(i) + '.csv')
		#return D2
	#generateDF()
#	print D2
generateDF()
