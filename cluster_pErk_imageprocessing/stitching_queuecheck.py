#!/usr/bin/python

import os,sys,glob,shutil

fullset = range(1,294)
outfiles = []
completednumbers = []
queueline = []
for file in glob.glob('*02.nrrd'):
	#completednumbers.append(int(file.split('.')[0].split('_')[1]))
	completednumbers.append((int(file.split('_')[-2][1:len(file.split('_')[-2])])))
#print completednumbers
redo = [int(i) for i in fullset]
redo3 = list(set(redo).difference(completednumbers))
str1 = ""
redo3.sort()
for n in redo3:
	str1 = str1 + "," + str(n)
print str1
dirnames = []

for d in dirnames:
	print d
