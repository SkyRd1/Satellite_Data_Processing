#Author: Sepehr Roudini.
#University of Iowa
#Department of Chemical Engineering
#Date: 02/09/2018.
#Purpose: Plotting True color image
#using VIIRS M3,M4, and M5 bands.


#--------------------------------------------------------------------------------------------#
#Defining function and importing necessary libraries.
#--------------------------------------------------------------------------------------------#

##############################################################################################
#Libraries used in this function are: numpy, h5py,
#matplotlib, Read_VIIRS_Data, and cv2.
##############################################################################################
#Path_To_M3Band_File: full path to hdf5 VIIRS
#M3Band file with file name in it.
##############################################################################################
#Path_To_M4Band_File: full path to hdf5 VIIRS
#M4Band file with file name in it.
##############################################################################################
#Path_To_M5Band_File: full path to hdf5 VIIRS
#M5Band file with file name in it.
##############################################################################################
#Path_To_GMTCO_npp_File: full path to hdf5
#VIIRS Mband terrein corrected geolocation
#file with file name in it.
##############################################################################################
#Save: either 'True' or 'False', if true,
# a true color image will be saved.
##############################################################################################
#This functions returnes respectively:
#an image instance and RGB data.
##############################################################################################
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
def plot_True_Color_Image(Path_to_M3Band_File, Path_to_M4Band_File,
                          Path_to_M5Band_File, Save='True'):
#numpy is for data manipulation
    import numpy as np
#This module is for plotting image.
    import matplotlib.pyplot as plt
#cv2 is for manipulating image data.
    import cv2 as cv
#h5py is for processing HDF5 files
    import h5py
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Reading data from our hdf file
#--------------------------------------------------------------------------------------------#
#Specifying the file
    filename1 = Path_to_M3Band_File
    filename2 = Path_to_M4Band_File
    filename3 = Path_to_M5Band_File
#Opening our hdf file in read mode
    file1 = h5py.File(filename1,'r')
    file2 = h5py.File(filename2, mode='r')
    file3 = h5py.File(filename3, 'r')
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Getting the reflectance data for RGB.
#--------------------------------------------------------------------------------------------#
#get the reflectance data for green
    Greenrawreflectance = file2['All_Data']['VIIRS-M4-SDR_All']['Reflectance'][:]
    Greenfactors = file2['All_Data']['VIIRS-M4-SDR_All']['ReflectanceFactors'][:]
    Greenscale = Greenfactors[0]
    Greenoffset = Greenfactors[1]
    Greenreflectance = (Greenrawreflectance * Greenscale) + Greenoffset
    Greenreflectance[np.where(Greenreflectance>1)] = 1
#get the reflectance data for blue
    Bluerawreflectance = file1['All_Data']['VIIRS-M3-SDR_All']['Reflectance'][:]
    Bluefactors = file1['All_Data']['VIIRS-M3-SDR_All']['ReflectanceFactors'][:]
    Bluescale = Bluefactors[0]
    Blueoffset = Bluefactors[1]
    Bluereflectance = (Bluerawreflectance * Bluescale) + Blueoffset
    Bluereflectance[np.where(Bluereflectance>1)] = 1
#get the reflectance data for red
    Redrawreflectance = file3['All_Data']['VIIRS-M5-SDR_All']['Reflectance'][:]
    Redfactors = file3['All_Data']['VIIRS-M5-SDR_All']['ReflectanceFactors'][:]
    Redscale = Redfactors[0]
    Redoffset = Redfactors[1]
    Redreflectance = (Redrawreflectance*Redscale) + Redoffset
    Redreflectance[np.where(Redreflectance>1)] = 1
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#prepare RGB array and plot it
#--------------------------------------------------------------------------------------------#
#data should be in form of integers between
#0-255 so that opencv library can execute
#histogram equalization
    red = Redreflectance * 255
    red = red.astype(np.uint8)
    green = Greenreflectance * 255
    green = green.astype(np.uint8)
    blue = Bluereflectance * 255
    blue = blue.astype(np.uint8)
#Implementing histogram equalization
    red = cv.equalizeHist(red)
    green = cv.equalizeHist(green)
    blue = cv.equalizeHist(blue)
#Producing RGB data
    rgbb_data = np.dstack((red, green, blue))
    rgbb_data = rgbb_data / 255.
    rgbb_data[rgbb_data < 0] = 0.0
    rgbb_data[rgbb_data > 1] = 1
#Plotting image
    Image = plt.imshow(np.flipud(np.fliplr(rgbb_data)), origin='upper')
    if Save == 'True':
        plt.savefig(Path_to_M3Band_File +
                    'VIIRS_Unprojected_True_Color_Image.png',
                    bbox_inches='tight', dpi = 200 )
    return Image, rgbb_data
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#