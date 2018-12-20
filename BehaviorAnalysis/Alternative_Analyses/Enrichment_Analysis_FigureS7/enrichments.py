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
import scipy.stats as stats
from scipy.stats import pearsonr
from scipy.stats import spearmanr

#Dig=pd.read_csv("all_regions_sum_nPix_perk_red_channel_PaperData_thres50_newnames.csv")
Dir=pd.read_csv("all_regions_sum_nPix_perk_green_channel_PaperData_thres50_newnames.csv")
Dig=pd.read_csv("all_regions_sum_nPix_perk_red_channel_PaperData_thres50_newnames.csv")
#Dig=pd.read_csv("all_regions_sum_perk_green_channel_PaperData_thres50_newnames.csv")
#Dig=pd.read_csv("all_regions_sum_perk_red_channel_PaperData_thres50_newnames.csv")
#Dir=pd.read_csv("all_regions_sum_perk_red_channel_PaperData_newnames.csv")
Db=pd.read_csv("MAY2018fullheatmapsetfinal_justbaseline_transposed.csv")
Db2=pd.read_csv("MAY2018fullheatmapsetfinal_justbaseline_transposed.csv")
rs=pd.read_csv("regionsizes.csv")
#Db=pd.read_csv("AUGMAY18testingfinalfullgoodonesoct30nonoise_transposed.csv")

# getting rid of all the regions that are less than 1000 in size by just making them huge (so percent won't count)
rs = rs.apply(lambda x: [y if y > 25000 else 100000000 for y in x])

Dig = Dig.divide(rs.iloc[0])
Dir = Dir.divide(rs.iloc[0])

#print Dig["Rhombencephalon"]
# getting rid of any region that is less than 1% full
Dig = Dig.apply(lambda x: [y if y > 0.01 else 0 for y in x])
Dir = Dir.apply(lambda x: [y if y > 0.01 else 0 for y in x])
#Dig.to_csv('sept142018_green_normalized_oneperc_thresh50.csv')
#Dir.to_csv('sept142018_red_normalized_oneperc_thresh50.csv')

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

#for binarizing
#Db = Db.apply(lambda x: [y if -0.05 < y < 0.05 else 1 for y in x])
#Db = Db.apply(lambda x: [y if y > 0.05 else 0 for y in x])
#negative only
Db2 = Db2.apply(lambda x: [y if -0.05 < y < 0 else 0 for y in x])
#positive only
Db = Db.apply(lambda x: [y if 0 < y < 0.05 else 0 for y in x])

Db = Db.apply(lambda x: [y if y == 0 else 1 for y in x])
Db2 = Db2.apply(lambda x: [y if y == 0 else 1 for y in x])
#Db.to_csv('sept142018_binarizedbehavior_increasedactivity.csv')
#Db2.to_csv('sept142018_binarizedbehavior_decreasedactivity.csv')
#exit()
#for column in Dig:
	#print column, rs[column]


#Db = Db.apply(lambda x: [y if y == np.nan else 1 for y in x])
#Db = Db.apply(lambda x: [y if y != np.nan else 0 for y in x])
# TRYING LOG ON P-VALUES, NOT SURE IF GOOD IDEA
#Db = Db.applymap(np.log10)
###Db = Db.apply(lambda x: [y if -0.1 < y < 0.1 else np.nan for y in x])
#print Db
#exit()

#TAble would be:
#							Has behavior, Doesn't have behavior
# Region has signal: X    Y
# Region doesn't have signal: Z   K

#altrnative, I think other is what we want
#   				Has signal   Doesn't have sigbal
# Has behavuier
# No behavior

#total should be 132
corrlist = []
for column1 in Dig:
	for column2 in Db:
		X=0
		Y=0
		Z=0
		K=0
		# requires order of genes in same in both
		indicesX = []
		digindices = list(Dig.index)
		dbindices = list(Db.index)
		for i in range(0,len(Dig[column1])):
			#print ii
	#		for ib in Db[column2]:
			for j in range(0,len(dbindices)):
				if digindices[i] == dbindices[j]:
					if Dig[column1][i] != 0 and Db[column2][j] != 0:
						indicesX.append(digindices[i])
			#if ii != 0 and ib != 0:
						X = X + 1
			#elif ii !=0 and ib == 0:
					elif Dig[column1][i] != 0 and Db[column2][j] == 0:
						Y = Y + 1
			#elif ii == 0 and ib != 0:
					elif Dig[column1][i] == 0 and Db[column2][j] != 0:
						Z = Z + 1
					else:
						K = K + 1
		#print column1, column2, X, Y, Z, K
		oddsratio, pvalue = stats.fisher_exact([[X,Y],[Z,K]], alternative='greater')
		corrlist.append((pvalue, (oddsratio, column1, column2, X, Y, Z, K, indicesX)))


#corrlist = []
#for column1 in Db:
#	for column2 in Digl:
#		corr = Db[column1].corr(Digl[column2], min_periods=6)
#		#corr = Db[column1].corr(Dig[column2], method='spearman', min_periods=7)
#		if corr > 0.6 or corr < -0.6:
#			#corrlist.append( (corr, column1, column2))
#			#newdf = pd.concat([Dig[column2], Digl[column2], Db[column1]], axis=1)
#			newdf = pd.concat([Digl[column2], Db[column1]], axis=1)
#			newdf = newdf.dropna()
#			corrlist.append( (corr, newdf))
#			#corrlist.append( (corr, column1, column2, newdf))
#			#newdf = Dig[column2].copy()
#			#newdf2 = newdf.concat(Db[column1])
#			#newdf[column1] = Db[column1]
#			#print newdf.dropna()
#			#exit()
#
corrlist.sort(key=lambda tup: tup[0])
#
for i2 in range(0, len(corrlist)):
	print corrlist[i2][0]
	print corrlist[i2][1]


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
