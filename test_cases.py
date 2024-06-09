#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:27:38 2024

@author: janmejoyarch
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np

def stripe(power):
    x= np.linspace(0, 20*np.pi, 4096)
    sine_arr= np.ones((4096,4096))
    for i in range(sine_arr.shape[0]):
        y= power*np.sin(x-0.001*i)+1 #Make diagonal stripe pattern
        sine_arr[i]=sine_arr[i]*y
    return(sine_arr)

project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project')
data_path= os.path.join(project_path, 'products/25_500/BB03_shtr_0_masked_scatter_corrected_reduced_avg_files_flat_lvl1.fits')
data= fits.open(data_path)[0].data
line_prof= data[2048]
x= np.arange(len(line_prof))
plt.figure()
plt.imshow(data, origin='lower')
plt.figure()
plt.plot(line_prof)
#plt.imshow(sine_arr, cmap='gray', origin='lower', alpha=0.2)


'''
line_prof= np.sum(data, axis=1)
x= np.arange(len(line_prof))
a,b,c= np.polyfit(x, line_prof, 2)
y= a*x**2+b*x+c
'''