#!/usr/bin/python
import os,sys,glob,re
import numpy as np
import scipy
from scipy import stats
import datetime
import time
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors as c
from matplotlib  import cm
from scipy.stats.kde import gaussian_kde
from numpy import linspace
#from scipy.stats import nanmean
#from scipy.stats import nanmedian
import pandas as pd
import statsmodels.api as sm

# Make heatmap graph
# Still using this graph
def activity_heatmap(intensity, type):
	heatgraphname = "heatgraph_" + type +".png"
	f = open(heatgraphname + "_data", 'w')
	for x in range(0, len(intensity)):
		f.write(' '.join(str(z) for z in intensity[x]))
		f.write('\n')
	f.close()
	x = range(0,len(intensity[0])+1)
	y = range(0,len(intensity)+1)
	x,y = np.meshgrid(x,y)
	intensity = np.array(intensity)
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	ax1.pcolormesh(x,y,intensity,cmap='hot')
	plt.savefig(heatgraphname, transparent=True)
	plt.close()

# The following two functions are actually just datasavers now
def activity_ribbongraph2(array1, array2, type, xlabel, ylabel, t = None):
	ribgraphname = "ribgraph_mean_" + type + ".png"
	np.savetxt(ribgraphname + "_a1_data", np.array(array1,dtype=np.float64), delimiter = ',')
	np.savetxt(ribgraphname + "_a2_data", np.array(array2,dtype=np.float64), delimiter=',')
	if t != None:
		np.savetxt(ribgraphname + "_bincenters", np.array(t,dtype=np.float64), delimiter=',')
