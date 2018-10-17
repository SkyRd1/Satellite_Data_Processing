#Author: Sepehr Roudini
#University of Iowa
#Department of Chemical Engineering
#Date: 01/02/2018
#Purpose: Reading hdf4 file and print out useful
#information


#--------------------------------------------------------------------------------------------#
#Defining function and import necessary libraries
#--------------------------------------------------------------------------------------------#

##############################################################################################
#Libraries used in this function are: netCDF4.
##############################################################################################
#Path_To_File: full path to file with
#file name in it.
##############################################################################################
#variables: either 'True or 'False, if 'True'
#variables will be printed out, default is
#'True'.
##############################################################################################
#Variables_Attributes: either 'True or 'False, if 'True'
#Variables_Attributes will be printed out, default is
#'True'.
##############################################################################################
#File_Attributes: either 'True or 'False, if 'True'
#File_Attributes will be printed out, default is
#'True'.
##############################################################################################
#This function returns "File" which has
#the hdf4 file information in it.
##############################################################################################
def Read_HDF4(Path_To_File, Variables='True',
              Variables_Attributes='True', File_Attributes='True'):
#This library is for reading hdf and netcdf files
    from netCDF4 import Dataset
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Reading the data and printing them out
#--------------------------------------------------------------------------------------------#
#Reading the hdf4 file
    File_Name =Path_To_File
    File = Dataset(File_Name)
    if Variables=='True':
        print('\x1b[6;30;42m' + 'File variables are:' + '\x1b[0m' + '\n')
        Count1 = 1
        for i in (File.variables):
            print(str(Count1) + ':', i)
            Count1 += 1
    if Variables_Attributes=='True':
        print ('{:=<150}'.format(''))
        print ('{:=<150}'.format(''))
        print('\x1b[6;30;42m' + 'Variables attributes are as follow:'+ '\x1b[0m' + '\n')
        Count2 = 1
        for i in (File.variables):
            print(str(Count2) + ': '+ str(i) + ' attributes are:\n', File.variables[str(i)])
            Count2 += 1
        print('{:=<150}'.format(''))
        print('{:=<150}'.format(''))
    if File_Attributes == 'True':
        print ('\x1b[6;30;42m' + 'File attributes are:' + '\x1b[0m' + '\n')
        print(File)
    return File
