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
import seaborn as sns
import glob
#from matplotlib import rcParams
#rcParams.update({'figure.autolayout': True})
#import makepds

cdict1 = {'red':   ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 1.0),
                   (1.0, 0.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.5, 0.8, 1.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (0.5, 1.0, 0.0),
                   (1.0, 0.0, 0.0))
        }


def clustermap(fname,matrix,thrs_row=1,thrs_col=1,row_cls=False,col_cls=True,method='average',fig_sz=(8,8),colnames=None, rownames=None,cls_info=False):
    colors=sns.color_palette("Set2", 25)
    colors=[mat_col.rgb2hex(color) for color in colors]
    set_link_color_palette(colors)
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
        D_row=scipy.spatial.distance.pdist(matrix)
    if col_cls:
        D_col=scipy.spatial.distance.pdist(matrix.T)
    fig=plt.figure(figsize=fig_sz)
    lef=0.01
    bot=0.05
    h_sep=0.2
    v_sep=0.7
    row_leg=0.01 #space for the legend of the rows plotted on the right side of the matrix
    if row_cls:
        if col_cls: #if want both row and column dendrogram
            mat_h=v_sep-0.005-bot
            mat_w=0.9-row_leg-h_sep
            den_h=1-v_sep-0.005
            den_w=h_sep-0.005-lef
            #plot dendrogram for column clusters
            ax_col=fig.add_axes([h_sep,v_sep,mat_w,den_h])
            #g_col=scipy.cluster.hierarchy.linkage(D_col,method=method, metric='cosine')
            g_col=scipy.cluster.hierarchy.linkage(D_col,method=method)
            den_col=scipy.cluster.hierarchy.dendrogram(g_col,color_threshold=thrs_col)
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
        den_row=scipy.cluster.hierarchy.dendrogram(g_row,color_threshold=thrs_row,orientation='left')
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
        den_col=scipy.cluster.hierarchy.dendrogram(g_col,color_threshold=thrs_col)
        idx_col = den_col['leaves']
        idx_row=list(range(0,matrix.shape[0]))
        ax_col.set_xticklabels([''])
        ax_mat = fig.add_axes([lef,bot,mat_w,mat_h])
    #plot data matrix as a heatmap
    matrix=np.array(matrix)
    D = matrix[idx_row,:]
    D = D[:,idx_col]
    blue_yellow1 = LinearSegmentedColormap('BlueYellow1', cdict1)
    #x=range(-1,1)
    #y=range(-1,1)
    #x,y=np.meshgrid(x,y)
    ax_mat.set_aspect('equal')
    im = ax_mat.pcolormesh(D,cmap=blue_yellow1,vmin=-0.05,vmax=0.05)
    #im = ax_mat.matshow(D, aspect='auto', origin='lower', cmap=plt.cm.YlGnBu)
    ax_mat.xaxis.set_ticks_position('bottom')
    ax_mat.yaxis.set_ticks_position('left')
    #ax_mat.yaxis.set_ticks_position('right')
    ax_mat.set_xticks(list(np.asarray(list(range(0,matrix.shape[1])))+0.5))
    ax_mat.set_yticks(list(np.asarray(list(range(0,matrix.shape[0])))+0.5))
    #ax_mat.set_yticks(list(range(0,matrix.shape[0])))
    ax_mat.set_xticklabels(colnames[idx_col], rotation = 'vertical', fontsize=5)
    ax_mat.set_yticklabels(rownames[idx_row], fontsize=5)
		#ax_mat.set_yticklabels(rownames[idx_row], va='center')
    ax_mat.grid(False)
    #plt.subplots_adjust(bottom=0.1)
    #fig,ax = plt.subplots()
    #fig.subplots_adjust(top=1,bottom=0.5)
		#fig.tight_layout()
    # Plot colorbar.
    axcolor = fig.add_axes([0.94,bot,0.02,mat_h])
    plt.colorbar(im, cax=axcolor)
    namepre = fname.split(".")[0]
    print namepre
    print colnames[idx_col]
    if row_cls:
			namepre = namepre + "rows_"
    plt.savefig(namepre+method+".png",bbox_inches='tight', dpi=600)
    if cls_info:
        cls_dic={}
        if col_cls:
            cls_dic['col_ind']=den_col['leaves']
            cls_dic['col_cls']=scipy.cluster.hierarchy.fcluster(g_col,t=thrs_col,criterion='distance')
        if row_cls:
            cls_dic['row_ind']=den_row['leaves']
            cls_dic['row_cls']=scipy.cluster.hierarchy.fcluster(g_row,t=thrs_row,criterion='distance')
        return(cls_dic)

# Generate a random matrix to test the clustering algorithm.
#D = np.random.rand(40,30) ## this mock data has 40 observations and 30 samples
##D=pd.DataFrame(D,index=range(1,41)) ## If input is a pandas dataframe, the algorithm will extract the row and column names and use for plotting
for fname in glob.glob("AUG16*.csv"):
	D=pd.read_csv(fname)
	#D=pd.read_csv("updatedlowavedata.csv")
###D = makepds.generateDF()
#	method = ['ward', 'complete', 'average']
	method = ['complete']
	for t in method:
		cls_info=clustermap(fname,D,row_cls=False,col_cls=True,cls_info=True,method=t,thrs_col=3)
#	cls_info=clustermap(D,row_cls=True,col_cls=True,cls_info=True,method=t,thrs_col=3)
#cls_info=clustermap(D,row_cls=False,col_cls=True,cls_info=True,method='ward',thrs_col=3)
#cls_info=clustermap(D,row_cls=False,col_cls=True,cls_info=True,method='average',thrs_col=3)
#cls_info=clustermap(D,row_cls=True,col_cls=True,cls_info=True,method='average',thrs_col=3)
