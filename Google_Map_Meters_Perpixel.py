#Author: Sepehr Roudini.
#University of Iowa
#Department of Chemical Engineering
#Date: 12/29/2017.
#Purpose: Calculating number of meters
#per pixel in a static google map image


# --------------------------------------------------------------------------------------------#
# Defining function and import necessary libraries.
# --------------------------------------------------------------------------------------------#

##############################################################################################
#Libraries used in this function are: numpy.
##############################################################################################
#Zoom_Level: The zoom level of the map which
#can be between 0 (view of the whole world) to
#21(view of an individual building).
##############################################################################################
#This function returns the number of
#meters per pixel in the google map image.
##############################################################################################
def Get_Meters(Zoom_Level):
#numpy is for data manipulation
    import numpy as np
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Calculating meters per pixel
#--------------------------------------------------------------------------------------------#
    Number_of_Pixels = 256
    earth_radius = 6378137.0
    metersPerPixel = (2*np.pi*earth_radius)/(pixels_in_image*(2**zoomlevel))
    return metersPerPixel
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#