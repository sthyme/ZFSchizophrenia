#!/usr/bin/python

import os,sys,glob,argparse,shutil

parser = argparse.ArgumentParser(description='argumentsforfilerename')

parser.add_argument('-run', type=str, action="store", dest = "run")
parser.add_argument('-xtype', type=str, action="store", dest = "xtype")
parser.add_argument('-gene', type=str, action="store", dest = "gene")

args = parser.parse_args()

for name in glob.glob('*output*'):
	print "dir: ", name
	shortdir = name.split("_")
	newname0 = "_".join(shortdir[0:-1]) + "_02"
	#print newname0
	for file in glob.glob("../../smooth*/onlysmoo*/namingnote*"):
		print file
		filer = open(file, 'r')
		test = False
		for line in filer.readlines():
			#print line
			if line.split()[1] == newname0:
				#print "**", line
				test = True
			if test == True and line.split(":")[0] == "newname":
				#print "*****", line
				#print "********", lastline
				newname1 = line.split()[1]
				newname = newname1.replace("pErk", "structure")
				sigfile = lastline.split()[1]
				print newname0, ", ", sigfile, ", ", newname
				shutil.copy(name + "/" + sigfile, '/n/schierfs2/projects/ImageRegistration/data/sthyme/structuremaps/'+ newname)
				break
			lastline = line



		#if overtype == firstgeno:
		#	newname = gene + "_" + type + "_" + str(tifCounter1) + firstgeno + "over" + str(tifCounter2) + secgeno + "_" + xtype + "_" + run + "_" + pval + ".tif"
		#	if first == True:
		#		shutil.copy(name + "/" + sigfile, '/n/schierfs2/projects/ImageRegistration/data/sthyme/structuremaps/'+ newname)
		#		print "newname: ", newname
		#elif overtype == secgeno:
		#	newname = gene + "_" + type + "_" + str(tifCounter2) + secgeno + "over" + str(tifCounter1) + firstgeno + "_" + xtype + "_" + run + "_" + pval + ".tif"
		#	if first == False:
		#		shutil.copy(name + "/" + sigfile, '/n/schierfs2/projects/ImageRegistration/data/sthyme/mapfilesforwebsite/'+ newname)
		#		print "newname: ", newname
