#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 08:22:32 2024

-Generated to create system wide flat field from off pointing data.
-Uses lighten blending mode.
-2024-04-08: Modified to use with scatter corrected, masked data
@author: janmejoy
"""
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
from astropy.convolution import convolve
from astropy.convolution import Box2DKernel
import os

def blur(data, kernel): #blurring function
    return(convolve(data, Box2DKernel(kernel), normalize_kernel=True))

def lighten(image_list):
    '''
    Lighten blend
    image_list= List of 2D numpy arrays
    '''
    lighten_blend=np.zeros(np.shape(data))
    for image in image_list:
        for i in range(4096):
            for j in range(4096):
                if image[i,j] > lighten_blend[i,j]:
                    lighten_blend[i,j]=image[i,j]
    return(lighten_blend)

def calib_status(data, row, col, size):
    '''
    returns % std and mean within a box
    row, col, size: position and size of box to be used.
    '''
    data_crop=data[row-size:row+size, col-size:col+size]
    std=np.std(data_crop)
    mean= np.mean(data_crop)
    std_pc, mean= round(std*100/mean, 2), round(mean, 2)
    return(std_pc, mean)

def profile(data, row, col): 
    '''
    To plot the image and generate line_profile of any numpy 2D Array
    data= 2D numpy array
    row, col= coordinates for line profiles
    '''
    fig= plt.figure(figsize=(8,4), dpi=300)
    (ax1, ax2)=fig.subplots(1,2)
    plt.suptitle("Intensity profiles across flat field- "+ftrname)   
    ax1.imshow(data, origin='lower')
    ax1.axhline(row, color='red')
    ax1.axvline(col, color='blue')
    ax1.set(ylabel="Pixels")
    
    ax2.plot(data[row], color='red', label= "Horizontal cut")
    ax2.plot(data[:,col], color='blue', label= "Verical cut")
    ax2.set(ylabel="Counts")
    ax2.legend()
    for ax in (ax1, ax2):
        ax.set(xlabel="Pixels")    
        ax.grid() 
    plt.show()
    
def plot(data, caption): #plots any numpy array with imshow (caption= image title)
    plt.figure()
    plt.imshow(data, origin='lower')
    plt.title(caption)
    plt.show()


if __name__=='__main__':
    
    #### USER-DEFINED ####
    ftrname="NB02"
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/')
    folder=project_path+'data/processed/'+ftrname+'/masked_scatter_corrected_averaged_files/'
    sav= project_path+'products/shtr_0_reduced_avg_files_flat/'
    #thres=0
    save= True #toggle to False to not save the image
    savename= "masked_scatter_corrected_reduced_avg_files_flat"
    shtr= "0" #to be used in saved filename

    #######################
    print("Generating Flat for", ftrname)
    files= os.listdir(folder)
    img_ls=[]
    for file in files:
        data= fits.open(folder+file)[0].data
        #data[data>thres]=0   #Intensity thresholding
        img_ls.append(data)
        
    lighten_img= lighten(img_ls) #blends the images in Lighten mode
    small_scale_removed_img= blur(lighten_img, 50) #removes small scale structures (PRNU and CCD dust)
    large_scale_img= blur(small_scale_removed_img, 220) #isolates large scale illumination changes.
    
    #removes large scale pattern from small scale removed image
    flat_field= blur(small_scale_removed_img/large_scale_img, 100) 
    #saves the fits file
    if save==True : fits.writeto(sav+ftrname+'_shtr_'+shtr+"_"+savename+'.fits', flat_field, overwrite=True)
    
    #visualization
    profile(flat_field, 2048, 2048) #to plot image profile

    #statistics
    print("Pos(200px Box) \t %Std, Mean")
    print("(1000, 1000)", calib_status(flat_field, 1000, 1000, 100))
    print("(2000, 2000)",calib_status(flat_field, 2000, 2000, 100))
    print("(3000, 3000)",calib_status(flat_field, 3000, 3000, 100))
    