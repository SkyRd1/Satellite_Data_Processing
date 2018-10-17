#Author: Sepehr Roudini.
#University of Iowa
#Department of Chemical Engineering
#Date: 12/28/2017.
#Purpose: Reading VIIRS AVAFO fire product and
#returning The latitude and longitude and aslo
#the julian day and overpass time(UTC)of each
#fire pixel in the area of interest.


#--------------------------------------------------------------------------------------------#
#Defining function and import necessary libraries.
#--------------------------------------------------------------------------------------------#

##############################################################################################
#Libraries used in this function are: h5py and
#Calendar_Date_to_Julian.
##############################################################################################
#Path_to_AVAFO_File: The path to the file
#accompanying the file name.
##############################################################################################
#minlon: minimum longitude in the area of interest.
##############################################################################################
#maxlon: maximum longitude in the area of interest.
##############################################################################################
#minlat: minimum latitude in the area of interest.
##############################################################################################
#maxlat: maximum latitude in the area of interest.
##############################################################################################
#This function returns respectively: latitudes
#(terrain corrected),longitudes(terrain corrected)
#,year,month, day, julian day,and start and end overpass time
#(UTC) of fire.
#pixels in the defined area.
##############################################################################################
#The saved text is saved in input file directory
#and has the name of input file with output.txt
#appended.
##############################################################################################
def Get_Date_Time_Coordinates(Path_to_AVAFO_File, minlon, maxlon, minlat, maxlat):
#h5py is for processing HDF5 files.
    import h5py
#numpy is for data manipulation
    import numpy as np
#This module is for converting calendar
#date to julian day.
    from Calendar_Date_to_Julian import Convert
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Reading data from our hdf file.
#--------------------------------------------------------------------------------------------#
#Specifying the file.
    filename = Path_to_AVAFO_File
#Opening the hdf5 file in read mode.
    file = h5py.File(filename, mode='r')
#Reading the fire latitudes and longitudes from hdf file.
    group1 = file['All_Data']
    subgroup1 = group1['VIIRS-AF-EDR_All']
    lat_0 = subgroup1['Latitude']['Latitude_0'][:]
    lon_0 = subgroup1['Longitude']['Longitude_0'][:]
    lat_1 = subgroup1['Latitude']['Latitude_1'][:]
    lon_1 = subgroup1['Longitude']['Longitude_1'][:]
    lat_2 = subgroup1['Latitude']['Latitude_2'][:]
    lon_2 = subgroup1['Longitude']['Longitude_2'][:]
    lat_3 = subgroup1['Latitude']['Latitude_3'][:]
    lon_3 = subgroup1['Longitude']['Longitude_3'][:]
#--------------------------------------------------------------------------------------------#
#Finding julian day and time.
#--------------------------------------------------------------------------------------------#
#Reading the date and time from file name.
    date = Path_to_AVAFO_File[Path_to_AVAFO_File.index('_d')+2:Path_to_AVAFO_File.index("_t")]
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    start_time = Path_to_AVAFO_File\
        [Path_to_AVAFO_File.index('_t')+2:Path_to_AVAFO_File.index("_e")]
    start_time = start_time[0:2]+'-'+start_time[2:4]+'-'+start_time[4:6]+'.'+start_time[6:]
    end_time = Path_to_AVAFO_File\
        [Path_to_AVAFO_File.index('_e')+2:Path_to_AVAFO_File.index("_b")]
    end_time = end_time[0:2]+'-'+end_time[2:4]+'-'+end_time[4:6]+'.'+end_time[6:]
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Calculating Julian day from date.
#--------------------------------------------------------------------------------------------#
    julian_day = Convert(month,day,year)
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------------------#
#Finding the fire pixels that are in the area of interest
#and saving coordinates and julianday and year and time.
#--------------------------------------------------------------------------------------------#
#Creating empty arrays for outputs.
    firelat = []
    firelon = []
    julianday = []
    Year = []
    starttime = []
    endtime = []
#Finding fire pixels coordinates and julian day and
#store them in arrays for later saving.
    for i in range(0, len(lat_0)):
        if (minlat <= lat_0[i]) & (lat_0[i] <= maxlat) & (minlon <= lon_0[i]) &\
                (lon_0[i] <= maxlon):
            firelat.append(lat_0[i])
            firelon.append(lon_0[i])
            julianday.append(julian_day)
            Year.append(year)
            starttime.append(start_time)
            endtime.append(end_time)
    for i in range(0, len(lat_1)):
        if (minlat <= lat_1[i]) & (lat_1[i] <= maxlat) & (minlon <= lon_1[i]) &\
                (lon_1[i] <= maxlon):
            firelat.append(lat_1[i])
            firelon.append(lon_1[i])
            julianday.append(julian_day)
            Year.append(year)
            starttime.append(start_time)
            endtime.append(end_time)
    for i in range(0, len(lat_2)):
        if (minlat <= lat_2[i]) & (lat_2[i] <= maxlat) & (minlon <= lon_2[i]) &\
                (lon_2[i] <= maxlon):
            firelat.append(lat_2[i])
            firelon.append(lon_2[i])
            julianday.append(julian_day)
            Year.append(year)
            starttime.append(start_time)
            endtime.append(end_time)
    for i in range(0, len(lat_3)):
        if (minlat <= lat_3[i]) & (lat_3[i] <= maxlat) & (minlon <= lon_3[i]) &\
                (lon_3[i] <= maxlon):
            firelat.append(lat_3[i])
            firelon.append(lon_3[i])
            julianday.append(julian_day)
            Year.append(year)
            starttime.append(start_time)
            endtime.append(end_time)
# Making the data list as array type
    firelat = np.asanyarray(firelat)
    firelon = np.asanyarray(firelon)
    Year = np.asanyarray(Year)
    julianday = np.asanyarray(julianday)
    starttime = np.asanyarray(starttime)
    endtime = np.asanyarray(endtime)
    output = open(Path_to_AVAFO_File+'_Output.txt', 'w')
    output.write('This is the output file contains fire pixel information extracted'
                 ' from AVAFO fire product'+'\n'+
                 'Fire Terrain Corrected Longitude: '+str(firelon)+'\n'+
                 'Fire Terrain Corrected Latitude: '+str(firelat)+'\n'\
                 +'Year of Fire: '+ str(Year)+'\n'+'Julian Day of Fire: ' +
                 str(julianday)+'\n'+
                 'Satellite Start Overpass Time: '+ str(starttime)+'\n'+ \
                 'Satellite End Overpass Time:' + str(endtime)+'\n')
#Also save lat and lon along with
#the julian day number as binary files
    Lat_0 = bytearray(lat_0)
    Lon_0 = bytearray(lon_0)
    Julianday = bytearray(julianday)
    output2 = open(Path_to_AVAFO_File+'_lat.dat', 'wb')
    output2.write(Lat_0)
    output3 = open(Path_to_AVAFO_File + '_lon.dat', 'wb')
    output3.write(Lon_0)
    output4 = open(Path_to_AVAFO_File + '_Julianday.dat', 'wb')
    output4.write(Julianday)
    return firelat, firelon, Year, month, day, julianday, starttime,endtime