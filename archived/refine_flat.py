#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 17:14:24 2024
-Prepared to refine the generated flat field by feature removal.
-To be implemented into the pipeline later.
@author: janmejoyarch
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os
from astropy.convolution import convolve, Box2DKernel

def blur(data, kernel):
    return(convolve(data, Box2DKernel(kernel), normalize_kernel=True))
def plot(data, name):
    plt.figure()
    plt.imshow(data, origin='lower')
    plt.title(name)
    plt.show()

if __name__=='__main__':
    ftrname= 'NB02'
    file= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/products/shtr_0_reduced_avg_files_flat/'+ftrname+'_shtr_0_masked_scatter_corrected_reduced_avg_files_flat.fits')
    sav= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/products/shtr_0_reduced_avg_files_flat/'+ftrname+'_refined_shtr_0_masked_scatter_corrected_reduced_avg_files_flat.fits')
    save=True
    
    hdu= fits.open(file)
    data= hdu[0].data
    blurred= blur(data, 220)
    corrected= blur(data/blurred, 100)
    if save==True: fits.writeto(sav, corrected)
    
    plot(blurred, 'blurred')
    plot(corrected, 'corrected')

