#!/usr/bin/python

import os,sys,glob,shutil

fullset = []
for d in glob.glob("images/*"):
	ds = d.split('/')
	if len(ds) > 1:
		if not ds[1].startswith("file"):
			if not ds[1].startswith("new"):
				fullset.append(int(ds[1]))
#print fullset
#backupfullset = range(1,50)
#dirset = [x[0] for x in os.walk("images")]
#for d in dirset:
#	ds = d.split('/')
#	if len(ds) > 1:
#		fullset.append(int(ds[1]))
#print fullset
outfiles = []
completednumbers = []
queueline = []
for file in glob.glob('reformatted*/*/*02*nrrd'):
	completednumbers.append(int((file.split('_')[-4])[1:len(file.split('_')[-4])]))
for file in glob.glob('queuelist'):
	for line in open(file, 'r'):
		queueline.append("hostname_" + line.split()[0])
for file in glob.glob('*out'):
	outfiles.append(int(file.split('.')[0]))

stillrunning = []
for x in queueline:
	for z in outfiles:
		if x == z:
#			print x, z
			stillrunning.append(int(z.split('_')[2]))
redo = [int(i) for i in fullset]
#print redo
#print stillrunning
redo2 = list(set(redo).difference(stillrunning))
redo3 = list(set(redo2).difference(completednumbers))
#print redo2
#print redo3
for file in glob.glob('reformatted*/*/*lock'):
	redo3.append(int((file.split('_')[-4])[1:len(file.split('_')[-4])]))
str1 = ""
for n in redo3:
	str1 = str1 + "," + str(n)
print str1
dirnames = []
for r in redo3:
	name = "Registration."+str(r)
	dirnames.append(name)
	name2 = "reformatted."+str(r)
	dirnames.append(name2)

for d in dirnames:
	print d
	shutil.rmtree(d,ignore_errors=True)

#notrunning = []
#for y in fullset:
#	for y2 in stillrunning:
#		#print y, y2.split('_')[2]
#		if str(y) == y2.split('_')[2]:
#			continue
#		notrunning.append(str(y))
#print notrunning
#for r in notrunning:
#	for r2 in completednumbers:
#		if str(r) == str(r2):
#			#print r, r2
#			continue
#		redo.append(r)

#print redo
