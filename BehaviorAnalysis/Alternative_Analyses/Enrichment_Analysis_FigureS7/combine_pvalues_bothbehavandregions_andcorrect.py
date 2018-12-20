import scipy.stats
import numpy as np
import glob
import statsmodels.stats.multitest as smm

fourregions = ["Rhombencephalon", "Telencephalon", "Diencephalon", "Mesencephalon"]

regions = [
"Rhombencephalon___Valvula_Cerebelli",
"Rhombencephalon___Glyt2_Cluster_1",
"Rhombencephalon___Eminentia_Granularis",
"Telencephalon___Isl1_cluster_1",
"Rhombencephalon___S1181t_Cluster",
"Diencephalon___Olig2_Band",
"Rhombencephalon___Vglut2_Stripe_3",
"Rhombencephalon___Vglut2_cluster_2",
"Rhombencephalon___Gad1b_Stripe_2",
"Diencephalon___Ventral_Thalamus",
"Diencephalon___Dorsal_Thalamus",
"Rhombencephalon___Glyt2_Stripe_3",
"Rhombencephalon___Olig2_enriched_areas_in_cerebellum",
"Rhombencephalon___X_Vagus_motorneuron_cluster",
"Diencephalon___Anterior_pretectum_cluster_of_vmat2_neurons",
"Diencephalon___Diffuse_Nucleus_of_the_Intermediate_Hypothalamus",
"Diencephalon___Habenula",
"Diencephalon___Pretectum",
"Diencephalon___Olig2_Band_2",
"Diencephalon___Hypothalamus__Caudal_Hypothalamus_Neural_Cluster",
"Rhombencephalon___Vglut2_Stripe_4",
"Telencephalon___Olfactory_Bulb",
"Rhombencephalon___Neuropil_Region_2",
"Rhombencephalon___Ptf1a_Stripe",
"Diencephalon___Rostral_Hypothalamus",
"Telencephalon___Vmat2_cluster",
"Rhombencephalon___Gad1b_Stripe_3",
"Telencephalon___Subpallial_Gad1b_Cluster",
"Mesencephalon___Medial_Tectal_Band",
"Diencephalon___Posterior_Tuberculum",
"Rhombencephalon___Vmat2_Stripe_1",
"Rhombencephalon___Gad1b_Stripe_1",
"Rhombencephalon___Neuropil_Region_4",
"Diencephalon___Caudal_Hypothalamus",
"Rhombencephalon___Cerebellar__Vglut2_enriched_areas",
"Rhombencephalon___Cerebellum_Gad1b_Enriched_Areas",
"Rhombencephalon___Vglut2_Stripe_1",
"Rhombencephalon___Neuropil_Region_3",
"Telencephalon___Vglut2_rind",
"Rhombencephalon___Rhombomere_5",
"Diencephalon___Preoptic_Area",
"Rhombencephalon___Rhombomere_4",
"Telencephalon___Subpallium",
"Rhombencephalon___Rhombomere_3",
"Rhombencephalon___Corpus_Cerebelli",
"Mesencephalon___Tegmentum",
"Rhombencephalon___Rhombomere_6",
"Telencephalon___Pallium",
"Mesencephalon___Torus_Semicircularis",
"Rhombencephalon___Rhombomere_2",
"Rhombencephalon___Cerebellum",
"Diencephalon___Intermediate_Hypothalamus",
"Mesencephalon___Tectum_Neuropil",
"Rhombencephalon___Neuropil_Region_5",
"Telencephalon",
"Rhombencephalon___Rhombomere_1",
"Rhombencephalon___Rhombomere_7",
"Mesencephalon___Tectum_Stratum_Periventriculare",
"Diencephalon",
"Mesencephalon",
"Rhombencephalon"
]

dictassays = {"Features of movement": [], "Location in well":[], "Frequency of movement":[]}

for filename in glob.glob("Sept18_top61regions_onlybaseline_green_increased_greater"):
	file = open(filename, 'r')
	for line in file.readlines():
		if line.startswith('('):
			for k in dictassays.keys():
				if k in line:
					for r3 in regions:
						if line.split(',')[1].split('\'')[1] == r3:
							dictassays[k].append((line.split(',')[1], float(pval), line.split('[')[1].strip().strip(')').strip(']').split(',')))
		else:
			pval = line.strip()

for k2,v2 in dictassays.iteritems():
	print k2
	newdict = {}
	newdict2 = {}
	for tup in v2:
		if tup[0] in newdict.keys():
			newdict[tup[0].split('___')[0]].append(tup[1])
			newdict2[tup[0].split('___')[0]] = newdict2[tup[0].split('___')[0]] + tup[2]
		else:
			newdict[tup[0].split('___')[0]] = []
			newdict2[tup[0].split('___')[0]] = []
	#print newdict
	#print newdict2
	for k4,v4 in newdict2.iteritems():
		for r in range(0,len(v4)):
			newdict2[k4][r] = newdict2[k4][r].strip()
	sortinglist = []
	for k3,v3 in newdict.iteritems():
		for r2 in fourregions:
			notinset = False
			if k3.split('\'')[1] == r2:
				results = scipy.stats.combine_pvalues(v3)
				#if float(results[1]) < 0.01:
				sortinglist.append((float(results[1]), k3, set(newdict2[k3])))
	sortinglist.sort()
	#pvallist = []
	for s in sortinglist:
	#	pvallist.append(s[0])
	#rej,pval_corr = smm.fdrcorrection(pvallist)
	#for x in range(0, len(pval_corr)):
		if float(s[0]) < 0.01:
	#print pval_corr[x], sortinglist[x][0], sortinglist[x][1], sortinglist[x][2]
			print s[0], s[1], s[2]
