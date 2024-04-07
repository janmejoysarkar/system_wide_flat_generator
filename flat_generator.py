#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 08:22:32 2024

-Generated to create system wide flat field from off pointing data.
-Uses lighten blending mode.
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
    ### lighten blend ###
    lighten_blend=np.zeros(np.shape(data))
    for image in image_list:
        for i in range(4096):
            for j in range(4096):
                if image[i,j] > lighten_blend[i,j]:
                    lighten_blend[i,j]=image[i,j]
    return(lighten_blend)

def calib_status(data, row, col, size):#returns % std and mean within a box
    data_crop=data[row-size:row+size, col-size:col+size]
    std=np.std(data_crop)
    mean= np.mean(data_crop)
    return(round(std*100/mean, 2), round(mean, 2))

def profile(data, row, col):    #line_profile   
    fig= plt.figure(figsize=(8,4), dpi=300)
    (ax1, ax2)=fig.subplots(1,2)
    plt.suptitle("Intensity profiles across residual image- "+ftrname)   
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


if __name__=='__main__':
    
    # ---- USER-DEFINED ----
    ftrname="NB02"
    #folder="/data1/janmejoy/system_wide_flat/"+ftrname+"/averaged_files/"
    folder='/data1/janmejoy/system_wide_flat/NB02/single_files_from_each_day_lvl0_shtr0/'
    sav= "/data1/janmejoy/system_wide_flat/"+ftrname+"/"
    shtr= "0"
    #thres=0
    savename= "reduced_avg_files_flat"
    save= False
    # ----------------------
    
    files= os.listdir(folder)
    img_ls=[]
    for file in files:
        data= fits.open(folder+file)[0].data
        #data[data>thres]=0   #Intensity thresholding
        img_ls.append(data)
        
    lighten_img= lighten(img_ls)
    flat_field= blur(lighten_img, 50)
    print("Pos(200px Box) \t %Std, Mean")
    print("(1000, 1000)", calib_status(flat_field, 1000, 1000, 100))
    print("(2000, 2000)",calib_status(flat_field, 2000, 2000, 100))
    print("(3000, 3000)",calib_status(flat_field, 3000, 3000, 100))

    profile(flat_field, 2048, 2048)
    if save==True : fits.writeto(sav+ftrname+'_shtr_'+shtr+"_"+savename+'.fits', flat_field, overwrite=True)
    
    