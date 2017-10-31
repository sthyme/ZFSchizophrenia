#!/usr/bin/python
import argparse
import brain_cluster as fxn
import os
import ast
import scipy
from scipy.ndimage.morphology import binary_dilation
from scipy.spatial.distance import cdist
import dill
import pandas as pd

### Take arguments from command line --- 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f_dir','-f_dir', help='Directory contains only the input images.', required=True)
    parser.add_argument('-out_dir','-o', help='Directory for output files.', required=True)
    parser.add_argument('-pre','-pre', help='prefix of the output file names.', required=True)
    parser.add_argument('-mask_f','-mask_f', help='path for mask file.', default=None)
    parser.add_argument('-dil','-dil', help='the radius to use for dilating the sigals in the image. If False, dilation will not be performed.', default=[2,4,4])
    parser.add_argument('-st_ed','-st_ed', help='indices for which reference images to run.', default=None)
    parser.add_argument('-st_ed2','-st_ed2', help='indices for which images to compare to the reference image.', default=None)
    parser.add_argument('-thres','-thres', help='intensity threshold for binarizing images.', default=50)
    parser.add_argument('-sym','-sym', help='whether to make the images left-right (third dimention of the image) symmetric .', default=False)

    args = parser.parse_args()
    out_dir = args.out_dir
    f_dir = args.f_dir
    pre = args.pre
    try:
        thres = ast.literal_eval(args.thres)
    except:
        thres = args.thres
    try:
        sym = ast.literal_eval(args.sym)
    except:
        sym = args.sym
    try:
        st_ed = ast.literal_eval(args.st_ed)
    except:
        st_ed = args.st_ed
    try:
        st_ed2 = ast.literal_eval(args.st_ed2)
    except:
        st_ed2 = args.st_ed2
    try:
        dil = ast.literal_eval(args.dil)
    except:
        dil = args.dil
    try:
        mask_f = ast.literal_eval(args.mask_f)
    except:
        mask_f = args.mask_f

if mask_f is not None:
    mask_f=fxn.load_object(mask_f)

fxn.overlap_matrix(f_dir, st_ed_i=st_ed, st_ed_j=st_ed2, mask=mask_f, save=out_dir+pre,rs=dil, sym=sym, channel=['R&G','R','G'],binary=True,thres=thres,dil=True,verbose=True)

