#Author: Sepehr Roudini.
#University of Iowa
#Department of Chemical Engineering
#Date: 02/12/2018.
#Purpose: Plotting True color image
#projected (cylindrical) on map
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
#a map instance and projected and
#unprojected RGB data.
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
#This module is for plotting image.
    import matplotlib.pyplot as plt
#This module is for map projection.
    from mpl_toolkits.basemap import Basemap
#pyproj is for defining different projections
    import pyproj
#pyresample is for projecting
#image on a map.
    import pyresample as pr
#math is for mathematical operations
    import math
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
    File1 = h5py.File(filename1,'r')
    File2 = h5py.File(filename2, mode='r')
    File3 = h5py.File(filename3, 'r')
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Getting the reflectance data for RGB.
#--------------------------------------------------------------------------------------------#
    #get the reflectance data for green
    Greenrawreflectance = File2['All_Data']['VIIRS-M4-SDR_All']['Reflectance'][:]
    Greenfactors = File2['All_Data']['VIIRS-M4-SDR_All']['ReflectanceFactors'][:]
    Greenscale = Greenfactors[0]
    Greenoffset = Greenfactors[1]
    Greenreflectance = (Greenrawreflectance * Greenscale) + Greenoffset
    #Correcting for pixel trims
    bowtie1 = np.where(Greenreflectance>1)
    bowtie1[0][-12000:-1] = bowtie1[0][-12000:-1] -4
    bowtie1[0][:-12000] = bowtie1[0][:-12000] + 4
    Greenreflectance[np.where(Greenreflectance>1)] = Greenreflectance[bowtie1]
    Greenreflectance[np.where(Greenreflectance>1)] = 1
    #get the reflectance data for blue
    Bluerawreflectance = File1['All_Data']['VIIRS-M3-SDR_All']['Reflectance'][:]
    Bluefactors = File1['All_Data']['VIIRS-M3-SDR_All']['ReflectanceFactors'][:]
    Bluescale = Bluefactors[0]
    Blueoffset = Bluefactors[1]
    Bluereflectance = (Bluerawreflectance * Bluescale) + Blueoffset
    #Correcting for pixel trims
    bowtie2 = np.where(Bluereflectance>1)
    bowtie2[0][-12000:-1] = bowtie2[0][-12000:-1] -4
    bowtie2[0][:-12000] = bowtie2[0][:-12000] + 4
    Bluereflectance[np.where(Bluereflectance>1)] = Bluereflectance[bowtie2]
    Bluereflectance[np.where(Bluereflectance>1)] = 1
    #get the reflectance data for red
    Redrawreflectance = File3['All_Data']['VIIRS-M5-SDR_All']['Reflectance'][:]
    Redfactors = File3['All_Data']['VIIRS-M5-SDR_All']['ReflectanceFactors'][:]
    Redscale = Redfactors[0]
    Redoffset = Redfactors[1]
    Redreflectance = (Redrawreflectance*Redscale) + Redoffset
    #Correcting for pixel trims
    bowtie3 = np.where(Redreflectance>1)
    bowtie3[0][-12000:-1] = bowtie3[0][-12000:-1] -4
    bowtie3[0][:-12000] = bowtie3[0][:-12000] + 4
    Redreflectance[np.where(Redreflectance>1)] = Redreflectance[bowtie3]
    Redreflectance[np.where(Redreflectance>1)] = 1
    #getting the geolocation data
    Lat = File1['All_Data']['VIIRS-MOD-GEO_All']['Latitude'][:]
    Lon = File1['All_Data']['VIIRS-MOD-GEO_All']['Longitude'][:]
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#prepare RGB array
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
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Projecting data on map
#--------------------------------------------------------------------------------------------#
#obtaining max and min values of lat and lon
    lat_m = math.ceil(np.min(Lat))
    lat_M = math.ceil(np.max(Lat))
    lon_m = math.ceil(np.min(Lon))
    lon_M = math.ceil(np.max(Lon))
#defining the type of map projection(here is
#cylindrical projection)
    d = '+proj=eqc +lat_ts=0 +lat_0=%d +lon_0=%d +x_0=0' \
        ' +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m' \
        ' +no_defs'%(lat_m, lon_m)
#Getting the x,y value for the
#specified coordinates
    c = pyproj.Proj(d)
    a = c(lon_m, lat_m)
    b = c(lon_M, lat_M)
#Specifying number of pixels for image
    x_size = 3074
    y_size = 3200
#Specifying extent of the map
    area_id = '1'
    name = 'Map'
    proj_id = '1'
    area_extent = (a[0], a[1], b[0], b[1])
#Projecting data
    proj_dict = {'a': '6371228.0', 'units': 'm', 'lon_0':
        lon_m, 'proj': 'eqc', 'lat_0': lat_m}
    area_def = pr.geometry.AreaDefinition(area_id, name,
                                          proj_id, proj_dict,
                                          x_size, y_size, area_extent)
    swath_def = pr.geometry.SwathDefinition(Lon, Lat)
    data_swaths = rgbb_data
#Correlating the geolocation data
#with rgb data through nearest
#neighbor iterpolation(convert
#from swath to grid).
    result = pr.kd_tree.resample_nearest(swath_def, data_swaths,
                                         area_def, radius_of_influence=50000,
                                         fill_value=1)
    bmap = pr.plot.area_def2basemap(area_def)
#Plotting parallels and merridians on map
    Lat_Step = '%e' %np.linspace(lat_m,lat_M,7,retstep=True)[1]
    if Lat_Step[Lat_Step.index('e')+1] == '-':
     Lat_Floating_Number = int(Lat_Step[Lat_Step.index('e-')+2:])
    else:
     Lat_Floating_Number = 2
    Lon_Step = '%e' % np.linspace(lon_m, lon_M, 7, retstep=True)[1]
    if Lat_Step[Lat_Step.index('e') + 1] == '-':
     Lon_Floating_Number = int(Lon_Step[Lon_Step.index('e-') + 2:])
    else:
     Lon_Floating_Number = 2
    bmap.drawparallels(np.linspace(lat_m,lat_M,7)[1:6],fmt ='%.{}f'.format(Lat_Floating_Number),color ='k',
                      dashes=[2,1],labels=[1, 1, 0, 0], linewidth
                      =0.9,fontsize=15)
    bmap.drawmeridians(np.linspace(lon_m,lon_M,7)[1:6],fmt ='%.{}f'.format(Lon_Floating_Number),color ='k',
                      dashes=[2,1],labels=[0, 0, 1, 1], linewidth
                      =0.9,fontsize=15)
#Plotting the map
    bmap.drawcountries(linewidth=1.5)
    bmap.drawcoastlines(linewidth=0.85)
    bmap.drawstates(linewidth=0.5)
    bmap.imshow(result, origin='upper')
    if Save == 'True':
     plt.savefig(Path_to_M3Band_File +
                'VIIRS_Unprojected_True_Color_Image.png',
                bbox_inches='tight', dpi=200)
    #plt.show()
    return bmap, result, rgbb_data
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#