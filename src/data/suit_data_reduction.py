#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 17:57:23 2024
-This script picks individual files from the csv file. The csv file contains
the real path of Complete Level 0 Files segregated based on shutter position and 
pointing target.
- reduce_files() Is used to reduce the files.
- average() Is used to make average of files of the same pointing and same filter.
@author: janmejoyarch
"""
import os
import sys
sys.path.append("/home/janmejoyarch/Dropbox/Janmejoy_SUIT_Dropbox/scripts/suit_pipeline_git/suitPipeline-main")
from overScan import removeOverScanAndDark
from astropy.io import fits
import numpy as np

def reduce_files(ftrname):
    '''
    Used to reduce files of a particular filter. The images are to be
    retrieved from a csv file containing realpaths of the files.
    '''
    sav= red_file_dir+'reduced_all_img_'+ftrname+'/'
    os.mkdir(sav) #create folder with filter name
    os.chdir(imagelist_path)
    csvlist= os.listdir()
    for i in csvlist:
        csv= open(i, 'r')
        lines= csv.readlines()
        makefolder=sav+i[:-4]+'/'
        os.mkdir(makefolder)
        for line in lines:
            filepath= line.split()[0]
            if (filepath.endswith(ftrname+'.fits')):
                print(filepath[-64:])
                removeOverScanAndDark(filepath, makefolder+'reduced_'+filepath[-64:], doOverscanCorrection=True, doGainCorrection=True)

def average(ftrname, avg_sav_dir):
    '''
    To save the average of each day's files during off pointing.
    '''    
    os.mkdir(avg_sav_dir)
    path= red_file_dir+'reduced_all_img_'+ftrname+'/'
    filelist=os.listdir(path)
    for i in filelist:
        print(i)
        file_ls=[]
        for j in os.listdir(path+i):
            data= fits.open(path+i+'/'+j)[0].data
            file_ls.append(data)
            print(j)
        sav= avg_sav_dir+ftrname+'_'+i+'.fits'
        fits.writeto(sav, np.mean(file_ls, axis=0))
        print("File Saved:", sav)    

if __name__=="__main__":
    ftrname="BB01"
    
    #define the path that contains the csv files containing the image lists.
    imagelist_path= '/home/janmejoyarch/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_field/complete_files_list_shtr_0'
    red_file_dir= '/data1/janmejoy/system_wide_flat/'+ftrname+'/' #directory to save reduced files
    reduce_files(ftrname)
    avg_sav_dir= '/data1/janmejoy/system_wide_flat/'+ftrname+'/averaged_files/' #directory to save averaged files
    average(ftrname, avg_sav_dir) #creates average files of the same filter and shutter position
    
    





