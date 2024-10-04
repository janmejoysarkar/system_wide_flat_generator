#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 08:22:32 2024

-Generated to create system wide flat field from off pointing data.
-Uses lighten blending mode.
-2024-04-08: Modified to use with scatter corrected, masked data
- Modified to use optimized upper limit for blurring
-2024-06-20: Large scale blur size was changed from 500 to 630.
-Small scale image/Large scale image was previously blurred with 100 px kernel
-This blurring has been removed.

*** NOTE ***

This branch is made for Test and Calib paper and ASWG closeouts only.
This is code is modified to make lighten blended illumination pattern of the CCD.

************

@author: janmejoy
"""
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
import os

def blur(data, kernel): #blurring function
    return(convolve(data, Box2DKernel(kernel), normalize_kernel=True))

def lighten(image_list):
    '''
    Lighten blend
    image_list= List of 2D numpy arrays
    '''
    lighten_blend=np.zeros(np.shape(image_list[0]))
    for image in image_list:
        for i in range(4096):
            for j in range(4096):
                if image[i,j] > lighten_blend[i,j]:
                    lighten_blend[i,j]=image[i,j]
    return(lighten_blend)

#def calib_status(data, row, col, size):
#    '''
#    returns % std and mean within a box
#    row, col, size: position and size of box to be used.
#    '''
#    data_crop=data[row-size:row+size, col-size:col+size]
#    std=np.std(data_crop)
#    mean= np.mean(data_crop)
#    std_pc, mean= round(std*100/mean, 2), round(mean, 2)
#    return(std_pc, mean)
#
#def profile(ftrname, data, row, col, saveplot=None): 
#    '''
#    To plot the image and generate line_profile of any numpy 2D Array
#    data= 2D numpy array
#    row, col= coordinates for line profiles
#    '''
#    fig= plt.figure(figsize=(8,4), dpi=300)
#    (ax1, ax2)=fig.subplots(1,2)
#    plt.suptitle(mfg_date+"_Intensity profiles across flat field- "+ftrname)   
#    ax1.imshow(data, origin='lower', vmin=0.9, vmax=1.1)
#    ax1.axhline(row, color='red')
#    ax1.axvline(col, color='blue')
#    ax1.set(ylabel="Pixels")
#    
#    ax2.plot(data[row], color='red', label= "Horizontal cut")
#    ax2.plot(data[:,col], color='blue', label= "Verical cut")
#    ax2.set(ylabel="Counts")
#    ax2.legend()
#    for ax in (ax1, ax2):
#        ax.set(xlabel="Pixels")    
#        ax.grid() 
#    if saveplot==True : plt.savefig(f'{project_path}reports/runtime_reports/{ftrname}.pdf')
#    plt.show()
#    
#def prep_header(ftrname, mfg, data_date):
#    header=fits.Header()
#    header['VERSION']=('beta', 'Version name for the Flat Field')
#    header['FTR_NAME']=(ftrname, 'Filter Name for SUIT')
#    header['SML_KRNL']=(str(small_kernel), 'Small scale kernel')
#    header['LRG_KRNL']=(str(large_kernel), 'Large scale kernel')
#    header['SHTR_STR']=(shtr, 'Shutter start position (0 or 180)')
#    header['MFG_DATE']=(mfg, 'Manufacturing date for the FITS file')
#    header['DATADATE']=(data_date,'Date of raw data recording')
#    return (header)
#
#def plot(data, caption): #plots any numpy array with imshow (caption= image title)
#    plt.figure()
#    plt.imshow(data, origin='lower')
#    plt.title(caption)
#    plt.show()

def edge_mask(data, thick):
    #masking the edges
    data[:thick+20]=1
    data[-(thick+20):]=1
    data[:,:thick+20]=1
    data[:,-(thick+20):]=1
    return(data)

def flat_generator(ftrname):
    folder=project_path+'data/processed/'+ftrname+'/masked_scatter_corrected_averaged_files/'
    sav= project_path+f'products/'
    savename= "lighten_illumination"
    #######################
    if os.path.exists(sav): 
        print(f"Saving flat fields at: {sav}\n")
    else:
        print("Write path does not exist. Aborting process.\n")
        exit()
    
    print("Generating Flat for", ftrname)
    files= os.listdir(folder)
    img_ls=[]
    for file in files:
        data= fits.open(folder+file)[0].data
        img_ls.append(data)
        
    lighten_img= lighten(img_ls).T #blends the images in Lighten mode
    #small_scale_removed_img= blur(lighten_img, small_kernel) #removes small scale structures (PRNU and CCD dust)
    #large_scale_img= blur(small_scale_removed_img, large_kernel) #isolates large scale illumination changes.
    ##removes large scale pattern from small scale removed image
    #flat_field= small_scale_removed_img/large_scale_img
    #flat_field_lvl1= np.transpose(flat_field)
    #flat_field_lvl1= edge_mask(flat_field_lvl1, int(large_kernel/2)+20)
    hdu= fits.PrimaryHDU(lighten_img)#, header=prep_header(ftrname, mfg_date, data_date))
    ##saves the fits file
    if save==True : hdu.writeto(sav+ftrname+'_shtr_'+shtr+"_"+savename+'_lvl1.fits', overwrite=True)
    ##visualization
    #profile(ftrname, flat_field_lvl1, 2048, 2048, saveplot=True) #to plot image profile

    ##statistics
    #print("***************")
    #print(ftrname)
    #print("Pos(200px Box) \t %Std, Mean")
    #print("(1000, 1000)", calib_status(flat_field, 1000, 1000, 100))
    #print("(2000, 2000)",calib_status(flat_field, 2000, 2000, 100))
    #print("(3000, 3000)",calib_status(flat_field, 3000, 3000, 100))
    #print("***************")
    return(lighten_img)
    
if __name__=='__main__':
    #### USER-DEFINED ####
    mfg_date, data_date= '2024-06-20', '2024-01-29'
    small_kernel, large_kernel= 50, 630
    save= True #toggle to False to not save the image
    shtr= "0" #to be used in saved filename
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_project/')
    lighten_image=flat_generator('BB03')

    '''
    ftr_list= ["NB01", "NB02", "NB03", "NB04", "NB05", "NB06", "NB07", "NB08", "BB01", "BB02", "BB03"]
    with ProcessPoolExecutor() as execute:
        execute.map(flat_generator, ftr_list)
    '''
