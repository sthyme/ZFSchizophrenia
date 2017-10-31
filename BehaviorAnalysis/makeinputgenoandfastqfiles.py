#!/usr/bin/python

import os,sys,glob,argparse,shutil

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
					"homhom":8,
					"drug":1,
					"dmso":0
				}

def make_fastqc_file(fd, fd2, date, file):
	ffile = open('fastqc_script_' + fd + "_vs_" + fd2 + '.slurm', 'w')
	ffile.write("#!/bin/bash\n")
	ffile.write("#SBATCH -p serial_requeue # Partition to submit to\n")
	ffile.write("#SBATCH -n 1 # Number of cores requested\n")
	ffile.write("#SBATCH -N 1 # Ensure that all cores are on one machine\n")
	ffile.write("#SBATCH -t 800 # Runtime in minutes\n")
	ffile.write("#SBATCH --mem=64000 # Memory per cpu in MB (see also --mem-per-cpu)\n")
	ffile.write("#SBATCH -o linearmodel_" + fd + "_vs_" + fd2 + "_%A_%a.out # Standard out goes to this file\n")
	ffile.write("#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname\n")
	ffile.write("module load Anaconda/4.3.0-fasrc01\n")
	ffile.write("cd outputfulldata_" + fd + "_vs_" + fd2 + '\n')
	os.mkdir("outputfulldata_" + fd + "_vs_" + fd2)
	ffile.write("python ../processmotiondata.py -t ")
	ffile.write("\"../testlog.timestamp1.")
	ffile.write(date)
	if os.path.isfile("finalppinight"):
		ffile.write("\" -e \"../finalppinight\" -c \"../testlog.centroid1.")
	elif os.path.isfile("finalppiassay"):
		ffile.write("\" -e \"../finalppiassay\" -c \"../testlog.centroid1.")
	elif os.path.isfile("finalseptemberfile"):
		ffile.write("\" -e \"../finalseptemberfile\" -c \"../testlog.centroid1.")
	else:
		ffile.write("\" -e \"../finalnovemberfile.txt\" -c \"../testlog.centroid1.")
	ffile.write(date)
	ffile.write("\" -d \"../testlog.motion1.")
	ffile.write(date)
	ffile.write("\" -m \"../hsmovie")
	ffile.write(date)
	ffile.write("_\" -g \"../")
	ffile.write(file)
	ffile.write("\" -s \"../sectionsfile\"")
	return 'fastqc_script_' + fd + "_vs_" + fd2 + '.slurm'

genofile = open("genotyping", 'r')
lines = genofile.readlines()
dirnames = []
iddict = {}
for line in lines:
	if line.startswith('*'):
		destdir = line.strip().split(':')[0][1:]
		type = destdir.split('_')[1]
		dirnames.append(destdir)
		ids = line.strip().split(':')[1].strip()
		iddict[type] = ids
for file1 in glob.glob('*timestamp1*'):
	date = file1.split('.')[2]
sfile = open("jobsubmission.sh", 'w')
sfile.write("#!/bin/bash\n")
for fd in dirnames:
	for fd2 in dirnames:
		if fd.split('_')[0] == fd2.split('_')[0]: # Check if same gene
			if fd != fd2:
				testfile = 'fastqc_script_' + fd + "_vs_" + fd2 + '.slurm'
				testfileo = 'fastqc_script_' + fd2 + "_vs_" + fd + '.slurm'
				if os.path.exists(testfile) or os.path.exists(testfileo):
					continue
				else:
					type1 = fd.split('_')[1]
					type2 = fd2.split('_')[1]
					if logic[type1] > logic[type2]:
						xfile = fd2 + "_vs_" + fd + "_scripted_inputgenotypeids"
						ifile = open(xfile, 'w')
						ifile.write("controlgroup:")
						ifile.write(iddict[type2])
						ifile.write("\ntestgroup:")
						ifile.write(iddict[type1])
						ifile.write("\n")
						fname2r = make_fastqc_file(fd2, fd, date, xfile)
					else:
						xfile = fd + "_vs_" + fd2 + "_scripted_inputgenotypeids"
						ifile = open(xfile, 'w')
						ifile.write("controlgroup:")
						ifile.write(iddict[type1])
						ifile.write("\ntestgroup:")
						ifile.write(iddict[type2])
						ifile.write("\n")
						fname2r = make_fastqc_file(fd, fd2, date, xfile)
					sfile.write("sbatch ")
					sfile.write(fname2r)
					sfile.write("\nsleep 5\n")

os.system("chmod +x jobsubmission.sh")
