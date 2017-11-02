#!/usr/bin/python

import os,sys,glob,shutil

fullset = range(1,240)
outfiles = []
completednumbers = []
queueline = []
for file in glob.glob('reformatted*/jacob*'):
	completednumbers.append(int(file.split('.')[1].split('_')[1]))
redo = [int(i) for i in fullset]
redo3 = list(set(redo).difference(completednumbers))
str1 = ""
for n in redo3:
	str1 = str1 + "," + str(n)
print str1
dirnames = []

for d in dirnames:
	print d
