#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 18:31:58 2024

@author: janmejoyarch
-This generates daily log file to identify the partial files in each pointing.
-Pointing change happens at 07:20 UT and 03:35 UT. Split has been made for each 
day's pointing at 07:20 UT.
-This uses xlsx files generated while making fits from binary packets to find
partial files.
-2024-02-26: Modifications made to give realpath of files.
This script can be modified to pick specific files of choice.
File variables chosen to give realpath for complete images with shutter pos 0. 
-This lists all filter images.
"""

import pandas as pd
import glob

##### USER-DEFINED #####
suit_scratch= '/home/janmejoyarch/sftp_drive/' #mount point of /scratch folder of SUIT server. Use sshfs to mount. 
save_loc='/home/janmejoyarch/Desktop/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_field/complete_files_list_shtr_0/' #Save location
typ= 'complete' # 'complete' or 'partial'
shtrpos= 0 # 0 or 180 Shutter position
mode= 'Engineering Mode' #Mode of taking images
########################

#make a consolidated datelist of all off pointing images.
datelist=['2024-01-29', '2024-01-30', '2024-01-31']
for i in range(1,14):
    datelist.append('2024-02-'+str(i).zfill(2)) #making a consolidated datelist over jan and feb 2024 for off pointing


#iterate over xlsx files of various dates and make a concatenated dataframe.
for i in range(len(datelist)-1): #making a concatenated dataframe from excel files
    folder= suit_scratch+'suitproducts/xlsx/'+datelist[i+1].replace('-', '/')+'/' #excel files are in data download date folders.
    #Therefore, you need to go to n+1th day's folder to get nth day's excel file.
    sav= save_loc+datelist[i] 
    
    filelist= glob.glob(folder+'*.xlsx')
    parent_df= pd.DataFrame() #make a blank dataframe
    
    for file in filelist:
        df1= pd.read_excel(file)
        parent_df=pd.concat([parent_df, df1], ignore_index=True) #concatenate each excel file's dataframe df1 to df.
    
    df=parent_df #keeping parent_df isolated from work copy.
    df=df[df['IMG_TYPE']== mode ] #pick only engineering mode images
    #select files based on shutter pos
    if (shtrpos == 0): #choosing files by shutter position
        df=df[df['SHTR_STR']<2]
    elif (shtrpos == 180):
        df=df[df['SHTR_STR']>2]
        
    #select files based on complete/partial images
    if (typ == 'complete'):
        df=df[df['QDESC'] == "Complete Image"] # Dataframe of only Complete files.
    elif (typ == 'partial'):
        df=df[df['QDESC'] == "Parial Image"] # Dataframe of only Partial files 
   
    #generate realpath
    path= suit_scratch+'suit_data/level0fits/'+datelist[i].replace('-', '/')+'/engg4/' #parent string for realpath
    df["REALPATH"]= path+df['F_NAME'] #adds the realpath to the dataframe as a column.
    
    pointing1= df[df['DHOBT_DT'] < datelist[i]+'T07:20:00.000000000'] #pointing change happens at 07:20 UT
    pointing2= df[df['DHOBT_DT'] >= datelist[i]+'T07:20:00.000000000']
    pointing1= pointing1.drop_duplicates('DHOBT_DT') #remove duplicates with same time.
    pointing2= pointing2.drop_duplicates('DHOBT_DT')
    
    pointing1= pointing1.sort_values('FTR_NAME') #sort by filter name
    pointing2= pointing2.sort_values('FTR_NAME')
    
    #save csv file
    pointing1.to_csv(sav+'_'+typ+'_shtr_'+str(shtrpos)+'_p1.csv', columns=['REALPATH'], index=False, header=False) #does not save index numbers
    pointing2.to_csv(sav+'_'+typ+'_shtr_'+str(shtrpos)+'_p2.csv', columns=['REALPATH'], index=False, header= False) #does not save index numbers