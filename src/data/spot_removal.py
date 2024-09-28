#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 11 17:41:34 2024
-Created to patch up sun spots on the Sun image for flat field generation.
-To be used on masked scatter corrected images. For NB08, scatter file is not available.
Being done without scatter correction for NB08.
2024-05-12- Used 1 px erosion to remove bright spots. Used Dilation filter 
to reduce sun spots.
@author: janmejoyarch
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np
import glob
from skimage.morphology import dilation, disk, erosion

####### USER-DEFINED #########
ftr_name='NB06'
overwrite=True #Files in the 'data/processed' directory will be replaced.
plot=False
##############################

project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/')
data_dir= os.path.join(project_path, f'data/processed/{ftr_name}/masked_scatter_corrected_averaged_files/*')
file_list= sorted(glob.glob(data_dir))[-7:]

pos_list= [(376, 1828), (1121, 2137), (2482,2172), (2524, 3111), 
           (3214, 3157), (445, 2036), (3194, 3011)]

print(f'Spot removal for {ftr_name}')
s=150
for file, (col, row) in zip(file_list, pos_list):
    data= fits.open(file)[0].data
    data_crop= data[row-s:row+s, col-s:col+s]
    data_crop=erosion(data_crop, disk(1))
    i=0
    dilated=data_crop
    while i<5 :
        shape=10
        dilated = dilation(dilated, disk(shape))
        i=i+1
    data[row-s:row+s, col-s:col+s]=dilated*0.97
    
    if plot==True:
        fig, ax= plt.subplots(1,2)
        ax[0].imshow(data_crop, origin='lower')
        ax[1].imshow(dilated, origin='lower')
        plt.show()
        plt.figure()
        plt.imshow(data, origin='lower')
    
    if overwrite == True: 
        fits.writeto(file, data, overwrite=True)
        print(f'Overwriting {file}')


def median_fill(): #To fill sun spot with median value
    for data_path, (col, row) in zip(file_list, pos_list):
        data= fits.open(data_path)[0].data
        data[row-s:row+s, col-s:col+s]=np.median(data[row-s:row+s, col+s:col+(2*s)])
        #fits.writeto(data_path, data, overwrite=False)
        plt.figure('1')
        plt.imshow(data, origin='lower')
        plt.scatter(col, row, color='red')
        plt.show()

