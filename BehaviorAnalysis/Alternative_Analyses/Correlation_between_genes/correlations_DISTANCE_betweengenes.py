import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import matplotlib.colors as mat_col
from matplotlib.colors import LinearSegmentedColormap
import scipy
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import set_link_color_palette
import numpy as np
import pandas as pd
import glob
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.spatial import distance

#Dig=pd.read_csv("all_regions_sum_nPix_perk_red_channel_PaperData_thres50_newnames.csv")
#Dig=pd.read_csv("all_regions_sum_nPix_perk_green_channel_PaperData_thres50_newnames.csv")
#Dig=pd.read_csv("all_regions_sum_perk_red_channel_PaperData_thres50_newnames.csv")
#Dir=pd.read_csv("all_regions_sum_perk_red_channel_PaperData_newnames.csv")
#Db=pd.read_csv("MAYbehaviorfullset_transposed.csv")
Db=pd.read_csv("AUG16_12_dectest.csv")
#Db=pd.read_csv("AUGMAY18testingfinalfullgoodonesoct30nonoise_transposed.csv")

#Dig = Dig.applymap(np.log)
#Digl = Dig # use if skipping log10
#Digl = Dig.applymap(np.log10)

#print Dig
#Digl = Digl.replace([np.inf, -np.inf], 0)
#Digl = Digl.replace([np.inf, -np.inf], np.nan)

# use if not doing log10
#Digl = Digl.replace([0], np.nan)

#Dig = Dig.replace([0], np.nan)
#DignoNA = Dig.dropna()

#Db = Db.apply(lambda x: [y if 0 < y < 0.05 else np.nan for y in x])
#Db = Db.apply(lambda x: [y if -0.05 < y < 0 else np.nan for y in x])

#print Db["adamtsl3"]
#for binarizing
# DEC 2018, THIS BINARIZING WORKS, BUT NOT DOIN GIT
# only binarizing the "non-significant" data
Db = Db.apply(lambda x: [y if -0.05 < y < 0.05 else 1 for y in x])
# convert all non-significant values to large number
##Db = Db.apply(lambda x: [y if -0.05 < y < 0.05 else 5 for y in x])
#print Db["adamtsl3"]
# keep all positive values, everything negative (between 0 and -0.05) becomes -1
##Db = Db.apply(lambda x: [y if y > 0 else -1 for y in x])
#print Db["adamtsl3"]
##Db = Db.apply(lambda x: [y if y < 2 else 0 for y in x])
#print Db["adamtsl3"]
# everything that is negative or 0 stays the same, everything else (between 0 and 0.05) becomes 1
##Db = Db.apply(lambda x: [y if y <= 0 else 1 for y in x])
#print Db["adamtsl3"]

#Db = Db.apply(lambda x: [y if y == np.nan else 1 for y in x])
#Db = Db.apply(lambda x: [y if y != np.nan else 0 for y in x])
# TRYING LOG ON P-VALUES, NOT SURE IF GOOD IDEA
#Db = Db.applymap(np.log10)
###Db = Db.apply(lambda x: [y if -0.1 < y < 0.1 else np.nan for y in x])
#print Db
#exit()

corrlist = []
dfdict = {}
dfdictdist = {}
collist = []
for column1 in Db:
	for column2 in Db:
		corr = Db[column1].corr(Db[column2], min_periods=6)
	#	dist = np.square(Db[column1] - Db[column2])
	#	print dist
		dist = distance.euclidean(Db[column1], Db[column2])
#		print dist
		#corr = Db[column1].corr(Dig[column2], method='spearman', min_periods=7)
	#	if corr > 0.6 or corr < -0.6:
			#corrlist.append( (corr, column1, column2))
			#newdf = pd.concat([Dig[column2], Digl[column2], Db[column1]], axis=1)
		newdf = pd.concat([Db[column2], Db[column1]], axis=1)
	#		newdf = newdf.dropna()
		corrlist.append( (corr, newdf, column1, column2, dist))
		if column1 in dfdict.keys():
			dfdict[column1].append(corr)
			dfdictdist[column1].append(dist)
		else:
			dfdict[column1] = []
			dfdictdist[column1] = []
			dfdict[column1].append(corr)
			dfdictdist[column1].append(dist)
		if column2 not in collist:
			collist.append(column2)
			#corrlist.append( (corr, column1, column2, newdf))
			#newdf = Dig[column2].copy()
			#newdf2 = newdf.concat(Db[column1])
			#newdf[column1] = Db[column1]
			#print newdf.dropna()
			#exit()
	#	break
	#break

#print dfdict
#print dfdictdist
#print collist

dfcor = pd.DataFrame.from_dict(dfdict, orient='index')
dfcor.columns = collist
dfdist = pd.DataFrame.from_dict(dfdictdist, orient='index')
dfdist.columns = collist

dfcor = dfcor.sort_index()
dfdist = dfdist.sort_index()

dfcor.to_csv("dec_correlation_sort1.csv")
dfdist.to_csv("dec_distance_sort1.csv")

#print dfcor

#corrlist.sort(key=lambda tup: tup[0])

#old way of just printing before generate the DF
##for i in range(0, len(corrlist)):
##	print corrlist[i][0], corrlist[i][4], corrlist[i][2], corrlist[i][3]
	#print corrlist[i][1]
	#print corrlist[i][2]


#Db=pd.read_csv("MAY2018fullheatmapsetfinal_0.csv")
#Db = Db.transpose()
#Dig = Dig.values
#Dir = Dir.values
#Db = Db.values

#print "test1"
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#	print Dig
#print "test2"
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#	print Db
#Digb = Dig[:,1:]
#Dirb = Dir[:,1:]
#Digb = np.delete(Dig, 0, axis=1)
#Dbb = Db[:,1:]
#Dbb = np.delete(Db, 0, axis=1)

#Digb = np.log(Digb)

#Digb = Dig.values
#Dbb = Db.values

#print "test1"
#print Dbb
#print "test2"
#print Digb

#print np.shape(Dbb)
#print np.shape(Digb)

#for row in range(Digb.shape[0]):
 #print str(pearsonr(Dbb[row,:], Digb[row,:]))
 #print str(pearsonr(Dbb[:,row], Digb[:,row]))

#spearlist = []
#print "green correlation"
#for column1 in Digb.T:
#	for column2 in Dbb.T:
#		spearlist.append(str(spearmanr(column1, column2, nan_policy='omit')))

#spearlist.sort()
#for s in spearlist:
#	print s

#print "red correlation"
#for column3 in Dirb.T:
#	for column4 in Dbb.T:
#		print str(pearsonr(column3, column4))



#for column1 in Dig:
#	for column2 in Db:
#		print column1.corr


#print "green correlation"

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	#print Dig.corrwith(Db.set_axis(Dig.columns, axis='columns', inplace=False))
	#print Dig.corrwith(Db)
#print "red correlation"
#Dir.corrwith(Db)
