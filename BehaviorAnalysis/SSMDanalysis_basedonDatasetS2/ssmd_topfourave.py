import glob
import math
import pandas as pd


metricdict = {}
for filea in glob.glob("finalsort*"):
	# this is the file to link metrics to 71 assays
	fileb = open(filea,'r')
	for line in fileb.readlines():
		if line.startswith("Low"):
			continue
		elif line.startswith("Average"):
			key = line.split("Average ")[1].split(":")[0]
		else:
			if key in metricdict.keys():
				metricdict[key].append(line.split(',')[0])
			else:
				metricdict[key] = []
				metricdict[key].append(line.split(',')[0])

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
		#print graph, meanwt, meanmut, varwt, varmut
		#print graph, line.split(',')[8]
		try:
			if line.split(',')[8] == '':
				#print "inif", graph, line.split(',')[8]
				try:
					ssmd = (meanwt - meanmut) / (math.sqrt(varwt + varmut))
					#print graph, ssmd
					notindict = True
					for g in genedict[gene]:
						if graph == g:
							if abs(ssmd) > abs(genedict[gene][graph]):
								genedict[gene][graph] = ssmd
							notindict = False
					if notindict:
						genedict[gene][graph] = ssmd
				except:
					print "failed, probably float division by zero: ", graph
		except:
			print "failed for some reason to do with [8]"


#	print metricdict
	finaldict = {}
	for genename in genedict.keys():
		finaldict[genename] = {}
		for graph2 in genedict[genename]:
			for m in metricdict.keys():
				for m2 in metricdict[m]:
					if m2 == graph2:
						assay = m
						#print assay, graph2
						if assay in finaldict[genename]:
							finaldict[genename][assay].append(genedict[genename][graph2])
						else:
							finaldict[genename][assay] = []
							finaldict[genename][assay].append(genedict[genename][graph2])

	#print finaldict
finalfinaldict = {}
for k,v in finaldict.iteritems():
	for v2 in v:
		#print v2
		if "Features" in v2 or "Frequency" in v2 or "Location" in v2:
			continue
			#print "skipping"
		else:
			#print v2
			incoms = finaldict[k][v2]
			#print incoms
			incoms = [incom for incom in incoms if str(incom) != 'nan']
			incoms = sorted(incoms, key = abs)
			incoms.reverse()
			#print incoms
			if abs(incoms[0]) > (3 * abs(incoms[1])):
				topfour = ( abs(incoms[4]) + abs(incoms[1]) + abs(incoms[2]) + abs(incoms[3]) ) / 4
				if incoms[1] < 0:
					topfour = topfour * -1
			else:
				topfour = ( abs(incoms[0]) + abs(incoms[1]) + abs(incoms[2]) + abs(incoms[3]) ) / 4
				if incoms[0] < 0:
					topfour = topfour * -1
			if k in finalfinaldict.keys():
				finalfinaldict[k][v2] = topfour
			else:
				finalfinaldict[k] = {}
				finalfinaldict[k][v2] = topfour
#	print finalfinaldict
#	exit()
DF = pd.DataFrame(finalfinaldict)
DF.to_csv('ssmd_stimulusonly_topfourave.csv')
