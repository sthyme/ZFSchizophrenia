import cv2
from PIL import Image
import os
import glob
import numpy as np

# START CONVERT MAP TIFF to png image set with transparent background 

def convert_tiff_to_map_png(file):
    """convert a tiff stack to transparent background and the BGR color desired
    for the mask portion. For example BGR => [80,100,30] for dark green, totally
    non-transparent on mask areas.
    """
    tiff = Image.open(file) 
    j = 0
    for i in xrange(tiff.n_frames):
        tiff.seek(i)
        image = np.array(tiff)

        img_num = '0' * (3 - len( str(j) )) + str(j)
        # generate new file name for png image from original tiff image 
        base_filename = file.split('/')[-1].split('.')[0]

        # check if directory to stora files exists and if not create it
        mdir = os.getcwd() + '/' + 'maps/' + base_filename
        if not os.path.exists(mdir):
            os.mkdir(mdir)

        new_filename = base_filename + '_' + img_num + '.png' 
        new_filename = 'maps/' + base_filename + '/' + new_filename

        # convert tiff slide from RGB to BGRA (include alpha channel)
        # raw image is in BGR from Image.open. convert to RGBA for opencv as that's what it expectes
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)

        # where image was black make and opaque it black and transparent
        image[np.where((image==[0,0,0,255]).all(axis=2))] = [0,0,0,0]

        image = cv2.transpose(image)
        image = cv2.flip(image, dst=None, flipCode=0)


        # save file
        print new_filename
        cv2.imwrite(new_filename,image)
        j += 1

def convert_tiff_dir_to_map_png(tdir):
    """conver an entire directory of maps tiff files to png. The black background will be transparent.
    """
    print 'CONVERTING TIFF DIRECTORY TO MAP PNGS WITH TRANSPARENT BACKGROUND'
    tdir = tdir + '/*' + '.tif'
    files = glob.glob(tdir)

    for file in files:
        print 'converting tiff of map' + file + 'to png with transparent background'
        convert_tiff_to_map_png(file)

# END CONVERT MAP TIFF to png image set with transparent background 

if __name__ == '__main__':
    convert_tiff_dir_to_map_png('maps')



