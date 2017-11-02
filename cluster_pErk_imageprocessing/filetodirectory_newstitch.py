#!/usr/bin/python

#requires that you are in a directory you made called "images"

import os,sys,glob

dirs = set()
dict = {}
dictlist = []
for file in glob.glob('*nrrd'):
	pos = file.split(".")[0].split("_")[-2]
	pos = int(pos[1:len(pos)])
	dirs.add(pos)
	if pos in dict.keys():
		dict[pos].append(file)
	else:
		dictlist = [file]
		dict[pos] = dictlist
#print dict
#print dirs
for d in dirs:
	os.mkdir(str(d));
for pos in dict.keys():
	for y in dict[pos]:
		os.rename("./" + y, "./" + str(pos) + "/" + y)
