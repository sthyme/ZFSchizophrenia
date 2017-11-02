#!/usr/bin/python

#requires that you are in a directory you made called "images"

import os,sys,glob,shutil

dirs = [d for d in os.listdir('../../smoothedtiffs/onlysmoothedtiffs') if os.path.isdir(os.path.join('../../smoothedtiffs/onlysmoothedtiffs', d))]
outputdirs = []
genodirs = []

for d2 in dirs:
	if "relaxed" not in d2.lower():
		if "output_02" in d2.lower():
			outputdirs.append(d2)
		elif "output" not in d2.lower():
			genodirs.append(d2)

print outputdirs
print genodirs

dirnames = []
sfile = open("jobsubmission.sh", 'w')
sfile.write("#!/bin/bash\n")

for od in outputdirs:
	oood = od[:-2] + "jacobian"
	print "oood: ", oood
	ood = os.path.dirname(str(oood))
	if not os.path.exists(ood):
		try:
			os.mkdir(str(oood))
		except:
			print ""
	#znf536_hetandwt_vs_znf536_hom_output_jacobian
	genodir1 = oood.split("_")[0] + "_" + oood.split("_")[1]
	genodir2 = oood.split("_")[3] + "_" + oood.split("_")[4]
	if genodir1 not in genodirs:
		print "ERROR, CAN'T FIND THE GENODIR 1: ", genodir1
		break
	if genodir2 not in genodirs:
		if (genodir2.split("-")[0] + genodir2.split("-")) in genodirs:
			genodir2 = genodir2.split("-")[0] + genodir2.split("-")
		else:
			print "ERROR, CAN'T FIND THE GENODIR 2, EVEN AFTER - CONSIDERATION: ", genodir2
			break
	gd1 = os.path.dirname(os.path.abspath(str(genodir1))) + "/" + genodir1
	gd2 = os.path.dirname(os.path.abspath(str(genodir2))) + "/" + genodir2
#	print "gd1: ", gd1
#	print "gd2: ", gd2
	if not os.path.exists(gd1):
		os.mkdir(str(genodir1));
		files1 = os.listdir('../../smoothedtiffs/onlysmoothedtiffs/' + genodir1)
		for f in files1:
			if f.split("_warp_")[0].split('_')[-2][0] == 'p':
				id = int(f.split("_warp_")[0].split('_')[-2][1:])
			else:
				id = int(f.split("_warp_")[0].split('_')[-2][0:])
			if "01_warp" in f:
				shutil.copy('../../smoothedtiffs/onlysmoothedtiffs/'+genodir1+"/"+f, genodir1)
			for jfile in glob.glob('*tiff'):
				#jacobian_2.nrrdGauSmooth.tiff
				if str(id) == jfile.split(".")[0].split("_")[1]:
					shutil.copy(jfile, genodir1)
	if not os.path.exists(gd2):
		os.mkdir(str(genodir2));
		files2 = os.listdir('../../smoothedtiffs/onlysmoothedtiffs/' + genodir2)
		for f2 in files2:
			if f2.split("_warp_")[0].split('_')[-2][0] == 'p':
				id = int(f2.split("_warp_")[0].split('_')[-2][1:])
			else:
				id = int(f2.split("_warp_")[0].split('_')[-2][0:])
			if "01_warp" in f2:
				shutil.copy('../../smoothedtiffs/onlysmoothedtiffs/'+genodir2+"/"+f2, genodir2)
			for jfile in glob.glob('*tiff'):
				if str(id) == jfile.split(".")[0].split("_")[1]:
					shutil.copy(jfile, genodir2)
	fname2r = 'fastqc_jacobian_' + str(genodir1) + "_vs_" + str(genodir2) + '.slurm'
	ffile = open(fname2r, 'w')
	sfile.write("sbatch ")
	sfile.write(fname2r)
	sfile.write("\nsleep 5\n")
	ffile.write("#!/bin/bash\n")
	ffile.write("#SBATCH -p serial_requeue # Partition to submit to\n")
	ffile.write("#SBATCH -n 12 # Number of cores requested\n")
	ffile.write("#SBATCH -N 1 # Ensure that all cores are on one machine\n")
	ffile.write("#SBATCH -t 600 # Runtime in minutes\n")
	ffile.write("#SBATCH --mem=128000 # Memory per cpu in MB (see also --mem-per-cpu)\n")
	ffile.write("#SBATCH -o hostname_%A_%a.out # Standard out goes to this file\n")
	ffile.write("#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname\n")
	ffile.write("module load matlab/R2015b-fasrc01\n")
	ffile.write("matlab-default -nosplash -nodesktop -r \"MakeTheMAPMap_test_jacobian_noErk('")
	oscwd = os.getcwd()
	ffile.write(oscwd)
	ffile.write("/")
	ffile.write(str(genodir1))
	ffile.write("', '")
	ffile.write(oscwd)
	ffile.write("/")
	ffile.write(str(genodir2))
	ffile.write("', '")
	ffile.write(oscwd)
	ffile.write("/")
	ffile.write(str(oood))
	ffile.write("')")
	ffile.write('"')

os.system("chmod +x jobsubmission.sh")
