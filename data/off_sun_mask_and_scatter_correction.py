#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 20:02:47 2024
Created to remove scatter from images
@author: janmejoyarch
"""
import os
from astropy.io import fits
import numpy as np
import glob
import matplotlib.pyplot as plt

def create_circular_mask(h, w, col, row, radius):
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - col)**2 + (Y-row)**2)
    mask = dist_from_center <= radius
    return mask

def plot(data, col, row):
    plt.imshow(data, origin='lower')
    plt.plot(col, row, 'o', color='r')
    plt.title(file[-44:])
    plt.show()

if __name__=='__main__':
    ### USER DEFINED ###
    folder= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/data/processed/NB02/averaged_files/')
    sc_file= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/references/sun_center_averaged_files_NB02.txt')
    scatter_file= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/data/external/NB2_scat_shtr0_lvl0.fits')
    sav= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/data/processed/NB02/masked_scatter_corrected_averaged_files/')
    scatter_correction=True
    visualize=True
    writefits=True
    #####################
    
    filelist= sorted(glob.glob(folder+"*"))
    sc_info= np.loadtxt(sc_file, skiprows=1, usecols=(1,2))
    scatter_data= fits.open(scatter_file)[0].data
    
    for file, sc in zip(filelist, sc_info):    
        data=fits.open(file)[0].data
        if scatter_correction==True : data= data-scatter_data
        mask= create_circular_mask(4096, 4096, sc[1], sc[0], 1500)
        data=data*mask
        if visualize==True: plot(data, sc[1], sc[0])
        if writefits==True: fits.writeto(sav+file.split("/")[-1],data, overwrite=True)