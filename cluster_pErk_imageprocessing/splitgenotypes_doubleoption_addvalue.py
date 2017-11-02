#!/usr/bin/python

import os,sys,glob,re,argparse

alphatonum = {'A': 0, 'B': 12, 'C': 24, 'D': 36, 'E': 48, 'F': 60, 'G': 72, 'H': 84, 'I':96, 'J':108, 'K':120, 'L':132, 'M': 144, 'N':156, 'O':168, 'P':180, 'Q':192}

def zipper(a,b):
	list = [a[i] + b[i] for i in range(len(a))]
	return list

gfile = open("genotyping", 'w')
for file in glob.glob('*matrix*'):
#for file in glob.glob('*matrix*'):
	f = open(file, 'r')
	line1 = f.readline()
	addvalue = 0
	if line1.split()[0] == "addvalue":
		addvalue = line1.split('=')[1]
		line2 = f.readline()
	else:
		print "ERROR! Added value line not present!"
	lines = f.readlines()
	wells = {}
	for line in lines:
		#print line.split()
		#print len(line.split())
		if len(line.split()) != 13:
			print "Either row not correct length or duplicated set, length = ", len(line.split())
			#print line.split()[1:13]
			#print line.split()[14:26]
		#	print line.split()[14:25]
		#	print line.split()[14:27]
			wells[line.split()[0]] = zipper(line.split()[1:13], line.split()[14:26])
		else:
			wells[line.split()[0]] = line.split()[1:13]
		#wells[line.split()[0]] = line.split()[1:len(line.split())]
	#print wells
	valuelist = []
	for v in wells.values():
		valuelist = valuelist + v
	valueset = set(valuelist)
	finaldata = {}
	for v2 in valueset:
		finaldata[v2] = []
	for a in wells.keys():
		#if len(wells[a]) != 12:
		#	print "ERROR, ROW NOT CORRECT LENGTH"
		for v3 in range(0, len(wells[a])):
			num = alphatonum[a] + (v3+1) + int(addvalue)
			finaldata[wells[a][v3]].append(num)
	for k in finaldata.keys():
		finaldata[k].sort()
	print file
	print finaldata
	gfile.write(file)
	gfile.write('\n')
	for key in finaldata.keys():
		title = file.split('_')[0] + "_" + key
		gfile.write(title + ": ")
		gfile.write(str(finaldata[key]).strip().strip("[").strip("]").replace(" ", ""))
		gfile.write('\n')
