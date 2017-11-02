#!/usr/bin/python

import os,sys,glob,shutil

fullset = range(1,198)
outfiles = []
completednumbers = []
queueline = []
for file in glob.glob('*.nrrdGauSmooth.tiff'):
	completednumbers.append(int(file.split('.')[0].split('_')[1]))
redo = [int(i) for i in fullset]
redo3 = list(set(redo).difference(completednumbers))
str1 = ""
for n in redo3:
	str1 = str1 + "," + str(n)
print str1
dirnames = []

for d in dirnames:
	print d
