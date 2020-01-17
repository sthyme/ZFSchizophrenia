import numpy as np
import tifffile
import os
import scipy
import dill

def load_object(filename):
    f = open(filename, "rb")
    obj = dill.load(f)
    f.close()
    return obj

## Define the folder that stores the images to be processed
file_dir="../fusedimagesave/"

## Load in the mask objects
mask_noSC=load_object("../Masks/whole_brain_mask_no_SpinalCord")
mask=load_object("../Masks/whole_brain_mask")

## Save the masks as images
#tifffile.imsave("../filtered_struct/mask_noSC.tif",np.array(mask_noSC*255,dtype='int8'))
#tifffile.imsave("../filtered_struct//mask.tif",np.array(mask*255,dtype='int8'))

## Apply masks to each file in the directory and save
files=[name for name in os.listdir(file_dir)]

for file_name in files:
    label=file_name.split("_")[0]
    brain_im=np.array(tifffile.imread(file_dir+file_name))
    brain_filter=np.zeros(brain_im.shape,dtype='int8')
    brain_noSC=np.zeros(brain_im.shape,dtype='int8')
    ## Filter out signals outside mask region
    for i in range(0,3):
        brain_filter[:,:,:,i]=brain_im[:,:,:,i]*mask
        brain_noSC[:,:,:,i]=brain_im[:,:,:,i]*mask_noSC
    ## Save filtered images (into an existing directory)
    tifffile.imsave("../filtered_ave/"+label+"_NoSpinalCord.tif",brain_noSC)
    tifffile.imsave("../filtered_ave/"+label+".tif",brain_filter)