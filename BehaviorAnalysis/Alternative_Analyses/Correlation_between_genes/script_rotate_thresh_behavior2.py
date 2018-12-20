import numpy as np
import dill
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import os
import skimage.external
from skimage.external import tifffile

def save_object(obj, filename,verbose=False):
    f = open(filename, "wb")
    if verbose:
        print("Opened file.")
    dill.dump(obj, f)
    if verbose:
        print("Dumped to file.")
    f.close()
    return

def load_object(filename):
    f = open(filename, "rb")
    obj = dill.load(f)
    f.close()
    return obj

#print ("test")

import scipy
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import set_link_color_palette
import matplotlib.colors as mat_col
def my_clustermap(matrix,thrs_row=1,thrs_col=1,distM=None,row_cls=False,col_cls=True,return_fig=False,method='average',fig_sz=(8,8),colnames=None, rownames=None,cls_info=False):
    colors=sns.color_palette("Set2", 25)
    colors=[mat_col.rgb2hex(color) for color in colors]
    set_link_color_palette(colors)
    #print ("testing")
    if colnames is None:
        try:
            colnames=np.array(matrix.columns,str)
        except AttributeError:
            colnames=np.array(range(0,matrix.shape[1]),str)
    if rownames is None:
        try:
            rownames=np.array(matrix.index,str)
        except AttributeError:
            rownames=np.array(range(0,matrix.shape[0]),str)
    if row_cls:
        if distM is None:
            D_row=scipy.spatial.distance.pdist(matrix)
        else:
            D_row=distM
    if col_cls:
        if distM is None:
            D_col=scipy.spatial.distance.pdist(matrix.T)
        else:
            D_col=distM
    #print ("testing")
    fig=plt.figure(figsize=fig_sz)
    #print ("testing2")
    lef=0.01
    bot=0.05
    h_sep=0.2
    v_sep=0.7
    row_leg=0.01 #space for the legend of the rows plotted on the right side of the matrix
    #print ("test")
    if row_cls:
        if col_cls: #if want both row and column dendrogram
            mat_h=v_sep-0.005-bot
            mat_w=0.9-row_leg-h_sep
            den_h=1-v_sep-0.005
            den_w=h_sep-0.005-lef
            #plot dendrogram for column clusters
            ax_col=fig.add_axes([h_sep,v_sep,mat_w,den_h])
            g_col=scipy.cluster.hierarchy.linkage(D_col,method=method)
            den_col=scipy.cluster.hierarchy.dendrogram(g_col,color_threshold=thrs_col,above_threshold_color='black')
            idx_col = den_col['leaves']
            ax_col.set_xticklabels([''])
        else: #if only want row dendrogram
            mat_h=1-bot*2
            mat_w=0.9-0.01-h_sep
            den_w=h_sep-0.005-lef
            idx_col=list(range(0,matrix.shape[1]))

        # plot dendrogram for row clusters
        ax_row=fig.add_axes([lef,bot,den_w,mat_h])
        g_row=scipy.cluster.hierarchy.linkage(D_row,method=method)
        den_row=scipy.cluster.hierarchy.dendrogram(g_row,color_threshold=thrs_row,orientation='left',above_threshold_color='black')
        idx_row = den_row['leaves']
        ax_row.set_yticklabels([''])
        ax_mat = fig.add_axes([h_sep,bot,mat_w,mat_h])

    else:
        if col_cls: #if only want column clusters
            lef=lef+0.04
            mat_h=v_sep-0.005-bot
            mat_w=0.9-row_leg-lef
            den_h=1-v_sep-0.005
        else:
            plt.close()
            raise ValueError("At least one of row_cls and col_cls has to be Ture.")

        #plot dendrogram for column clusters
        ax_col=fig.add_axes([lef,v_sep,mat_w,den_h])
        g_col=scipy.cluster.hierarchy.linkage(D_col,method=method)
        den_col=scipy.cluster.hierarchy.dendrogram(g_col,color_threshold=thrs_col,above_threshold_color='black')
        idx_col = den_col['leaves']
        idx_row=list(range(0,matrix.shape[0]))
        ax_col.set_xticklabels([''])
        ax_mat = fig.add_axes([lef,bot,mat_w,mat_h])
    #plot data matrix as a heatmap
    #print (matrix.index)
    #matrix.loc['znf536','clcn3','tcf4','cnnm2','akt3b','foxg1het','foxg1','snap91','kmt2e']
    #matrix.loc[['gria1','znf536','clcn3','tcf4','cnnm2','akt3b','foxg1het','foxg1','snap91','kmt2e'],['gria1','znf536','clcn3','tcf4','cnnm2','akt3b','foxg1het','foxg1','snap91','kmt2e']]
    matrix=np.array(matrix)
    matrix2 = np.array(matrix)
    matrix2[matrix2 > 0.9999] = np.nan
    maxval = np.nanmax(matrix2)
   # maxval2 = np.nanmax(matrix)
    D = matrix[idx_row,:]
    D = D[:,idx_col]
    D2 = np.rot90(D)
    #print (D2)
    #D3 = np.rot90(D2)
    #print (D3)
    #print (colnames[idx_col])
    #print (rownames[idx_row])
    revlist = np.flipud(colnames[idx_col])
    #print (maxval, maxval2)
    #im = ax_mat.matshow(D, aspect='auto', origin='lower', cmap=plt.cm.YlGnBu)
    im = ax_mat.pcolormesh(D2,cmap=plt.cm.YlGnBu, vmin=0, vmax=maxval)
    ax_mat.xaxis.set_ticks_position('bottom')
    ax_mat.yaxis.set_ticks_position('right')
    ax_mat.set_xticks(list(np.asarray(list(range(0,matrix.shape[1])))+0.5))
    ax_mat.set_yticks(list(np.asarray(list(range(0,matrix.shape[0])))+0.5))
    #ax_mat.set_xticks(list(range(0,matrix.shape[1])+0.05))
    #ax_mat.set_yticks(list(range(0,matrix.shape[0])+0.05))
    ax_mat.set_xticklabels(colnames[idx_col],rotation=90,size=4)
    #ax_mat.set_xticklabels(colnames[idx_col],rotation=90,size=4)
    #ax_mat.set_yticklabels(rownames[idx_row],size=4)
    ax_mat.set_yticklabels(revlist,size=4)
    ax_mat.grid(False)

    # Plot colorbar.
    axcolor = fig.add_axes([0.94,bot,0.02,mat_h])
    plt.colorbar(im, cax=axcolor)
    axcolor = fig.add_axes([0.94,bot,0.02,mat_h])
    plt.colorbar(im, cax=axcolor)
    #namepre = fname.split(".")[0]
  #  if row_cls:
	#		namepre = namepre + "rows_"
    plt.savefig("Dec_corr_nonegs_sort1_"+method+".png",bbox_inches='tight', dpi=600)
    #plt.savefig(namepre+method+".png",bbox_inches='tight', dpi=600)
    if cls_info:
        cls_dic={}
        if col_cls:
            cls_dic['col_ind']=den_col['leaves']
            cls_dic['col_cls']=scipy.cluster.hierarchy.fcluster(g_col,t=thrs_col,criterion='distance')
        if row_cls:
            cls_dic['row_ind']=den_row['leaves']
            cls_dic['row_cls']=scipy.cluster.hierarchy.fcluster(g_row,t=thrs_row,criterion='distance')
        return(cls_dic)

#result=load_object('./cleanfusedperk_overlap')
#result.keys()

M=pd.read_csv("dec_correlation_sort1.csv")
#M=result['R&G'] ## Change to result['R'] or result['G'] to cluster on result calculated from the two channels separately
labels=[file.split('_')[0] for file in M.index] ## the columns and row names of the saved dataframe is the tif file names, this line extract only the gene name for labeling the plot
#print (M)
dict = {}
for x in range(0,len(M.index)):
	dict[M.index[x]] = labels[x]
#print (dict)
M = M.rename(columns=dict)
M = M.rename(index=dict)
#M = M.reindex(index=np.array(labels), columns=np.array(labels))
#M.reindex(index=labels, columns=labels)
#print (M)
#M = (np.log(M+1))
#M.loc[['gria1','znf536','clcn3','tcf4','cnnm2','akt3b','foxg1het','foxg1','snap91','kmt2e'],['gria1','znf536','clcn3','tcf4','cnnm2','akt3b','foxg1het','foxg1','snap91','kmt2e']]
#M = M.loc[['gria1','znf536','clcn3','tcf4','cnnm2','akt3b','foxg1het','foxg1','snap91','kmt2e'],['gria1','znf536','clcn3','tcf4','cnnm2','akt3b','foxg1het','foxg1','snap91','kmt2e']]

#print (M)
#exit()

#M = M.loc[["klc1","gria1","c2orf82","nrgn","fam5b","gatad2ab","nck1","atxn7","grm3","fut9a","fes","galnt10","anp32e","gramd1b","slc35g2","tsnare1","snx19","plcl1","c12orf65","sipa1l1","ep300","dgkz","tle1","bag5","gpm6a","tbc1d5","shisa9","mdk","negr1","mir137","pak6","cntn4","ca8","man2a1","kcnj13","tcf20","csmd1","stat6","vrk2","egr1","cacna1c","cnksr2","satb1","hcn1","chst12","c2orf69","foxg1het","lrp1","arhgap1","rora","arl3","ckb","fpgt","znf536","grin2a","cnnm2","luzp2","elfn1","bcl11b","tcf4","mad1l1","tle3","kmt2e","clcn3","lrrn3","shmt2","pitpnm2","man2a2","akt3b","znf804a","gigyf2","ambra1","sbno1","c10orf32","ireb2","cacnb2","foxg1","snap91"],["klc1","gria1","c2orf82","nrgn","fam5b","gatad2ab","nck1","atxn7","grm3","fut9a","fes","galnt10","anp32e","gramd1b","slc35g2","tsnare1","snx19","plcl1","c12orf65","sipa1l1","ep300","dgkz","tle1","bag5","gpm6a","tbc1d5","shisa9","mdk","negr1","mir137","pak6","cntn4","ca8","man2a1","kcnj13","tcf20","csmd1","stat6","vrk2","egr1","cacna1c","cnksr2","satb1","hcn1","chst12","c2orf69","foxg1het","lrp1","arhgap1","rora","arl3","ckb","fpgt","znf536","grin2a","cnnm2","luzp2","elfn1","bcl11b","tcf4","mad1l1","tle3","kmt2e","clcn3","lrrn3","shmt2","pitpnm2","man2a2","akt3b","znf804a","gigyf2","ambra1","sbno1","c10orf32","ireb2","cacnb2","foxg1","snap91"]]
#print(M)
linklist = ['ward','complete','average']
for l in linklist:
	fig=my_clustermap(M,method=l,thrs_col=1.27,thrs_row=1.27,row_cls=True,return_fig=True)#,colnames=np.array(labels),rownames=np.array(labels))
#fig=my_clustermap(M,method='average',thrs_col=1.25,thrs_row=1.25,row_cls=True,return_fig=True,colnames=np.array(labels),rownames=np.array(labels))
#fig.savefig("../Results/pErk_ave_overlap_Binary.pdf")
