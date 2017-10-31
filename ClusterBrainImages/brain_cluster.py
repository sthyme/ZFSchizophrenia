import numpy as np
import tifffile
import os
import scipy
from scipy.ndimage.morphology import binary_dilation
import dill
import pandas as pd
from scipy.signal import fftconvolve

def save_object(obj, filename):
    """
    Dump a python object as a dill file. The file can then be loaded by function load_object()
    """
    with open(filename,'wb+') as f:
        f = open(filename, "wb")
        dill.dump(obj, f)
    return

def load_object(filename):
    """
    Load dill dumped file.
    """
    with open(filename, "rb") as f:
        obj = dill.load(f)
    return obj

def dilate(brain_im,rs=[2,4,4],thres=50):
    """
    Dilate each point in a binarized 3D np.array.
    Inputs:
    braim_im: a 3D np.array.
    rs: the radius for performing the dilation along each axis.
    thres: the threshold value for binarizing the input image. If thres is False, input must be a binarized array.
    Returns a binary 3D np.array of the same shape as the input one.
    """
    if thres:
        brain_im=brain_im>thres
    if np.sum(np.sum(brain_im))==0:
        return(np.array(brain_im*0,dtype=bool))
    else:
        x,y,z = np.indices([2*rs[0]+1,2*rs[1]+1,2*rs[2]+1])
        sphere = (x-rs[0])**2/rs[0]**2+(y-rs[1])**2/rs[1]**2+(z-rs[2])**2/rs[2]**2<1
        brain_dil = binary_dilation(brain_im,sphere)
        return(brain_dil)

def calc_overlap(brain_i, brain_j, thres=50,rs=[2,4,4],binary=True,dil=True):
    """
    Calculate a similarity score based on overlaping signals for two input images.
    Inputs:
    brain_i, brain_j: images of interest in format of 3D np.array. the two images must be of the same shape.
    thres: the threshold for binarizing the image in order to calculate the overlap score (with the function dilate()).
    rs: the radius for performing the dilation along each axis.
    binary: whether to binariz the images when calculating the overlap.
    dil: whether to dilate the pixels with signals for calculating the overlapping region of the two images.
    Returns a floating point similarity score. The range of the score is between 0 (no overlap at all) and 1 (perfect overlap).
    """
    if dil:
        brain_i_dil=dilate(brain_i,rs=rs,thres=thres)
    else:
        brain_i_dil=(brain_i>thres)*1
    if np.sum(brain_i_dil)==0:
        return(0)
    else:
        if dil:
            brain_j_dil=dilate(brain_j,rs=rs,thres=thres)
        else:
            brain_j_dil=(brain_j>thres)*1
        if np.sum(brain_j_dil)==0:
            return(0)
        else:
            overlap_ind=brain_j_dil*brain_i_dil>0
            if dil:
                if binary:
                    brain_i_norm=(brain_i>thres)*1/np.sum((brain_i>thres)*1)
                    brain_j_norm=(brain_j>thres)*1/np.sum((brain_j>thres)*1)
                else:
                    brain_i=(brain_i>thres)*brain_i
                    brain_j=(brain_j>thres)*brain_j
                    brain_i_norm=brain_i/np.sum(brain_i)
                    brain_j_norm=brain_j/np.sum(brain_j)
            else:
                if binary:
                    brain_i_norm=brain_i_dil/np.sum(brain_i_dil)
                    brain_j_norm=brain_j_dil/np.sum(brain_j_dil)
                else:
                    brain_i=(brain_i>thres)*brain_i
                    brain_j=(brain_j>thres)*brain_j
                    brain_i_norm=brain_i/np.sum(brain_i)
                    brain_j_norm=brain_j/np.sum(brain_j)
            overlap_i=brain_i_norm*overlap_ind
            overlap_j=brain_j_norm*overlap_ind
            overlap=np.sum(overlap_i+overlap_j)/np.sum(brain_j_norm+brain_i_norm)
            return(overlap)

def overlap_matrix(file_dir="./images/", files=None, mask=None, sym=False, channel=['R&G'], ,dil=True, rs=[2,2,4], st_ed_i=None, st_ed_j=None, verbose=True,save=False,retn=True,thres=50,binary=True,n_sig_thres=100):
    """
    Calculate pairwise overlap score for a list of images.
    Restriction on the input images: 
        The images need to be in tif format, and are assumed to have 4 dimensions.
        The first 3 dimensions encode for the 3D space, with the 3rd dimension as the left-right axis. This is important if making the images left-right symmetric before calculating overlap is desired.
        The 4th dimension is for the 3 color channels, R G and B. The R and B (first and third) channels are asummed to be identical, and the B (third) channel is not used in the function.

    Input:
        file_dir: directory that contains images of interest. The image files need to be of tif format and have ".tif" as filename extension.
        files: name of the files in the file_dir to use. If set to "None", all tif files in the directory will be used.
        mask: a binary 3D numpy array with the same shape as the first 3 dimensions of the input images. The mask is for filtering out signals in the unwanted regions in the images.
            Pixel positions to keep in images are marked with 1; positions to filter out are marked with 0.
        sym: whether to make the images left-right symmetric (along the 3rd dimension of the input image) before calculating overlap.
        channel: which color channel of each image to calculate the overlap score on. Need to be passed as strings in a list. 
            Passible values in the list are: "R" (first channel), "G" (second channel), and "R&G" (max of the first two channels at each pixel position).
        dil: whether to dilate the signals in 3D when calculating overlapping signal regions.
        rs: the radii to use for dilating the signals in the images. Needs to be passed as a list with 3 elements, specifying the radius to use for each of the first 3 dimensions of the images.
        st_ed_i: start and end index for the images to run the code with. To be used in the outer loop of the nested for-loop in the function.
            For example: if st_ed_i=10 (integer), the code will run the images indexed with 10 (the 9th image) to the last image in the input files.
                If st_ed=[0,10] (list of two integers), the code will run the images indexed from 0 (the 1st image) to 9 (the 8th image).
        st_ed_j: start and end index for the images to run the code with. To be used in the inner loop of the nested for-loop in the function.
        verbose: whether to print out the progress as the code is running.
        save: path of the file to save the resulting matrix as. The saved file can be read in python using the load_object function defined above. 
            If False, the result will be calculated but not saved to a file.
        retn: whether to return the resulting matrix in the current environment.
        binary: whether to binarize the image when calculating the overlap.
        thres: the intensity threshold to use for binarizing the image and calling out signals.
        n_sig_thres: the minimum number of pixels with signal to consider the image as having signal. If an image has no signal, its overlap score with any image will be set to 0 without performing calculation.
    Output:
        A dictionary whose keys are the elements in the input argument "channel". 
        For example, if channel=["R","R&G"], the function will return a dictionary {"R": matrix_calculated_with_channel_R, "R&G": matrix_calculated_with_channel_R&G}.
        Each value in the dictionary is a pandas dataframe of a symmetric matrix storing the overlap scores, with the input file names as column and row names. 
    """
    if (files is None):
        files=np.sort([name for name in os.listdir(file_dir) if name.endswith('.tif')])
    else:
        files=np.sort(files)
    num_file=len(files)
    overlap={}
    for chan in channel:
        overlap[chan]=np.zeros((num_file,num_file))
    if (mask is not None) & sym:
        mask=np.max(np.array([mask,mask[:,:,::-1]]),axis=0)
    if st_ed_i is None:
        st=0
        ed=num_file
    elif type(st_ed_i) is int:
        st=st_ed_i
        ed=num_file
    else:
        st=st_ed_i[0]
        ed=st_ed_i[1]
    for i in range(st,ed):
        if verbose:
            print('Calculating overlap score of image # '+str(i))
        brain_is={}
        brain_i=np.array(tifffile.imread(file_dir+files[i]))
        if np.sum(brain_i>thres)<100:
            if verbose:
                print('skip')
            continue
        if sym:
            brain_i=np.max(np.array([brain_i,brain_i[:,:,::-1,:]]),axis=0)
        if 'R&G' in channel:
            brain_is['R&G']=np.max(np.array([brain_i[:,:,:,0],brain_i[:,:,:,1]]),axis=0)
        if 'R' in channel:
            brain_is['R']=brain_i[:,:,:,0]
        if 'G' in channel:
            brain_is['G']=brain_i[:,:,:,1]

        sig=False
        for chan in channel:
            if mask is not None:
                brain_is[chan]=brain_is[chan]*mask
            #brain_is[chan]=brain_is[chan]
            if np.sum(brain_is[chan]>thres)>100:
                sig=True
        if not sig:
            if verbose:
                print('skip')
            continue
        if st_ed_j is None:
            stj=i
            edj=num_file
        elif type(st_ed_j) is int:
            stj=st_ed_j
            edj=num_file
        else:
            stj=st_ed_j[0]
            edj=st_ed_j_[1]
        for j in range(stj,edj):
            brain_js={}            
            brain_j=np.array(tifffile.imread(file_dir+files[j]))
            if np.sum(brain_j>thres)<n_sig_thres:
                if verbose:
                    print('Skiping calculation with image #' + str(j) + ' due to low amount of signals.')
                continue
            if sym:
                brain_j=np.max(np.array([brain_j,brain_j[:,:,::-1,:]]),axis=0)
            if 'R&G' in channel:
                brain_js['R&G']=np.max(np.array([brain_j[:,:,:,0],brain_j[:,:,:,1]]),axis=0)
            if 'R' in channel:
                brain_js['R']=brain_j[:,:,:,0]
            if 'G' in channel:
                brain_js['G']=brain_j[:,:,:,1]
                
            sig=False
            for chan in channel:
                if mask is not None:
                    brain_js[chan]=brain_js[chan]*mask
                #brain_js[chan]=brain_js[chan]>thres
                print(np.sum(brain_js[chan]>thres))
                if np.sum(brain_js[chan]>thres)>n_sig_thres:
                    sig=True
            if not sig:
                if verbose:
                    print('Skiping calculation with image #' + str(j) + ' due to low amount of signals.')
                continue
            else:
                if verbose:
                    print('with image # '+str(j))
            for chan in channel:
                overlap[chan][i,j]=calc_overlap(brain_is[chan],brain_js[chan],rs=rs,thres=thres,binary=binary,dil=dil)
                overlap[chan][j,i]=overlap[chan][i,j]
    for chan in channel:
        overlap[chan]=pd.DataFrame(overlap[chan],index=files, columns=files)
    if save:
        save_object(overlap,save)
    if retn:
        return(overlap)

def collect_results(file_dir, output_path, retn=True):
    """
    Collect result from multiple subjobs to create the one final matrix (for each channel) for clustering.
    Inputs:
        file_dir must contain only output files from the overlap_matrix function.
        output_path: path for the result file to be saved as.
        retn: whether to return the result in the current environment.
    Output:
        A dictionary with channels ("R", "G", "R&G" or any combination of the three) as the keys. 
        Each key is associated with a pandas dataframe. 
        Each dataframe contains all the overlap scores in the sub-result files resulted from running all images in multiple subjobs.
        Each dataframe has the same row and column names as in each of the input sub-result files.
    """
    res_files=[res for res in os.listdir(file_dir)]
    res_collect={}
    for res in np.array(res_files):
        res_collect[res]=fxn.load_object(file_dir+res)
    key0=res_files[0]
    res_all={}
    for res in np.array(res_files):
        res_collect[res]=fxn.load_object(res_dir+res)
    for chan in res_collect[key0].keys():
        res_all[chan]=np.zeros(res_collect[key0][chan].shape)

    for key in res_collect.keys():
        for chan in res_all.keys():
            res_all[chan]=res_all[chan]+res_collect[key][chan]
    save_object(res_all,output_path)
    if retn:
        return(res_all)



