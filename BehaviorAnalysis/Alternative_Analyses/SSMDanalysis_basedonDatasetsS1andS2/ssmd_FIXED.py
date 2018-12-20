import glob
import math
import pandas as pd

genedict = {}
for file1 in glob.glob('stats*csv'):
	if "and" in file1.split('out_')[1]:
		gene1 = file1.split('out_')[1].split('_')[0]
		gene2 = file1.split('out_')[1].split('and_')[1].split('_')[0]
		if gene1 in file1.split('out_')[0]:
			gene = gene1
		elif gene2 in file1.split('out_')[0]:
			gene = gene2
		else:
			print "PROBLEM - CANT FIND OUT WHICH GENE ", file1
	else:
		gene = file1.split('out_')[1].split('_')[0]
	print file1, gene
	if gene not in genedict.keys():
		genedict[gene] = {}
	file2 = open(file1,'r')
	for line in file2.readlines():
		if line.startswith('graph'):
			continue
		graph = line.split(',')[0]
		meanwt = float(line.split(',')[1])
		meanmut = float(line.split(',')[2])
		varwt = float(line.split(',')[3])
		varmut = float(line.split(',')[4])
		try:
			kpval = float(line.split(',')[7])
		except:
			continue
		#print graph, meanwt, meanmut, varwt, varmut, kpval
		#print graph, line.split(',')[8]
		try:
			if line.split(',')[8] == '':
				#print "inif", graph, line.split(',')[8]
				try:
					ssmd = (meanwt - meanmut) / (math.sqrt(varwt + varmut))
					#print graph, ssmd
					notindict = True
					for g in genedict[gene]:
						#print graph, g
						if graph == g:
							if abs(ssmd) > abs(genedict[gene][graph]):
								#if kpval < 0.05:
								genedict[gene][graph] = ssmd
							notindict = False
					if notindict:
						#if kpval < 0.05:
						genedict[gene][graph] = ssmd
						#else:
						#	genedict[gene][graph] = 0
				except:
					print "failed, probably float division by zero: ", graph
		except:
			print "failed for some reason to do with [8]"
DF = pd.DataFrame(genedict)
DF.to_csv('ssmd_stimulusonly_FIXED.csv')
#	print genedict
#	exit()
