#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 16:24:42 2024

@author: janmejoyarch
"""
from astropy.io import fits
import numpy as np
import os
import glob


project_path=os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/')

files_path=project_path+'products/shtr_0_reduced_avg_files_flat/*'
sav_path= project_path+'products/shtr_0_reduced_avg_files_flat_lvl1/'

file_list= glob.glob(files_path)

for file in file_list:
    l0_data= fits.open(file)[0].data
    l1_product= np.transpose(l0_data)
    filename= file[-64:-5]+'_lvl1.fits'
    print(sav_path+filename, 'Saved!')
    fits.writeto(sav_path+filename, l1_product, overwrite=True)



