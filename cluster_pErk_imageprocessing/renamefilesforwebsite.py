#!/usr/bin/python

import os,sys,glob,argparse,shutil

parser = argparse.ArgumentParser(description='argumentsforfilerename')

parser.add_argument('-run', type=str, action="store", dest = "run")
parser.add_argument('-xtype', type=str, action="store", dest = "xtype")
parser.add_argument('-gene', type=str, action="store", dest = "gene")

args = parser.parse_args()

run = args.run
xtype = args.xtype
gene = args.gene

logic = { "wt":0,
					"wtwt":0,
					"hetwt":2,
					"wthet":1,
					"wtandhet":1,
					"hetandwt":1,
					"hethet":3,
					"het":3,
					"homwt":5,
					"wthom":4,
					"hethom":6,
					"homhet":7,
					"hom":7,
					"homhom":8
				}


#./renamefilesforwebsite.py -run 1st -xtype hethomfxhomhetm -gene ep300

#ep300hethomxhomhet_homhet_vs_ep300hethomxhomhet_hethom_output_02_relaxed
for name in glob.glob(gene + '*output*'):
	print "dir: ", name
	for sigfile in glob.glob1(name, '*SignificantDeltaMedians*'):
		print "file: ", sigfile
		overtype = sigfile.split('_')[1]
		info = name.split('_')
		vssplit = name.split('vs')
		outsplit = name.split('output')
		#print vssplit[0].split('_'), outsplit[0].split('_')
		firstgeno = vssplit[0].split('_')[-2]
		secgeno = outsplit[0].split('_')[-2]
		if logic[firstgeno] > logic[secgeno]:
			first = True
		else:
			first = False
		#print "first and second: ", firstgeno, secgeno
		type = ""
		pval = ""
		if info[-1] == 'relaxed':
			pval = "p0005"
			if info[-2] == "02":
				type = "pErk"
			else:
				type = "znp1"
		else:
			pval = "p00005"
			if info[-1] == "02":
				type = "pErk"
			elif info[-1] == "output":
				type = "znp1"
		for name2 in glob.glob(gene + '*'):
			if "output" in name2:
				continue
			if "matrix" in name2:
				continue
			#print name2
			geno2 = name2.split('_')[-1]
			#print "geno2", geno2, firstgeno, secgeno
			if firstgeno == geno2:
				tifCounter1 = len(glob.glob1(name2,"*_01_warp_*"))
				#print "t: ", tifCounter
			elif secgeno == geno2:
				tifCounter2 = len(glob.glob1(name2,"*_01_warp_*"))
				#print "t2: ", tifCounter
		if overtype == firstgeno:
			newname = gene + "_" + type + "_" + str(tifCounter1) + firstgeno + "over" + str(tifCounter2) + secgeno + "_" + xtype + "_" + run + "_" + pval + ".tif"
			if first == True:
				shutil.copy(name + "/" + sigfile, '/n/schierfs2/projects/ImageRegistration/data/sthyme/mapfilesforwebsite/'+ newname)
				print "newname: ", newname
		elif overtype == secgeno:
			newname = gene + "_" + type + "_" + str(tifCounter2) + secgeno + "over" + str(tifCounter1) + firstgeno + "_" + xtype + "_" + run + "_" + pval + ".tif"
			if first == False:
				shutil.copy(name + "/" + sigfile, '/n/schierfs2/projects/ImageRegistration/data/sthyme/mapfilesforwebsite/'+ newname)
				print "newname: ", newname
		#shutil.copy(name + "/" + sigfile, '/n/schierfs2/projects/ImageRegistration/data/sthyme/mapfilesforwebsite/'+ newname)
