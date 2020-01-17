import numpy as np
import tifffile
import os
import scipy
import dill
import pandas as pd

def load_object(filename):
    f = open(filename, "rb")
    obj = dill.load(f)
    f.close()
    return obj

## Directory of the folder containing activity images
file_dir="/n/schier_lab2/everyone/avereallyfullfusionperk_Yiqun_filtered_fixed/"
#file_dir="/n/schier_lab2/everyone/avereallyfullfusionstruct_Yiqun_filtered_fixed/"
#file_dir="/n/boslfs/LABS/schier_lab/everyone/aveupdatedreallyfullfusionstruct_Yiqun_filtered/"
#file_dir="/n/schier_lab2/users/yiqunwang/Summer Data/ReviewAnalysis/filtered_fused_and_nodup/"

## Load various masks
mask_noSC=load_object("../Masks/whole_brain_mask_no_SpinalCord")
mask=load_object("../Masks/whole_brain_mask")
all_masks=load_object("../Masks/all_masks_sym_all_good")
#mask_dien=all_masks['Diencephalon']
#mask_mesen=all_masks['Mesencephalon']
#mask_rhom=all_masks['Rhombencephalon']
#mask_telen=all_masks['Telencephalon']
    
## Parse image names to extract genotype information: gene name, hom/het
files=[name for name in os.listdir(file_dir)]
genes=np.array([name.split("_")[0] for name in files])
genos=np.array([name.split("_")[2] for name in files])
genos=np.array([''.join(i for i in j if not i.isdigit()) for j in genos])
labels=[genes[i]+"_"+genos[i] for i in np.arange(len(genes))]

## Preallocate dataframes (1 for each channel) to store sum of intensities in each image (rows) for each region (columns)
all_regions=list(all_masks.keys())
sum_G=pd.DataFrame(np.zeros((len(files)+1,len(all_regions))),index=["size"]+labels,columns=all_regions)
sum_R=pd.DataFrame(np.zeros((len(files)+1,len(all_regions))),index=["size"]+labels,columns=all_regions)
sum_both=pd.DataFrame(np.zeros((len(files)+1,len(all_regions))),index=["size"]+labels,columns=all_regions)

## Calculate the size of each brain region by summing up each region mask. Write the sums in the dataframes as a row
sum_G.loc["size",:]=[np.sum(all_masks[region_mask]) for region_mask in all_regions]
sum_R.loc["size",:]=[np.sum(all_masks[region_mask]) for region_mask in all_regions]
sum_both.loc["size",:]=[np.sum(all_masks[region_mask]) for region_mask in all_regions]

## Preallocate dataframes to store number of active pixels in each image for each region
sum_numG=pd.DataFrame(np.zeros((len(files)+1,len(all_regions))),index=["size"]+labels,columns=all_regions)
sum_numR=pd.DataFrame(np.zeros((len(files)+1,len(all_regions))),index=["size"]+labels,columns=all_regions)
sum_numboth=pd.DataFrame(np.zeros((len(files)+1,len(all_regions))),index=["size"]+labels,columns=all_regions)

sum_numG.loc["size",:]=[np.sum(all_masks[region_mask]) for region_mask in all_regions]
sum_numR.loc["size",:]=[np.sum(all_masks[region_mask]) for region_mask in all_regions]
sum_numboth.loc["size",:]=[np.sum(all_masks[region_mask]) for region_mask in all_regions]

#labels=[filename.split('_')[0] for filename in files]

#sum_G=pd.DataFrame(np.zeros((len(files),6)),index=labels,columns=['Brain','NoSpinalCord','Diencephalon','Mesencephalon','Rhombencephalon','Telencephalon'])
#sum_R=pd.DataFrame(np.zeros((len(files),6)),index=labels,columns=['Brain','NoSpinalCord','Diencephalon','Mesencephalon','Rhombencephalon','Telencephalon'])
#sum_both=pd.DataFrame(np.zeros((len(files),6)),index=labels,columns=['Brain','NoSpinalCord','Diencephalon','Mesencephalon','Rhombencephalon','Telencephalon'])

## set intensity threshold for calling active pixels. 
thres=50
## Calculate region-wise sum of intensities and number of active pixels for each image
for i in np.arange(len(files)):
    file_name=files[i]
    label=labels[i]
    print("summing intensities for "+label+"...")
    brain_im=np.array(tifffile.imread(file_dir+file_name))
    brain_R=brain_im[:,:,:,0]
    brain_R=brain_R*(brain_R>=thres)
    brain_G=brain_im[:,:,:,1]
    brain_G=brain_G*(brain_G>=thres)
    brain_both=np.max(np.array([brain_im[:,:,:,0],brain_im[:,:,:,1]]),axis=0)
    #sum_G.loc[label,:]=[np.sum(brain_G*mask),np.sum(brain_G*mask_noSC),np.sum(brain_G*mask_dien),np.sum(brain_G*mask_mesen),np.sum(brain_G*mask_rhom),np.sum(brain_G*mask_telen)]
    #sum_R.loc[label,:]=[np.sum(brain_R*mask),np.sum(brain_R*mask_noSC),np.sum(brain_R*mask_dien),np.sum(brain_R*mask_mesen),np.sum(brain_R*mask_rhom),np.sum(brain_R*mask_telen)]
    #sum_both.loc[label,:]=[np.sum(brain_both*mask),np.sum(brain_both*mask_noSC),np.sum(brain_both*mask_dien),np.sum(brain_both*mask_mesen),np.sum(brain_both*mask_rhom),np.sum(brain_both*mask_telen)]
    sum_G.loc[label,:]=[np.sum(brain_G*all_masks[region_mask]) for region_mask in all_regions]
    sum_R.loc[label,:]=[np.sum(brain_R*all_masks[region_mask]) for region_mask in all_regions]
    sum_both.loc[label,:]=[np.sum(brain_both*all_masks[region_mask]) for region_mask in all_regions]
    
    sum_numG.loc[label,:]=[np.sum((brain_G>0)*all_masks[region_mask]) for region_mask in all_regions]
    sum_numR.loc[label,:]=[np.sum((brain_R>0)*all_masks[region_mask]) for region_mask in all_regions]
    sum_numboth.loc[label,:]=[np.sum((brain_both>0)*all_masks[region_mask]) for region_mask in all_regions]

## save the dataframes
sum_G.to_csv('/n/schier_lab2/users/yiqunwang/Summer Data/ReviewAnalysis/intensity_sum/all_regions_sum_perk_green_channel_PaperData_thres50.csv')
sum_R.to_csv('/n/schier_lab2/users/yiqunwang/Summer Data/ReviewAnalysis/intensity_sum/all_regions_sum_perk_red_channel_PaperData_thres50.csv')
sum_both.to_csv('/n/schier_lab2/users/yiqunwang/Summer Data/ReviewAnalysis/intensity_sum/all_regions_sum_perk_both_channels_PaperData_thres50.csv')

sum_numG.to_csv('/n/schier_lab2/users/yiqunwang/Summer Data/ReviewAnalysis/intensity_sum/all_regions_sum_nPix_perk_green_channel_PaperData_thres50.csv')
sum_numR.to_csv('/n/schier_lab2/users/yiqunwang/Summer Data/ReviewAnalysis/intensity_sum/all_regions_sum_nPix_perk_red_channel_PaperData_thres50.csv')
sum_numboth.to_csv('/n/schier_lab2/users/yiqunwang/Summer Data/ReviewAnalysis/intensity_sum/all_regions_sum_nPix_perk_both_channels_PaperData_thres50.csv')
