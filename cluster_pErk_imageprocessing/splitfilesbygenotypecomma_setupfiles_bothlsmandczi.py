#!/usr/bin/python

import os,sys,glob,argparse,shutil

def make_fastqc_file(fd, fd2, type):
	ffile = open('fastqc_scriptmapmap' + type + "_" + fd + "_vs_" + fd2 + '.slurm', 'w')
	ffile.write("#!/bin/bash\n")
	ffile.write("#SBATCH -p serial_requeue # Partition to submit to\n")
	ffile.write("#SBATCH -n 12 # Number of cores requested\n")
	ffile.write("#SBATCH -N 1 # Ensure that all cores are on one machine\n")
	ffile.write("#SBATCH -t 600 # Runtime in minutes\n")
	ffile.write("#SBATCH --mem=128000 # Memory per cpu in MB (see also --mem-per-cpu)\n")
	ffile.write("#SBATCH -o hostname_%A_%a.out # Standard out goes to this file\n")
	ffile.write("#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname\n")
	ffile.write("module load matlab/R2015b-fasrc01\n")
	ffile.write("matlab-default -nosplash -nodesktop -r \"MakeTheMAPMap_test")
	ffile.write(type)
	ffile.write("('")
	oscwd = os.getcwd()
	ffile.write(oscwd)
	ffile.write("/")
	ffile.write(fd)
	ffile.write("', '")
	ffile.write(oscwd)
	ffile.write("/")
	ffile.write(fd2)
	ffile.write("', '")
	ffile.write(oscwd)
	ffile.write("/")
	ffile.write(fd + "_vs_" + fd2 + "_output" + type)
	ffile.write("')")
	ffile.write('"')
	os.mkdir(fd + "_vs_" + fd2 + "_output" + type)
	return 'fastqc_scriptmapmap' + type + "_" + fd + "_vs_" + fd2 + '.slurm'

genofile = open("genotyping", 'r')
lines = genofile.readlines()
dirnames = []
check3chan = False
for line in lines:
	idstomove = []
	if line.startswith('*'):
		destdir = line.strip().split(':')[0][1:]
		#prefix = destdir.split('_')
		#outdir = prefix + "output"
		#out02dir = prefix + "output02"
		#outdirrel = prefix + "outputrelaxed"
		#out02dirrel = prefix + "output02relaxed"
		dirnames.append(destdir)
		#if not os.path.exists(str(destdir)):
		os.mkdir(str(destdir));
		idstomove = line.strip().split(':')[1].strip().split(',')
		print destdir
		print idstomove
		for i in idstomove:
			for file in glob.glob('*tiff'):
				#__p48_01_warp_
				if file.split("_warp_")[0].split('_')[-2][0] == 'p':
					id = int(file.split("_warp_")[0].split('_')[-2][1:])
				else:
					id = int(file.split("_warp_")[0].split('_')[-2][0:])
				if str(int(i)) == str(id):
					print file
					shutil.copy(file, destdir)
				#check = "_" + i + "_01_warp"
				#check2 = "_" + i + "_02_warp"
				#check3 = "_" + i + "_03_warp"
				#if check in file or check2 in file or check3 in file:
				#	print file
					###shutil.copy(file, destdir)
				if "_03_warp" in file:
				#if check3 in file:
					check3chan = True

sfile = open("jobsubmission.sh", 'w')
sfile.write("#!/bin/bash\n")
for fd in dirnames:
	for fd2 in dirnames:
		if fd.split('_')[0] == fd2.split('_')[0]: # Check if same gene
			if fd != fd2:
				testfile = 'fastqc_scriptmapmap_02_' + fd + "_vs_" + fd2 + '.slurm'
				testfileo = 'fastqc_scriptmapmap_02_' + fd2 + "_vs_" + fd + '.slurm'
				if os.path.exists(testfile) or os.path.exists(testfileo):
					continue
				else:
					fname2r = make_fastqc_file(fd, fd2, '_02_relaxed')
					sfile.write("sbatch ")
					sfile.write(fname2r)
					sfile.write("\nsleep 5\n")
					fname2 = make_fastqc_file(fd, fd2, '_02')
					sfile.write("sbatch ")
					sfile.write(fname2)
					sfile.write("\nsleep 5\n")
					if check3chan == True:
						fnamer = make_fastqc_file(fd, fd2, '_relaxed')
						sfile.write("sbatch ")
						sfile.write(fnamer)
						sfile.write("\nsleep 5\n")
						fname = make_fastqc_file(fd, fd2, '')
						sfile.write("sbatch ")
						sfile.write(fname)
						sfile.write("\nsleep 5\n")

os.system("chmod +x jobsubmission.sh")
