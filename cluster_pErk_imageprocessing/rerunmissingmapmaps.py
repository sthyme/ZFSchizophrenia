#!/usr/bin/python

import os,sys,glob,argparse,shutil


sfile = open("jobsubmission.sh", 'w')
sfile.write("#!/bin/bash\n")
for file in glob.glob("*output*"):
	if not os.listdir(file):
		print "missing: ", file
		for file2 in glob.glob("fastqc_scriptmapmap*"):
			ofile2 = open(file2, 'r')
			lines = ofile2.readlines()
			for line in lines:
				if line.split()[0] == "matlab-default":
					if file == line.split('/')[-1].split("'")[0]:
						sfile.write("sbatch ")
						sfile.write(file2)
						sfile.write("\nsleep 5\n")

os.system("chmod +x jobsubmission.sh")
