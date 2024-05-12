#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 20:02:47 2024
Created to remove scatter from images.
Pass list of averaged images to this program. This will apply scatter correction
and mask the off disk features.
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
    plt.close()

if __name__=='__main__':
    ### USER DEFINED ###
    ftrname= 'BB03'
    scatter_correction=True
    visualize=True
    writefits=True
    #####################
    
    print("Generating files for", ftrname)
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/')
    folder= project_path+'data/interim/'+ftrname+'/averaged_files/'
    sc_file= project_path+'references/sun_center_averaged_files_NB02.txt'
    #contains sun center information of each pointing.
    scatter_file= project_path+'data/external/'+ftrname+'_scat_0_lvl_0.fits'
    #contains scatter file for that filter
    sav= project_path+'data/processed/'+ftrname+'/masked_scatter_corrected_averaged_files/'

    
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